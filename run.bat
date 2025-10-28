@echo off
echo ========================================
echo Starting Smart Handwritten Text Extractor
echo ========================================
echo.

:: Check if virtual environment exists
if not exist venv (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first
    pause
    exit /b 1
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Start the application
echo.
echo Starting server...
echo The application will be available at: http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py
