import requests
from bs4 import BeautifulSoup
import json

def scrape_match_details(url):
    """
    Scrapes match details from a Cricbuzz match facts URL using updated, robust selectors
    for the mobile version of the site. Also extracts the link to the full commentary.

    Args:
        url (str): The URL of the Cricbuzz match page.

    Returns:
        dict: A dictionary containing the scraped match data, or None if an error occurs.
    """
    print(f"Attempting to scrape data from: {url}")

    try:
        # Set a User-Agent to mimic a real web browser to avoid being blocked.
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Make the GET request to the URL with the specified headers.
        response = requests.get(url, headers=headers)

        # Raise an exception for bad status codes (like 404 or 500).
        response.raise_for_status()

        # Parse the HTML content of the page using BeautifulSoup.
        soup = BeautifulSoup(response.text, 'html.parser')

        # --- Data Extraction ---
        
        # Create a dictionary to hold the scraped data.
        match_data = {}

        # Extract the main match title from the <h1> tag.
        h1_tag = soup.find('h1')
        if h1_tag:
            # Clean up the title text
            match_data['matchTitle'] = h1_tag.get_text(strip=True).split('-')[0]

        # --- Extract Match Details (Series, Date, Toss, etc.) ---
        # Find the main container for match details.
        details_container = soup.find('div', class_='cb-match-details')
        if details_container:
            # Find all the detail rows within the container.
            detail_rows = details_container.find_all('div', class_='cb-col-100 cb-col')
            for row in detail_rows:
                # The label (e.g., "Series:") and value are in separate divs.
                label_div = row.find('div', class_='cb-col-27')
                value_div = row.find('div', class_='cb-col-73')
                
                if label_div and value_div:
                    label = label_div.get_text(strip=True).replace(':', '')
                    value = value_div.get_text(strip=True)
                    
                    # Use a mapping to keep the keys clean.
                    key_map = {
                        'Series': 'series',
                        'Date': 'date',
                        'Time': 'time',
                        'Toss': 'toss',
                        'Venue': 'venue'
                    }
                    if label in key_map:
                        match_data[key_map[label]] = value

        # --- Extract Squads ---
        squads = {}
        # Find all the squad container blocks.
        squad_containers = soup.find_all('div', class_='cb-team-squad')
        for container in squad_containers:
            # Get the team name from the header of the squad block.
            team_name_header = container.find('div', class_='cb-squad-hdr')
            if not team_name_header:
                continue
            
            team_name = team_name_header.get_text(strip=True).replace(' Squad', '')
            
            # Find all player links within this squad block.
            player_links = container.find_all('a', class_='text-hvr-underline')
            players = [link.get_text(strip=True) for link in player_links]
            
            if team_name and players:
                squads[team_name] = players
        
        match_data['squads'] = squads

        # --- Extract Commentary Link ---
        # Find the link by its title attribute, which is a reliable selector.
        commentary_link_tag = soup.find('a', title=lambda t: t and 'Full Commentary' in t)
        if commentary_link_tag and commentary_link_tag.has_attr('href'):
            commentary_path = commentary_link_tag['href']
            # Prepend the base URL to make the link absolute and usable.
            match_data['commentaryLink'] = f"https://m.cricbuzz.com{commentary_path}"
        else:
            match_data['commentaryLink'] = "Not found"


        return match_data

    except requests.exceptions.RequestException as e:
        print(f"Error during request to URL: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during scraping: {e}")
        return None

# --- Main execution ---
if __name__ == "__main__":
    # The URL of the match facts page to scrape.
    TARGET_URL = "https://m.cricbuzz.com/cricket-match-facts/105778/eng-vs-ind-4th-test-india-tour-of-england-2025"

    # Call the function to scrape the data from the URL.
    scraped_data = scrape_match_details(TARGET_URL)

    # If data was successfully scraped, print it in a nicely formatted JSON.
    if scraped_data:
        print("\n--- Match Details Scraped Successfully ---")
        # Use json.dumps for pretty-printing the dictionary with an indent.
        print(json.dumps(scraped_data, indent=4))
