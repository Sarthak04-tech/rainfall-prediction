@echo off
title Rainfall AI Predictor - Server Launcher

echo ===================================================
echo     Rainfall AI Predictor - One-Click Launcher
echo ===================================================
echo.

:: 1. Navigate to project root directory
cd /d "%~dp0"

:: 2. Check Python installation
echo [*] Checking Python installation...
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not found in system PATH.
    echo Please install Python 3.8 or higher from https://www.python.org/
    echo Make sure to check the option "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%v in ('python --version 2^>^&1') do (
    echo [OK] Found %%v
)

:: 3. Check essential project files
echo [*] Verifying essential project files...
if not exist "app.py" (
    echo [ERROR] Missing app.py in project folder.
    pause
    exit /b 1
)

if not exist "model_unzipped\rainfall_model.pkl" (
    echo [WARNING] Model file not found at model_unzipped\rainfall_model.pkl.
    if exist "rainfall_model.zip" (
        echo [*] Extracting rainfall_model.zip...
        powershell -Command "Expand-Archive -Path 'rainfall_model.zip' -DestinationPath 'model_unzipped' -Force"
    )
)

if not exist "model_unzipped\rainfall_model.pkl" (
    echo [ERROR] Model file missing.
    pause
    exit /b 1
)

:: 4. Virtual environment setup / selection
set "PYTHON_EXE=python"
if exist "venv\Scripts\python.exe" (
    set "PYTHON_EXE=venv\Scripts\python.exe"
) else (
    echo [*] Setting up virtual environment...
    python -m venv venv
    if exist "venv\Scripts\python.exe" (
        set "PYTHON_EXE=venv\Scripts\python.exe"
        echo [OK] Virtual environment created.
    ) else (
        echo [INFO] Continuing with system Python.
    )
)

:: 5. Install / Verify dependencies
echo [*] Checking required dependencies...
"%PYTHON_EXE%" -m pip install -r requirements.txt --quiet

:: 6. Terminate any previous instance on port 5000
"%PYTHON_EXE%" stop_server.py >nul 2>&1

:: 7. Start application and open browser
echo.
echo ===================================================
echo  Starting server at http://127.0.0.1:5000
echo  Press Ctrl+C or run STOP.bat to close the app.
echo ===================================================
echo.

:: Automatically launch browser after 2 seconds
start "" powershell -Command "Start-Sleep -Seconds 2; Start-Process 'http://127.0.0.1:5000'"

:: Launch application
"%PYTHON_EXE%" app.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Application stopped unexpectedly with code %errorlevel%.
    pause
)
