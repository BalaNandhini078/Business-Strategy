@echo off
REM AI-Powered Business Idea Generator - Run Script for Windows

echo.
echo 🚀 Starting AI-Powered Business Idea Generator...
echo.

REM Check if GOOGLE_API_KEY is set
if "%GOOGLE_API_KEY%"=="" (
    echo ⚠️  Warning: GOOGLE_API_KEY environment variable is not set!
    echo Please set it using:
    echo   set GOOGLE_API_KEY=your-api-key-here
    echo.
    set /p continue="Do you want to continue anyway? (y/n): "
    if /i not "%continue%"=="y" exit /b 1
)

echo.
echo 📦 Checking requirements...
pip install -r requirements.txt

echo.
echo ✅ Starting Streamlit application...
echo 🌐 The app will open in your browser automatically
echo.

REM Run the Streamlit app
streamlit run app.py

pause
