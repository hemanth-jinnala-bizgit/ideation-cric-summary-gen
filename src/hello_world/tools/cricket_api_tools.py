# # # src/cricket_crew/tools/cricket_api_tools.py
# # from crewai.tools import BaseTool
# # from typing import Type, Dict, Any, List
# # from pydantic import BaseModel, Field
# # import requests
# # from tabulate import tabulate
# # from datetime import datetime
# # import json

# # class CricketAPIInput(BaseModel):
# #     """Input schema for Cricket API tools."""
# #     match_id: str = Field(..., description="The match ID to fetch data for")

# # class ScorecardTool(BaseTool):
# #     name: str = "Cricket Scorecard Fetcher"
# #     description: str = (
# #         "Fetches detailed scorecard information including batting and bowling statistics, "
# #         "team scores, extras, powerplay details, and dismissal information for a cricket match."
# #     )
# #     args_schema: Type[BaseModel] = CricketAPIInput

# #     def _run(self, match_id: str) -> str:
# #         """Fetch and format scorecard data"""
# #         url = "https://unofficial-cricbuzz.p.rapidapi.com/matches/get-scorecard"
# #         querystring = {"matchId": match_id}
# #         headers = {
# #             "X-RapidAPI-Host": "unofficial-cricbuzz.p.rapidapi.com",
# #             "X-RapidAPI-Key": "0251d0e808mshf2b38142969493ap110abajsnd14d99bb9cf3"
# #         }
        
# #         try:
# #             response = requests.get(url, headers=headers, params=querystring)
# #             if response.status_code == 200:
# #                 data = response.json()
# #                 return self._format_scorecard(data)
# #             else:
# #                 return f"❌ Failed to fetch scorecard. Status code: {response.status_code}"
# #         except Exception as e:
# #             return f"❌ Error fetching scorecard: {str(e)}"
    
# #     def _format_scorecard(self, data: Dict[Any, Any]) -> str:
# #         """Format scorecard data into readable text"""
# #         result = "🏏 MATCH SCORECARD\n" + "="*50 + "\n\n"
        
# #         scorecard_list = data.get('scorecard', [])
        
# #         for innings in scorecard_list:
# #             team_name = innings.get('batTeamName', 'Unknown Team')
# #             score = innings.get('score', 0)
# #             wickets = innings.get('wickets', 0)
# #             overs = innings.get('overs', 0)
# #             run_rate = innings.get('runRate', 0)
            
# #             result += f"🏏 {team_name}: {score}/{wickets} ({overs} overs)\n"
# #             result += f"Run Rate: {run_rate}\n\n"
            
# #             result += "BATTING PERFORMANCE:\n"
# #             result += "-" * 30 + "\n"
            
# #             for batsman in innings.get('batsman', []):
# #                 name = batsman.get('name', 'Unknown')
# #                 runs = batsman.get('runs', 0)
# #                 balls = batsman.get('balls', 0)
# #                 fours = batsman.get('fours', 0)
# #                 sixes = batsman.get('sixes', 0)
# #                 strike_rate = batsman.get('strkRate', 0)
# #                 dismissal = batsman.get('outDec', 'Not Out')
                
# #                 result += f"{name}: {runs} ({balls}b, {fours}×4, {sixes}×6) SR: {strike_rate} - {dismissal}\n"
            
# #             extras = innings.get('extras', {}).get('total', 0)
# #             powerplay_runs = innings.get('pp', [{}])[0].get('powerPlay', [{}])[0].get('run', 'N/A')
            
# #             result += f"\nExtras: {extras}\n"
# #             result += f"Powerplay: {powerplay_runs} runs\n"
# #             result += "\n" + "="*50 + "\n\n"
        
# #         return result

# # class MatchInfoTool(BaseTool):
# #     name: str = "Cricket Match Info Fetcher"
# #     description: str = (
# #         "Fetches comprehensive match information including series details, teams, venue, "
# #         "toss result, match format, officials, and timing information."
# #     )
# #     args_schema: Type[BaseModel] = CricketAPIInput

# #     def _run(self, match_id: str) -> str:
# #         """Fetch and format match info"""
# #         url = "https://unofficial-cricbuzz.p.rapidapi.com/matches/get-info"
# #         querystring = {"matchId": match_id}
# #         headers = {
# #             "X-RapidAPI-Host": "unofficial-cricbuzz.p.rapidapi.com",
# #             "X-RapidAPI-Key": "0251d0e808mshf2b38142969493ap110abajsnd14d99bb9cf3"
# #         }
        
# #         try:
# #             response = requests.get(url, headers=headers, params=querystring)
# #             if response.status_code == 200:
# #                 data = response.json()
# #                 return self._format_match_info(data)
# #             else:
# #                 return f"❌ Failed to fetch match info. Status code: {response.status_code}"
# #         except Exception as e:
# #             return f"❌ Error fetching match info: {str(e)}"
    
# #     def _format_match_info(self, data: Dict[Any, Any]) -> str:
# #         """Format match info into readable text"""
# #         def format_timestamp(ts):
# #             if ts:
# #                 return datetime.utcfromtimestamp(int(ts)//1000).strftime('%Y-%m-%d %H:%M:%S')
# #             return 'N/A'
        
# #         result = "📋 MATCH INFORMATION\n" + "="*40 + "\n\n"
        
# #         series_name = data.get('seriesName', 'Unknown Series')
# #         match_desc = data.get('matchDesc', 'Unknown Match')
# #         match_format = data.get('matchFormat', 'Unknown Format')
# #         status = data.get('status', 'Unknown Status')
        
# #         team1 = data.get('team1', {}).get('teamName', 'Team 1')
# #         team2 = data.get('team2', {}).get('teamName', 'Team 2')
        
# #         venue_info = data.get('venueInfo', {})
# #         ground = venue_info.get('ground', 'Unknown Ground')
# #         city = venue_info.get('city', 'Unknown City')
        
# #         toss = data.get('toss', 'Unknown')
# #         start_date = format_timestamp(data.get('startDate'))
# #         end_date = format_timestamp(data.get('endDate'))
        
# #         umpire1 = data.get('umpire1', {}).get('name', 'Unknown')
# #         umpire2 = data.get('umpire2', {}).get('name', 'Unknown')
# #         referee = data.get('referee', {}).get('name', 'Unknown')
        
# #         result += f"Series: {series_name}\n"
# #         result += f"Match: {match_desc}\n"
# #         result += f"Format: {match_format}\n"
# #         result += f"Status: {status}\n"
# #         result += f"Teams: {team1} vs {team2}\n"
# #         result += f"Venue: {ground}, {city}\n"
# #         result += f"Toss: {toss}\n"
# #         result += f"Start: {start_date}\n"
# #         result += f"End: {end_date}\n"
# #         result += f"Umpires: {umpire1}, {umpire2}\n"
# #         result += f"Referee: {referee}\n"
        
# #         return result

# # class HighlightsTool(BaseTool):
# #     name: str = "Cricket Highlights Fetcher"
# #     description: str = (
# #         "Fetches key highlights and important moments from the match commentary, "
# #         "including wickets, boundaries, milestones, and other significant events."
# #     )
# #     args_schema: Type[BaseModel] = CricketAPIInput

# #     def _run(self, match_id: str) -> str:
# #         """Fetch and format highlights"""
# #         url = "https://unofficial-cricbuzz.p.rapidapi.com/matches/get-highlights"
# #         querystring = {"matchId": match_id}
# #         headers = {
# #             "X-RapidAPI-Host": "unofficial-cricbuzz.p.rapidapi.com",
# #             "X-RapidAPI-Key": "0251d0e808mshf2b38142969493ap110abajsnd14d99bb9cf3"
# #         }
        
# #         try:
# #             response = requests.get(url, headers=headers, params=querystring)
# #             if response.status_code == 200:
# #                 data = response.json()
# #                 return self._format_highlights(data)
# #             else:
# #                 return f"❌ Failed to fetch highlights. Status code: {response.status_code}"
# #         except Exception as e:
# #             return f"❌ Error fetching highlights: {str(e)}"
    
# #     def _format_highlights(self, data: Dict[Any, Any]) -> str:
# #         """Format highlights into readable text"""
# #         result = "⚡ MATCH HIGHLIGHTS\n" + "="*40 + "\n\n"
        
# #         commentary_lines = data.get("commentaryLines", [])
        
# #         if not commentary_lines:
# #             return result + "No highlights available.\n"
        
# #         for i, event in enumerate(commentary_lines, 1):
# #             commentary = event.get("commentary", {})
# #             over_num = commentary.get("overNum", "")
# #             event_type = commentary.get("eventType", "")
# #             text = commentary.get("commtxt", "")
            
# #             if text:  # Only include non-empty commentary
# #                 result += f"{i}. Over {over_num} - {event_type}\n"
# #                 result += f"   {text}\n\n"
        
# #         return result

# # class CommentaryTool(BaseTool):
# #     name: str = "Cricket Commentary Fetcher"
# #     description: str = (
# #         "Fetches ball-by-ball commentary for the entire match, providing detailed "
# #         "insights into each delivery, player performances, and match progression."
# #     )
# #     args_schema: Type[BaseModel] = CricketAPIInput

# #     def _run(self, match_id: str) -> str:
# #         """Fetch and format commentary"""
# #         url = "https://unofficial-cricbuzz.p.rapidapi.com/matches/get-commentaries"
# #         querystring = {"matchId": match_id}
# #         headers = {
# #             "X-RapidAPI-Host": "unofficial-cricbuzz.p.rapidapi.com",
# #             "X-RapidAPI-Key": "0251d0e808mshf2b38142969493ap110abajsnd14d99bb9cf3"
# #         }
        
# #         try:
# #             response = requests.get(url, headers=headers, params=querystring)
# #             if response.status_code == 200:
# #                 data = response.json()
# #                 return self._format_commentary(data)
# #             else:
# #                 return f"❌ Failed to fetch commentary. Status code: {response.status_code}"
# #         except Exception as e:
# #             return f"❌ Error fetching commentary: {str(e)}"
    
# #     def _format_commentary(self, data: Dict[Any, Any]) -> str:
# #         """Format commentary into readable text"""
# #         result = "🎤 MATCH COMMENTARY\n" + "="*40 + "\n\n"
        
# #         commentary_lines = data.get('commentaryLines', [])
        
# #         if not commentary_lines:
# #             return result + "No commentary available.\n"
        
# #         # Group commentary by overs for better readability
# #         current_over = None
        
# #         for line in commentary_lines:
# #             commentary = line.get('commentary', {})
# #             commtxt = commentary.get('commtxt', '').replace('B0$', '').replace('B1$', '').strip()
# #             event_type = commentary.get('eventType', '')
# #             over_num = commentary.get('overNum', '')
# #             timestamp = commentary.get('timestamp', '')
            
# #             if commtxt:  # Only include non-empty commentary
# #                 # Add over header if it's a new over
# #                 if over_num and over_num != current_over:
# #                     result += f"\n--- OVER {over_num} ---\n"
# #                     current_over = over_num
                
# #                 result += f"[{event_type}] {commtxt}\n"
        
# #         return result















# from crewai.tools import BaseTool
# from typing import Type, Dict, Any
# from pydantic import BaseModel, Field
# import requests
# from tabulate import tabulate
# from datetime import datetime

# class CricketAPIInput(BaseModel):
#     """Input schema for Cricket API tools."""
#     match_id: str = Field(..., description="The match ID to fetch data for")

# class MatchSummaryTool(BaseTool):
#     name: str = "Match Final Summary Tool"
#     description: str = (
#         "Fetches the definitive final match summary, including the official result, status, "
#         "and Man of the Match. This should be the first tool used to verify the outcome."
#     )
#     args_schema: Type[BaseModel] = CricketAPIInput

#     def _run(self, match_id: str) -> str:
#         """Fetch and format the final match summary."""
#         url = "https://unofficial-cricbuzz.p.rapidapi.com/matches/get-overs"
#         querystring = {"matchId": match_id}
#         headers = {
#             "X-RapidAPI-Host": "unofficial-cricbuzz.p.rapidapi.com",
#             "X-RapidAPI-Key": "0251d0e808mshf2b38142969493ap110abajsnd14d99bb9cf3"
#         }
#         try:
#             response = requests.get(url, headers=headers, params=querystring)
#             if response.status_code == 200:
#                 data = response.json()
#                 return self._format_summary(data)
#             else:
#                 return f"❌ Failed to fetch final summary. Status code: {response.status_code}"
#         except Exception as e:
#             return f"❌ Error fetching final summary: {str(e)}"

#     def _format_summary(self, data: Dict[Any, Any]) -> str:
#         """Formats the summary data into readable text."""
#         match_info = data.get('matchHeaders', {})
#         miniscore = data.get('miniscore', {})
        
#         match_summary_data = [
#             ["Match Description", match_info.get('matchDesc', 'N/A')],
#             ["Series", match_info.get('seriesName', 'N/A')],
#             ["Official Status", match_info.get('status', 'N/A')],
#             ["Final Result", miniscore.get('custStatus', 'Result not available')]
#         ]
        
#         return "📋 OFFICIAL MATCH RESULT\n" + tabulate(match_summary_data, tablefmt="grid")

# class ScorecardTool(BaseTool):
#     name: str = "Cricket Scorecard Fetcher"
#     description: str = (
#         "Fetches detailed scorecard information including batting and bowling statistics, "
#         "team scores, extras, powerplay details, and dismissal information for a cricket match."
#     )
#     args_schema: Type[BaseModel] = CricketAPIInput

#     def _run(self, match_id: str) -> str:
#         # --- Function implementation remains the same ---
#         url = "https://unofficial-cricbuzz.p.rapidapi.com/matches/get-scorecard"
#         querystring = {"matchId": match_id}
#         headers = {
#             "X-RapidAPI-Host": "unofficial-cricbuzz.p.rapidapi.com",
#             "X-RapidAPI-Key": "0251d0e808mshf2b38142969493ap110abajsnd14d99bb9cf3"
#         }
#         try:
#             response = requests.get(url, headers=headers, params=querystring)
#             if response.status_code == 200:
#                 data = response.json()
#                 return self._format_scorecard(data)
#             else:
#                 return f"❌ Failed to fetch scorecard. Status code: {response.status_code}"
#         except Exception as e:
#             return f"❌ Error fetching scorecard: {str(e)}"

#     def _format_scorecard(self, data: Dict[Any, Any]) -> str:
#         """Format scorecard data into readable text"""
#         result = "🏏 MATCH SCORECARD\n" + "="*50 + "\n\n"
#         scorecard_list = data.get('scorecard', [])
#         for innings in scorecard_list:
#             team_name = innings.get('batTeamName', 'Unknown Team')
#             score = innings.get('score', 0)
#             wickets = innings.get('wickets', 0)
#             overs = innings.get('overs', 0)
#             result += f"🏏 {team_name}: {score}/{wickets} ({overs} overs)\n"
#             result += "BATTING PERFORMANCE:\n" + "-" * 30 + "\n"
#             for batsman in innings.get('batsman', []):
#                 name = batsman.get('name', 'Unknown')
#                 runs = batsman.get('runs', 0)
#                 balls = batsman.get('balls', 0)
#                 dismissal = batsman.get('outDec', 'Not Out')
#                 result += f"{name}: {runs} ({balls}b) - {dismissal}\n"
#             result += "\n" + "="*50 + "\n\n"
#         return result

# class MatchInfoTool(BaseTool):
#     name: str = "Cricket Match Info Fetcher"
#     description: str = (
#         "Fetches comprehensive match information including series details, teams, venue, "
#         "toss result, match format, and officials."
#     )
#     args_schema: Type[BaseModel] = CricketAPIInput

#     def _run(self, match_id: str) -> str:
#         # --- Function implementation remains the same ---
#         url = "https://unofficial-cricbuzz.p.rapidapi.com/matches/get-info"
#         querystring = {"matchId": match_id}
#         headers = {
#             "X-RapidAPI-Host": "unofficial-cricbuzz.p.rapidapi.com",
#             "X-RapidAPI-Key": "0251d0e808mshf2b38142969493ap110abajsnd14d99bb9cf3"
#         }
#         try:
#             response = requests.get(url, headers=headers, params=querystring)
#             if response.status_code == 200:
#                 data = response.json()
#                 return self._format_match_info(data)
#             else:
#                 return f"❌ Failed to fetch match info. Status code: {response.status_code}"
#         except Exception as e:
#             return f"❌ Error fetching match info: {str(e)}"
            
#     def _format_match_info(self, data: Dict[Any, Any]) -> str:
#         result = "📋 MATCH INFORMATION\n" + "="*40 + "\n\n"
#         result += f"Series: {data.get('seriesName', 'N/A')}\n"
#         result += f"Match: {data.get('matchDesc', 'N/A')}\n"
#         result += f"Status: {data.get('status', 'N/A')}\n"
#         result += f"Toss: {data.get('toss', 'N/A')}\n"
#         return result

# class HighlightsTool(BaseTool):
#     name: str = "Cricket Highlights Fetcher"
#     description: str = (
#         "Fetches key highlights and important moments from the match commentary."
#     )
#     args_schema: Type[BaseModel] = CricketAPIInput

#     def _run(self, match_id: str) -> str:
#         # --- Function implementation remains the same ---
#         url = "https://unofficial-cricbuzz.p.rapidapi.com/matches/get-highlights"
#         querystring = {"matchId": match_id}
#         headers = {
#             "X-RapidAPI-Host": "unofficial-cricbuzz.p.rapidapi.com",
#             "X-RapidAPI-Key": "0251d0e808mshf2b38142969493ap110abajsnd14d99bb9cf3"
#         }
#         try:
#             response = requests.get(url, headers=headers, params=querystring)
#             if response.status_code == 200:
#                 data = response.json()
#                 return self._format_highlights(data)
#             else:
#                 return f"❌ Failed to fetch highlights. Status code: {response.status_code}"
#         except Exception as e:
#             return f"❌ Error fetching highlights: {str(e)}"
    
#     def _format_highlights(self, data: Dict[Any, Any]) -> str:
#         result = "⚡ MATCH HIGHLIGHTS\n" + "="*40 + "\n\n"
#         for i, event in enumerate(data.get("commentaryLines", []), 1):
#             commentary = event.get("commentary", {})
#             text = commentary.get("commtxt", "")
#             if text:
#                 result += f"{i}. Over {commentary.get('overNum', '')}: {text}\n"
#         return result

# class CommentaryTool(BaseTool):
#     name: str = "Cricket Commentary Fetcher"
#     description: str = (
#         "Fetches ball-by-ball commentary for the entire match."
#     )
#     args_schema: Type[BaseModel] = CricketAPIInput

#     def _run(self, match_id: str) -> str:
#         # --- Function implementation remains the same ---
#         url = "https://unofficial-cricbuzz.p.rapidapi.com/matches/get-commentaries"
#         querystring = {"matchId": match_id}
#         headers = {
#             "X-RapidAPI-Host": "unofficial-cricbuzz.p.rapidapi.com",
#             "X-RapidAPI-Key": "0251d0e808mshf2b38142969493ap110abajsnd14d99bb9cf3"
#         }
#         try:
#             response = requests.get(url, headers=headers, params=querystring)
#             if response.status_code == 200:
#                 data = response.json()
#                 return self._format_commentary(data)
#             else:
#                 return f"❌ Failed to fetch commentary. Status code: {response.status_code}"
#         except Exception as e:
#             return f"❌ Error fetching commentary: {str(e)}"
            
#     def _format_commentary(self, data: Dict[Any, Any]) -> str:
#         result = "🎤 MATCH COMMENTARY\n" + "="*40 + "\n\n"
#         current_over = None
#         for line in data.get('commentaryLines', []):
#             commentary = line.get('commentary', {})
#             commtxt = commentary.get('commtxt', '').strip()
#             over_num = commentary.get('overNum', '')
#             if commtxt:
#                 if over_num and over_num != current_over:
#                     result += f"\n--- OVER {over_num} ---\n"
#                     current_over = over_num
#                 result += f"[{commentary.get('eventType', '')}] {commtxt}\n"
#         return result

































#src/hello_world/tools/cricket_api_tools.py


from crewai.tools import BaseTool
from typing import Type, Dict, Any
from pydantic import BaseModel, Field
import requests
from tabulate import tabulate
from datetime import datetime

class CricketAPIInput(BaseModel):
    """Input schema for Cricket API tools."""
    match_id: str = Field(..., description="The match ID to fetch data for")

class MatchSummaryTool(BaseTool):
    name: str = "Match Final Summary Tool"
    description: str = (
        "Fetches the definitive final match summary, including the official result, status, teams, "
        "and Man of the Match. This should be the first tool used to verify the outcome."
    )
    args_schema: Type[BaseModel] = CricketAPIInput

    def _run(self, match_id: str) -> str:
        url = "https://unofficial-cricbuzz.p.rapidapi.com/matches/get-overs"
        querystring = {"matchId": match_id}
        headers = {
            "X-RapidAPI-Host": "unofficial-cricbuzz.p.rapidapi.com",
            "X-RapidAPI-Key": "0251d0e808mshf2b38142969493ap110abajsnd14d99bb9cf3"
        }
        try:
            response = requests.get(url, headers=headers, params=querystring)
            if response.status_code == 204:
                return f"❌ Error: No content found for match_id '{match_id}'. It is likely invalid. Please use a numerical ID."
            if response.status_code == 200:
                data = response.json()
                return self._format_summary(data)
            else:
                return f"❌ Failed to fetch final summary. Status code: {response.status_code}"
        except Exception as e:
            return f"❌ Error fetching final summary: {str(e)}"

    def _format_summary(self, data: Dict[Any, Any]) -> str:
        match_info = data.get('matchHeaders', {})
        miniscore = data.get('miniscore', {})
        
        # --- CORRECTED TEAM NAME LOGIC ---
        team_details = match_info.get('teamDetails', {})
        bat_team = team_details.get('batTeamName', 'Team A') if team_details else 'Team A'
        bowl_team = team_details.get('bowlTeamName', 'Team B') if team_details else 'Team B'
        teams = f"{bat_team} vs {bowl_team}"
        # --- END OF FIX ---

        man_of_the_match = miniscore.get('playerManOfTheMatch', {}).get('name', 'Not Announced')
        target = miniscore.get('target', 'N/A')

        match_summary_data = [
            ["Match", f"{match_info.get('matchDesc', 'N/A')} - {match_info.get('seriesName', 'N/A')}"],
            ["Teams", teams],
            ["Result", miniscore.get('custStatus', 'Result not available')],
            ["Man of the Match", man_of_the_match],
            ["Target", f"{target} runs" if target != 'N/A' else "N/A"]
        ]
        
        return "📋 OFFICIAL MATCH SUMMARY\n" + tabulate(match_summary_data, tablefmt="grid")

# ... (The rest of the tools: ScorecardTool, MatchInfoTool, etc. remain the same) ...
class ScorecardTool(BaseTool):
    name: str = "Cricket Scorecard Fetcher"
    description: str = "Fetches detailed scorecard information including batting and bowling statistics for a cricket match."
    args_schema: Type[BaseModel] = CricketAPIInput

    def _run(self, match_id: str) -> str:
        url = "https://unofficial-cricbuzz.p.rapidapi.com/matches/get-scorecard"
        querystring = {"matchId": match_id}
        headers = {
            "X-RapidAPI-Host": "unofficial-cricbuzz.p.rapidapi.com",
            "X-RapidAPI-Key": "0251d0e808mshf2b38142969493ap110abajsnd14d99bb9cf3"
        }
        try:
            response = requests.get(url, headers=headers, params=querystring)
            if response.status_code == 200:
                return self._format_scorecard(response.json())
            return f"❌ Failed to fetch scorecard. Status code: {response.status_code}"
        except Exception as e:
            return f"❌ Error fetching scorecard: {str(e)}"

    def _format_scorecard(self, data: Dict[Any, Any]) -> str:
        result = "🏏 MATCH SCORECARD\n" + "="*50 + "\n\n"
        for innings in data.get('scorecard', []):
            team_name = innings.get('batTeamName', 'N/A')
            result += f"🏏 {team_name}: {innings.get('score', 0)}/{innings.get('wickets', 0)} ({innings.get('overs', 0)} overs)\n"
            result += "BATTING PERFORMANCE:\n" + "-" * 30 + "\n"
            for batsman in innings.get('batsman', []):
                result += f"{batsman.get('name', 'N/A')}: {batsman.get('runs', 0)} ({batsman.get('balls', 0)}b) - {batsman.get('outDec', 'Not Out')}\n"
            result += "\n" + "="*50 + "\n\n"
        return result

class MatchInfoTool(BaseTool):
    name: str = "Cricket Match Info Fetcher"
    description: str = "Fetches comprehensive match information like series, venue, toss, and officials."
    args_schema: Type[BaseModel] = CricketAPIInput

    def _run(self, match_id: str) -> str:
        url = "https://unofficial-cricbuzz.p.rapidapi.com/matches/get-info"
        querystring = {"matchId": match_id}
        headers = {
            "X-RapidAPI-Host": "unofficial-cricbuzz.p.rapidapi.com",
            "X-RapidAPI-Key": "0251d0e808mshf2b38142969493ap110abajsnd14d99bb9cf3"
        }
        try:
            response = requests.get(url, headers=headers, params=querystring)
            if response.status_code == 200:
                return self._format_match_info(response.json())
            return f"❌ Failed to fetch match info. Status code: {response.status_code}"
        except Exception as e:
            return f"❌ Error fetching match info: {str(e)}"
            
    def _format_match_info(self, data: Dict[Any, Any]) -> str:
        result = "📋 MATCH INFORMATION\n" + "="*40 + "\n\n"
        result += f"Series: {data.get('seriesName', 'N/A')}\n"
        result += f"Match: {data.get('matchDesc', 'N/A')}\n"
        result += f"Venue: {data.get('venueInfo', {}).get('ground', 'N/A')}\n"
        result += f"Toss: {data.get('toss', 'N/A')}\n"
        return result

class HighlightsTool(BaseTool):
    name: str = "Cricket Highlights Fetcher"
    description: str = "Fetches key highlights and important moments from the match commentary."
    args_schema: Type[BaseModel] = CricketAPIInput

    def _run(self, match_id: str) -> str:
        url = "https://unofficial-cricbuzz.p.rapidapi.com/matches/get-highlights"
        querystring = {"matchId": match_id}
        headers = {
            "X-RapidAPI-Host": "unofficial-cricbuzz.p.rapidapi.com",
            "X-RapidAPI-Key": "0251d0e808mshf2b38142969493ap110abajsnd14d99bb9cf3"
        }
        try:
            response = requests.get(url, headers=headers, params=querystring)
            if response.status_code == 200:
                return self._format_highlights(response.json())
            return f"❌ Failed to fetch highlights. Status code: {response.status_code}"
        except Exception as e:
            return f"❌ Error fetching highlights: {str(e)}"
    
    def _format_highlights(self, data: Dict[Any, Any]) -> str:
        result = "⚡ MATCH HIGHLIGHTS\n" + "="*40 + "\n\n"
        for i, event in enumerate(data.get("commentaryLines", []), 1):
            commentary = event.get("commentary", {})
            text = commentary.get("commtxt", "")
            if text:
                result += f"{i}. Over {commentary.get('overNum', '')}: {text}\n"
        return result

class CommentaryTool(BaseTool):
    name: str = "Cricket Commentary Fetcher"
    description: str = "Fetches ball-by-ball commentary for the entire match."
    args_schema: Type[BaseModel] = CricketAPIInput

    def _run(self, match_id: str) -> str:
        url = "https://unofficial-cricbuzz.p.rapidapi.com/matches/get-commentaries"
        querystring = {"matchId": match_id}
        headers = {
            "X-RapidAPI-Host": "unofficial-cricbuzz.p.rapidapi.com",
            "X-RapidAPI-Key": "0251d0e808mshf2b38142969493ap110abajsnd14d99bb9cf3"
        }
        try:
            response = requests.get(url, headers=headers, params=querystring)
            if response.status_code == 200:
                return self._format_commentary(response.json())
            return f"❌ Failed to fetch commentary. Status code: {response.status_code}"
        except Exception as e:
            return f"❌ Error fetching commentary: {str(e)}"
            
    def _format_commentary(self, data: Dict[Any, Any]) -> str:
        result = "🎤 MATCH COMMENTARY\n" + "="*40 + "\n\n"
        current_over = None
        for line in data.get('commentaryLines', []):
            commentary = line.get('commentary', {})
            commtxt = commentary.get('commtxt', '').strip()
            if commtxt:
                over_num = commentary.get('overNum', '')
                if over_num and over_num != current_over:
                    result += f"\n--- OVER {over_num} ---\n"
                    current_over = over_num
                result += f"[{commentary.get('eventType', '')}] {commtxt}\n"
        return result