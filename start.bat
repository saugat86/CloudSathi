@echo off
REM CloudSathi Startup Script for Windows
REM This script starts both the backend and frontend servers

echo.
echo ==========================================
echo   Starting CloudSathi Application
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed. Please install Node.js 16 or higher.
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist "backend\.env" (
    echo Creating .env file from template...
    copy "backend\.env.example" "backend\.env"
    echo Created backend\.env - Using mock data mode
)

echo.
echo Starting Backend Server (Port 8000)...
start "CloudSathi Backend" cmd /k "cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"

echo Waiting for backend to start...
timeout /t 3 /nobreak >nul

echo.
echo Starting Frontend Server (Port 3000)...
start "CloudSathi Frontend" cmd /k "cd frontend && npm start"

echo.
echo ==========================================
echo   CloudSathi is now running!
echo ==========================================
echo.
echo Frontend:      http://localhost:3000
echo Backend API:   http://localhost:8000
echo API Docs:      http://localhost:8000/docs
echo Health Check:  http://localhost:8000/health
echo.
echo Close the terminal windows to stop the servers.
echo.
pause
