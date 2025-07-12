#!/usr/bin/env python3
"""
Test script for Live Weather App
This script verifies that all dependencies are installed and the app can run.
"""

import sys
import importlib

def test_imports():
    """Test if all required modules can be imported."""
    print("🔍 Testing module imports...")
    
    required_modules = [
        ('tkinter', 'Tkinter GUI framework'),
        ('requests', 'HTTP requests library'),
        ('json', 'JSON parsing'),
        ('threading', 'Threading support'),
        ('datetime', 'Date and time utilities')
    ]
    
    all_good = True
    
    for module_name, description in required_modules:
        try:
            importlib.import_module(module_name)
            print(f"✅ {module_name} - {description}")
        except ImportError as e:
            print(f"❌ {module_name} - {description}")
            print(f"   Error: {e}")
            all_good = False
    
    return all_good

def test_api_key():
    """Check if API key is configured."""
    print("\n🔑 Testing API key configuration...")
    
    try:
        with open('weather_app.py', 'r') as f:
            content = f.read()
            
        if 'YOUR_API_KEY_HERE' in content:
            print("⚠️  API key not configured")
            print("   Please replace 'YOUR_API_KEY_HERE' with your actual API key")
            return False
        else:
            print("✅ API key appears to be configured")
            return True
    except FileNotFoundError:
        print("❌ weather_app.py not found")
        return False

def test_gui_creation():
    """Test if Tkinter GUI can be created."""
    print("\n🖥️  Testing GUI creation...")
    
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Hide the window
        root.destroy()
        print("✅ GUI can be created successfully")
        return True
    except Exception as e:
        print(f"❌ GUI creation failed: {e}")
        return False

def main():
    """Main test function."""
    print("🧪 Live Weather App - Installation Test")
    print("=" * 40)
    
    # Test Python version
    print(f"🐍 Python version: {sys.version.split()[0]}")
    if sys.version_info < (3, 6):
        print("❌ Python 3.6 or higher is required")
        return False
    else:
        print("✅ Python version is compatible")
    
    # Test imports
    imports_ok = test_imports()
    
    # Test API key
    api_key_ok = test_api_key()
    
    # Test GUI
    gui_ok = test_gui_creation()
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 20)
    
    if imports_ok and gui_ok:
        print("✅ All tests passed!")
        print("🎉 Your Live Weather App is ready to run!")
        print("\nTo start the app:")
        print("   python weather_app.py")
        
        if not api_key_ok:
            print("\n⚠️  Remember to configure your API key first!")
        
        return True
    else:
        print("❌ Some tests failed")
        print("\nTo fix issues:")
        print("1. Install missing dependencies: pip install requests")
        print("2. Configure API key in weather_app.py")
        print("3. Ensure Python 3.6+ is installed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 