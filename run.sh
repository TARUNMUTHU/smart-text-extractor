#!/bin/bash

echo "========================================"
echo "Starting Smart Handwritten Text Extractor"
echo "========================================"
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "ERROR: Virtual environment not found!"
    echo "Please run setup.sh first"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Start the application
echo
echo "Starting server..."
echo "The application will be available at: http://localhost:8000"
echo
echo "Press Ctrl+C to stop the server"
echo

python app.py
