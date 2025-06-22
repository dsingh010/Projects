#!/usr/bin/env python3
"""
Quick start script for Claude Startup Insights Bot
"""

import os
import sys
import subprocess

def check_env():
    """Check if .env file exists and has API key."""
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("Please run: python setup.py")
        return False
    
    with open('.env', 'r') as f:
        content = f.read()
        if 'ANTHROPIC_API_KEY=your_anthropic_api_key_here' in content:
            print("❌ Please set your actual Anthropic API key in .env file")
            return False
    
    return True

def check_dependencies():
    """Check if required packages are installed."""
    try:
        import streamlit
        import anthropic
        import pandas
        import plotly
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def main():
    """Main function to run the application."""
    print("🚀 Starting Claude Startup Insights Bot...")
    
    # Check environment
    if not check_env():
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    print("✅ All checks passed!")
    print("🌐 Starting Streamlit app...")
    print("📱 The app will open in your browser at: http://localhost:8501")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Run streamlit
        subprocess.run(["streamlit", "run", "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Thanks for using Claude Startup Insights Bot!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running Streamlit: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
