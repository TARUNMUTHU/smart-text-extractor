@echo off
echo ========================================
echo Starting Smart Handwritten Text Extractor
echo With Gemini AI Evaluation Enabled
echo ========================================
echo.

REM Set Gemini API Key
set GEMINI_API_KEY=AIzaSyBJOXfQC06cnu_MwBzcH_AMAmJGEdhb-yM

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Starting server with AI evaluation enabled...
echo The application will be available at: http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py
