@echo off
setlocal
title Stop Rainfall AI Predictor Server

echo ===================================================
echo     Stopping Rainfall AI Predictor Server
echo ===================================================
echo.

cd /d "%~dp0"

where python >nul 2>&1
if %errorlevel% equ 0 (
    python stop_server.py
) else (
    if exist "venv\Scripts\python.exe" (
        venv\Scripts\python.exe stop_server.py
    ) else (
        echo [ERROR] Python not found to terminate server.
    )
)

echo.
pause
