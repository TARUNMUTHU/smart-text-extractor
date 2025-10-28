@echo off
echo ========================================
echo Quick Fix - Reinstalling Dependencies
echo ========================================
echo.
echo Smart Handwritten Text Extractor v2.1
echo Now supports IMAGE files only (No PDF/Poppler needed!)
echo.
echo This will install all required packages
echo.

:: Activate virtual environment
call venv\Scripts\activate.bat

echo.
echo [1/7] Upgrading pip and build tools...
python -m pip install --upgrade pip setuptools wheel

echo.
echo [2/7] Installing core web dependencies...
pip install fastapi "uvicorn[standard]" python-multipart aiofiles Jinja2

echo.
echo [3/7] Installing image processing libraries...
echo (No Poppler needed - direct image support!)
pip install Pillow opencv-python

echo.
echo [4/7] Installing numpy (may take a moment)...
pip install "numpy<2.3" --only-binary :all:

echo.
echo [5/7] Installing EasyOCR (basic OCR engine)...
echo (This will download ~400MB of models on first use)
pip install easyocr

echo.
echo [6/7] Installing text processing...
pip install textblob python-docx

echo.
echo Downloading TextBlob corpora...
python -m textblob.download_corpora

echo.
echo [7/7] Installing optional advanced features...
echo.
set /p INSTALL_GOOGLE="Install Google Vision API support? (y/n): "

if /i "%INSTALL_GOOGLE%"=="y" (
    echo Installing Google Cloud Vision...
    pip install google-cloud-vision
    echo Google Vision API support installed!
) else (
    echo Skipping Google Vision API.
    echo You can install it later with: pip install google-cloud-vision
)

echo.
set /p INSTALL_GEMINI="Install Google Gemini API for answer evaluation? (y/n): "

if /i "%INSTALL_GEMINI%"=="y" (
    echo Installing Google Generative AI (Gemini)...
    pip install google-generativeai
    echo Gemini API support installed!
    echo.
    echo IMPORTANT: Set your Gemini API key as environment variable:
    echo   set GEMINI_API_KEY=your_api_key_here
    echo.
    echo Get your API key from: https://makersuite.google.com/app/apikey
) else (
    echo Skipping Gemini API.
    echo You can install it later with: pip install google-generativeai
)

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Installed OCR Engines:
echo   ✓ EasyOCR (always installed)
if /i "%INSTALL_GOOGLE%"=="y" (
    echo   ✓ Google Vision API
) else (
    echo   ✗ Google Vision API (not installed)
)
echo.
echo Answer Evaluation:
if /i "%INSTALL_GEMINI%"=="y" (
    echo   ✓ Gemini AI (installed - configure API key)
) else (
    echo   ✗ Gemini AI (not installed)
)
echo.
echo To start the application:
echo   run.bat
echo.
echo Then open: http://localhost:8000
echo.
pause
