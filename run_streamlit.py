#!/usr/bin/env python3
"""
Simple script to run the Streamlit app for Cricket Match Analysis
"""
import subprocess
import sys
import os

def main():
    """Run the Streamlit app"""
    try:
        # Change to the project directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        print("🏏 Starting Cricket Match Analysis Streamlit App...")
        print("📍 Project directory:", os.getcwd())
        print("🌐 The app will open in your browser at: http://localhost:8501")
        print("⏹️  Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.address", "localhost",
            "--server.port", "8501"
        ])
        
    except KeyboardInterrupt:
        print("\n👋 Streamlit app stopped")
    except Exception as e:
        print(f"❌ Error starting Streamlit app: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()