import streamlit as st
import sys
import os
from pathlib import Path
import logging
from datetime import datetime
import traceback

# SQLite fix for ChromaDB on Streamlit Cloud - MUST BE FIRST
try:
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    # Try environment variable approach
    os.environ['CHROMA_DB_IMPL'] = 'duckdb'
    os.environ['ANONYMIZED_TELEMETRY'] = 'False'

# Add the src directory to Python path
sys.path.append(str(Path(__file__).parent / "src"))

from src.hello_world.main import run

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def format_cricket_analysis(text):
    """Format cricket analysis output - Ultimate Match Digest first, then everything else"""
    
    # First, find and display the Ultimate Match Digest section
    ultimate_digest_start = text.find("## 🚨 INDIA'S LEGENDARY OLD TRAFFORD ESCAPE")
    if ultimate_digest_start == -1:
        ultimate_digest_start = text.find("🚨 INDIA'S LEGENDARY OLD TRAFFORD ESCAPE")
    
    if ultimate_digest_start != -1:
        # Extract and display the Ultimate Match Digest section
        digest_content = text[ultimate_digest_start:]
        st.markdown(digest_content)
        st.markdown("---")  # Add separator
    
    # Then display everything else (before the Ultimate Match Digest)
    if ultimate_digest_start != -1:
        other_content = text[:ultimate_digest_start].strip()
    else:
        other_content = text
    
    if other_content:
        # Split the remaining content into sections
        sections = other_content.split('\n\n')
        
        for section in sections:
            if not section.strip():
                continue
                
            lines = section.strip().split('\n')
            if not lines:
                continue
                
            first_line = lines[0].strip()
            
            # Main title
            if "INDIA'S EPIC COMEBACK" in first_line or "EPIC COMEBACK DRAWS" in first_line:
                st.markdown(f"# {first_line}")
                continue
            
            # Skip duplicate GenZ summaries and tactical breakdown
            if ("30-WORD GENZ MATCH SUMMARY" in first_line or 
                "TACTICAL BREAKDOWN & TURNING POINTS" in first_line or
                "🧠 TACTICAL BREAKDOWN & TURNING POINTS" in first_line or
                "GenZ Match Summary" in first_line):
                continue
            
            # Major sections with double asterisks
            if first_line.startswith('**') and first_line.endswith('**'):
                section_title = first_line.strip('*')
                st.markdown(f"### **{section_title}**")
                
                # Process content under the section
                if len(lines) > 1:
                    content_lines = lines[1:]
                    process_section_content(content_lines, section_title)
                continue
            
            # Top highlights/performances sections
            if any(keyword in first_line for keyword in ['TOP 4 HIGHLIGHTS', 'TOP 3 BATTING', 'TOP 3 BOWLING']):
                st.markdown(f"### **{first_line}**")
                if len(lines) > 1:
                    process_highlights(lines[1:])
                continue
            
            # Partnerships section (12-word limit)
            if "PARTNERSHIPS THAT CHANGED EVERYTHING" in first_line or "🤝 PARTNERSHIPS THAT CHANGED EVERYTHING" in first_line:
                st.markdown(f"### **{first_line}**")
                if len(lines) > 1:
                    process_partnerships(lines[1:])
                continue
            
            # Fielding highlights section
            if "FIELDING HIGHLIGHTS" in first_line or "🎯 FIELDING HIGHLIGHTS" in first_line:
                st.markdown(f"### **{first_line}**")
                if len(lines) > 1:
                    process_fielding_highlights(lines[1:])
                continue
            
            # Statistical facts (10-word limit)
            if "FASCINATING STATISTICAL FACTS" in first_line or "📊 STATISTICAL DEEP DIVE" in first_line:
                st.markdown(f"### **{first_line}**")
                if len(lines) > 1:
                    process_statistical_facts(lines[1:])
                continue
            
            # Other sections
            if first_line and not first_line.startswith('-'):
                st.markdown(f"### **{first_line}**")
                if len(lines) > 1:
                    for line in lines[1:]:
                        if line.strip():
                            st.markdown(line.strip())

def process_section_content(lines, section_title):
    """Process content under major sections"""
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        if line.startswith('- **'):
            # Bullet points with bold headers
            st.markdown(line)
        elif line.startswith('**') and line.endswith('**'):
            # Bold subheadings
            st.markdown(f"#### {line}")
        else:
            st.markdown(line)

def process_highlights(lines):
    """Process top highlights/performances with 10-word limit"""
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        if line[0].isdigit() and '.' in line[:5]:
            # Extract title and description
            parts = line.split(':', 1)
            if len(parts) == 2:
                title = parts[0].strip()
                description = parts[1].strip()
                
                # Limit description to 10 words
                words = description.split()
                if len(words) > 10:
                    description = ' '.join(words[:10]) + '...'
                
                # Use container for better styling
                with st.container():
                    st.markdown(f"""
                    <div class="highlight-card">
                        <strong>{title}:</strong> {description}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown(f"**{line}**")
        else:
            st.markdown(line)

def process_partnerships(lines):
    """Process partnerships section with 12-word limit"""
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        if line.startswith('- '):
            # Extract title and description
            line_content = line[2:]  # Remove "- "
            parts = line_content.split(' - ', 1)
            if len(parts) == 2:
                title = parts[0].strip()
                description = parts[1].strip()
                
                # Limit description to 12 words
                words = description.split()
                if len(words) > 12:
                    description = ' '.join(words[:12]) + '...'
                
                st.markdown(f"""
                <div class="highlight-card">
                    <strong>🤝 {title}:</strong> {description}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"**{line_content}**")
        else:
            st.markdown(line)

def process_fielding_highlights(lines):
    """Process fielding highlights section"""
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        if line.startswith('- '):
            # Extract title and description
            line_content = line[2:]  # Remove "- "
            parts = line_content.split(' - ', 1)
            if len(parts) == 2:
                title = parts[0].strip()
                description = parts[1].strip()
                
                # Limit description to 10 words for consistency
                words = description.split()
                if len(words) > 10:
                    description = ' '.join(words[:10]) + '...'
                
                st.markdown(f"""
                <div class="highlight-card">
                    <strong>🎯 {title}:</strong> {description}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"**{line_content}**")
        else:
            st.markdown(line)

def process_statistical_facts(lines):
    """Process statistical facts section with 10-word limit"""
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        if line.startswith('- '):
            # Extract title and description
            line_content = line[2:]  # Remove "- "
            parts = line_content.split(' - ', 1)
            if len(parts) == 2:
                title = parts[0].strip()
                description = parts[1].strip()
                
                # Limit description to 10 words
                words = description.split()
                if len(words) > 10:
                    description = ' '.join(words[:10]) + '...'
                
                st.markdown(f"""
                <div class="stats-container">
                    <strong>📊 {title}:</strong><br>
                    {description}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"**{line_content}**")
        elif line[0].isdigit() and '.' in line[:5]:
            parts = line.split(':', 1)
            if len(parts) == 2:
                title = parts[0].strip()
                description = parts[1].strip()
                
                # Limit description to 10 words
                words = description.split()
                if len(words) > 10:
                    description = ' '.join(words[:10]) + '...'
                
                st.markdown(f"""
                <div class="stats-container">
                    <strong>📊 {title}:</strong><br>
                    {description}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"**{line}**")
        else:
            st.markdown(line)

# Configure Streamlit page
st.set_page_config(
    page_title="Field Manager's Cricket Intelligence Hub",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Header with logo and title
    col1, col2 = st.columns([1, 6])
    
    with col1:
        st.image("https://content.fieldsmanager.com/System.png", width=80)
    
    with col2:
        st.title("🏏 Field Manager's Cricket Intelligence Hub")
        st.markdown("**Powered by AI Agents • Comprehensive Match Analysis • Real-time Insights**")
    
    st.markdown("---")
    
    # Add custom CSS for better styling
    st.markdown("""
    <style>
    .stApp {
        padding-top: 2rem;
    }
    .main-header {
        font-size: 3rem !important;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        background: linear-gradient(90deg, #ff6b6b, #4ecdc4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
        margin: 1.5rem 0 1rem 0;
    }
    .highlight-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #4ecdc4;
        margin: 0.5rem 0;
    }
    .stats-container {
        background-color: #fff5f5;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar for inputs
    with st.sidebar:
        st.header("⚙️ Match Analysis Setup")
        
        # Important notice about Cricbuzz
        st.warning("⚠️ **IMPORTANT**: Use only Match IDs from **cricbuzz.com**")
        st.markdown("📌 **How to get Match ID from Cricbuzz:**")
        st.markdown("""
        1. Go to [cricbuzz.com](https://cricbuzz.com)
        2. Select any live or completed match
        3. Copy the **numbers** from the URL
        
        **Example:** 
        - URL: `cricbuzz.com/live-cricket-scores/105778/match-name`
        - Match ID: `105778`
        """)
        
        # Match ID input
        match_id = st.text_input(
            "🏏 Cricbuzz Match ID",
            value="105778",
            help="Enter the Match ID from cricbuzz.com URL",
            placeholder="e.g., 105778"
        )
        
        # Analysis button
        analyze_button = st.button("🚀 Generate Intelligence Report", type="primary")
        
        st.markdown("---")
        st.markdown("### 🤖 AI Analysis Engine")
        st.markdown(
            """
            **Field Manager's Intelligence System:**
            - 📊 **Data Analyst**: Extracts match statistics
            - 🎯 **Performance Analyst**: Identifies key moments  
            - 📝 **Content Strategist**: Creates engaging insights
            - 🏆 **Master Analyst**: Compiles comprehensive reports
            """
        )
    
    # Main content area - full width
    if analyze_button and match_id:
        if not match_id.strip():
            st.error("Please enter a valid Match ID")
            return
        
        # Show loading spinner with Field Manager branding
        with st.spinner("🤖 Field Manager's AI Agents analyzing match data..."):
            try:
                # Run the CrewAI analysis
                result = run(match_id)
                
                # Display results
                if result:
                    # Get the result text
                    if hasattr(result, 'raw'):
                        result_text = result.raw
                    else:
                        result_text = str(result)
                    
                    # Format and display the cricket analysis
                    format_cricket_analysis(result_text)
                    
                    # Download button for results
                    st.download_button(
                        label="📥 Download Intelligence Report",
                        data=result_text,
                        file_name=f"field_managers_cricket_analysis_{match_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )
                
            except Exception as e:
                st.error(f"An error occurred during analysis: {str(e)}")
                
                with st.expander("🔍 Error Details"):
                    st.code(traceback.format_exc())
                
                logger.error(f"Analysis failed for match {match_id}: {str(e)}")
    
    elif not match_id:
        st.info("👈 Please enter a **Cricbuzz Match ID** in the sidebar to start analysis")
        
        # Add instructions in main area when no analysis is running
        st.markdown("### 🎯 Welcome to Field Manager's Cricket Intelligence Hub")
        st.markdown("""
        Get **comprehensive AI-powered cricket match analysis** in seconds!
        
        **📋 What you'll get:**
        - 🏆 **Ultimate Match Digest** - Complete match overview with key statistics
        - ⭐ **Top Highlights** - Most important moments and performances  
        - 📊 **Performance Analysis** - Detailed batting, bowling, and fielding insights
        - 🤝 **Partnership Analysis** - Critical partnerships that shaped the match
        - 📈 **Statistical Deep Dive** - Fascinating facts and records
        - 🎭 **Match Narrative** - Complete story of how the match unfolded
        
        **🚀 Simply enter a Cricbuzz Match ID and click 'Generate Intelligence Report'!**
        """)
        
    else:
        st.info("👆 Click the 'Generate Intelligence Report' button to begin analysis")

if __name__ == "__main__":
    main()