#!/usr/bin/env python3
"""
Setup script for Live Weather App
This script helps users install dependencies and configure the application.
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required Python packages."""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies. Please install manually:")
        print("   pip install requests")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 6):
        print("❌ Python 3.6 or higher is required.")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version {sys.version.split()[0]} is compatible.")
    return True

def setup_api_key():
    """Guide user through API key setup."""
    print("\n🔑 OpenWeatherMap API Key Setup")
    print("=" * 40)
    print("1. Visit https://openweathermap.org/")
    print("2. Sign up for a free account")
    print("3. Go to your profile → API keys")
    print("4. Copy your API key")
    print("5. Open weather_app.py and replace 'YOUR_API_KEY_HERE' with your key")
    print("\n💡 The API key is free and allows 60 calls per minute.")

def main():
    """Main setup function."""
    print("🌤️ Live Weather App Setup")
    print("=" * 30)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Setup API key
    setup_api_key()
    
    print("\n🎉 Setup complete!")
    print("Run the app with: python weather_app.py")
    print("\n📖 For more information, see README.md")

if __name__ == "__main__":
    main() 