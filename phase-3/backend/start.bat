@echo off
REM Phase 3 Backend Startup Script
REM This script starts the FastAPI backend with Gemini API integration

echo ========================================
echo Phase 3: AI-Powered Todo Chatbot
echo Backend Server with Google Gemini API
echo ========================================
echo.

REM Change to backend directory
cd /d "%~dp0"

REM Check if .env file exists
if not exist .env (
    echo ERROR: .env file not found!
    echo Please create .env file with GEMINI_API_KEY
    echo.
    pause
    exit /b 1
)

REM Load environment variables
for /f "tokens=1,2 delims==" %%a in (.env) do (
    if not "%%a"=="" if not "%%b"=="" (
        set %%a=%%b
    )
)

REM Check if GEMINI_API_KEY is set
if "%GEMINI_API_KEY%"=="" (
    echo ERROR: GEMINI_API_KEY not set in .env file!
    echo.
    echo Please add your Gemini API key to .env:
    echo GEMINI_API_KEY=your-api-key-here
    echo.
    echo Get a FREE API key from: https://makersuite.google.com/app/apikey
    echo.
    pause
    exit /b 1
)

echo ✓ Environment variables loaded
echo ✓ Gemini API Key: %GEMINI_API_KEY:~0,20%...
echo.

REM Check if dependencies are installed
python -c "import google.generativeai" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install google-generativeai fastapi uvicorn python-dotenv
    echo.
)

echo Starting backend server...
echo.
echo Server will be available at:
echo   - Local:   http://localhost:8001
echo   - Network: http://0.0.0.0:8001
echo.
echo API Documentation:
echo   - Swagger UI: http://localhost:8001/docs
echo   - ReDoc:      http://localhost:8001/redoc
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

REM Start the server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8001
