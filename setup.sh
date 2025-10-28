#!/bin/bash

echo "========================================"
echo "Smart Handwritten Text Extractor Setup"
echo "========================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "[1/5] Checking Python version..."
python3 --version

echo
echo "[2/5] Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists, skipping..."
else
    python3 -m venv venv
    echo "Virtual environment created successfully"
fi

echo
echo "[3/5] Activating virtual environment..."
source venv/bin/activate

echo
echo "[4/5] Installing dependencies..."
echo "This may take several minutes..."
pip install --upgrade pip
pip install -r requirements.txt

echo
echo "[5/5] Downloading TextBlob corpora..."
python -m textblob.download_corpora

echo
echo "========================================"
echo "Setup completed successfully!"
echo "========================================"
echo
echo "IMPORTANT: Before running the app, make sure:"
echo "  1. Poppler is installed"
echo "     macOS: brew install poppler"
echo "     Linux: sudo apt-get install poppler-utils"
echo
echo "  2. (Optional) For Google Vision API, set:"
echo "     export GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json"
echo
echo "To start the application:"
echo "  1. Run: ./run.sh"
echo "  2. Or manually: source venv/bin/activate && python app.py"
echo
