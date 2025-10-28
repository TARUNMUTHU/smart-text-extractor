@echo off
echo ========================================
echo Smart Handwritten Text Extractor Setup
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo [1/5] Checking Python version...
python --version

echo.
echo [2/5] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists, skipping...
) else (
    python -m venv venv
    echo Virtual environment created successfully
)

echo.
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [4/5] Installing dependencies...
echo This may take several minutes...
python -m pip install --upgrade pip
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

echo.
echo [5/5] Downloading TextBlob corpora...
python -m textblob.download_corpora

echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo IMPORTANT: Before running the app, make sure:
echo   1. Poppler is installed and in your PATH
echo      Download from: https://github.com/oschwartz10612/poppler-windows/releases/
echo.
echo   2. (Optional) For Google Vision API, set:
echo      set GOOGLE_APPLICATION_CREDENTIALS=path\to\credentials.json
echo.
echo To start the application:
echo   1. Run: run.bat
echo   2. Or manually: venv\Scripts\activate ^&^& python app.py
echo.
pause
