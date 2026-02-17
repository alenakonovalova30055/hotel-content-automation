@echo off
REM Quick start script for Hotel Content Automation (Windows)

echo ==========================================
echo Hotel Content Automation - Quick Start
echo ==========================================
echo.

REM Check Python version
echo Checking Python version...
python --version 2>nul || (
    echo Error: Python not found
    echo Please install Python 3.10 or higher from https://www.python.org
    pause
    exit /b 1
)

REM Check if .env exists
if not exist .env (
    echo.
    echo WARNING: .env file not found!
    echo Creating .env from .env.example...
    copy .env.example .env
    echo Created .env file
    echo.
    echo IMPORTANT: Please edit .env and fill in your API keys and configuration
    echo    - OPENAI_API_KEY
    echo    - GOOGLE_SERVICE_ACCOUNT_FILE
    echo    - TELEGRAM_BOT_TOKEN
    echo.
    pause
)

REM Check if virtual environment exists
if not exist venv (
    echo.
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo Dependencies installed

REM Check FFmpeg
echo.
echo Checking FFmpeg...
ffmpeg -version >nul 2>&1
if %errorlevel% equ 0 (
    echo FFmpeg is installed
    ffmpeg -version | findstr /C:"version"
) else (
    echo WARNING: FFmpeg not found!
    echo Please install FFmpeg:
    echo   - Download from https://ffmpeg.org
    echo   - Extract and add to PATH
    echo.
    pause
)

REM Run structure test
echo.
echo Running structure verification...
python test_structure.py

echo.
echo ==========================================
echo Setup complete!
echo ==========================================
echo.
echo To run the automation:
echo   1. Activate virtual environment: venv\Scripts\activate
echo   2. Run: python main.py
echo.
echo For detailed setup instructions, see setup.md
echo.
pause
