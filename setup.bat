@echo off
echo ========================================
echo     RaspFileSend Setup Script
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

echo Python found!
echo.

echo Installing required packages...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install packages
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo.
echo Packages installed successfully!
echo.

echo Starting configuration tool...
python raspfilesend_config.py

echo.
echo Setup complete! You can now:
echo 1. Configure your Raspberry Pi connection settings
echo 2. Install the Send To menu integration
echo 3. Start sending files by right-clicking them!
echo.
pause
