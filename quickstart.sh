#!/bin/bash
# Quick start script for Hotel Content Automation

set -e

echo "=========================================="
echo "Hotel Content Automation - Quick Start"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version || { echo "Error: Python 3 not found"; exit 1; }

# Check if .env exists
if [ ! -f .env ]; then
    echo ""
    echo "⚠️  .env file not found!"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "✅ Created .env file"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and fill in your API keys and configuration"
    echo "   - OPENAI_API_KEY"
    echo "   - GOOGLE_SERVICE_ACCOUNT_FILE"
    echo "   - TELEGRAM_BOT_TOKEN"
    echo ""
    read -p "Press Enter after you've configured .env to continue..."
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate || . venv/bin/activate

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Dependencies installed"

# Check FFmpeg
echo ""
echo "Checking FFmpeg..."
if command -v ffmpeg &> /dev/null; then
    echo "✅ FFmpeg is installed"
    ffmpeg -version | head -1
else
    echo "⚠️  FFmpeg not found!"
    echo "Please install FFmpeg:"
    echo "  - Ubuntu/Debian: sudo apt install ffmpeg"
    echo "  - macOS: brew install ffmpeg"
    echo "  - Windows: Download from https://ffmpeg.org"
    echo ""
    read -p "Press Enter after installing FFmpeg to continue..."
fi

# Run structure test
echo ""
echo "Running structure verification..."
python3 test_structure.py

echo ""
echo "=========================================="
echo "✅ Setup complete!"
echo "=========================================="
echo ""
echo "To run the automation:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run: python main.py"
echo ""
echo "For detailed setup instructions, see setup.md"
echo ""
