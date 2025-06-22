#!/usr/bin/env python3
"""
Setup script for Claude Startup Insights Bot
"""

import os
import sys

def create_env_file():
    """Create .env file with user input."""
    print("🤖 Claude Startup Insights Bot Setup")
    print("=" * 50)
    
    api_key = input("Enter your Anthropic API key: ").strip()
    
    if not api_key:
        print("❌ API key is required!")
        return False
    
    env_content = f"""# Anthropic API Configuration
ANTHROPIC_API_KEY={api_key}

# Optional: Customize Claude model (default: claude-3-5-sonnet-20241022)
# CLAUDE_MODEL=claude-3-5-sonnet-20241022
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def check_dependencies():
    """Check if required packages are installed."""
    print("\n📦 Checking dependencies...")
    
    required_packages = [
        'streamlit',
        'anthropic', 
        'pandas',
        'numpy',
        'plotly',
        'python-dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - not installed")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📥 Installing missing packages: {', '.join(missing_packages)}")
        os.system(f"pip install {' '.join(missing_packages)}")
    else:
        print("✅ All dependencies are installed!")

def main():
    """Main setup function."""
    print("🚀 Welcome to Claude Startup Insights Bot Setup!")
    
    # Check if .env already exists
    if os.path.exists('.env'):
        overwrite = input("⚠️  .env file already exists. Overwrite? (y/N): ").strip().lower()
        if overwrite != 'y':
            print("Setup cancelled.")
            return
    
    # Create .env file
    if not create_env_file():
        return
    
    # Check dependencies
    check_dependencies()
    
    print("\n🎉 Setup complete!")
    print("\n📋 Next steps:")
    print("1. Run: streamlit run app.py")
    print("2. Open your browser to: http://localhost:8501")
    print("3. Start analyzing startup data with Claude!")
    
    print("\n💡 Tips:")
    print("- Get your Anthropic API key from: https://console.anthropic.com/")
    print("- The app includes sample data to get you started")
    print("- Check the README.md for detailed usage instructions")

if __name__ == "__main__":
    main() 
