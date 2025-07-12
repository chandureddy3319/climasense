@echo off
echo 🌤️ Live Weather App Launcher
echo ============================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.6 or higher from https://python.org
    pause
    exit /b 1
)

REM Check if weather_app.py exists
if not exist "weather_app.py" (
    echo ❌ weather_app.py not found
    echo Please make sure you're in the correct directory
    pause
    exit /b 1
)

REM Check if requests module is installed
python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Requests module not found. Installing...
    pip install requests
    if errorlevel 1 (
        echo ❌ Failed to install requests module
        pause
        exit /b 1
    )
)

echo ✅ Starting Live Weather App...
echo.
python weather_app.py

pause 