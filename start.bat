@echo off
cd /d "%~dp0"

echo ========================================================
echo   CLEANING UP OLD PROCESSES
echo ========================================================
echo Closing any open Python/Streamlit windows to free up port 8501...
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM cloudflared.exe >nul 2>&1
timeout /t 2 /nobreak >nul

:: --- Configuration ---
set PORT=8501

echo.
echo ========================================================
echo   STARTING NEW SESSION
echo ========================================================

:: 1. Start Streamlit in a HIDDEN window so this script can continue
echo Launching Streamlit on port %PORT%...
start "Streamlit App" /min cmd /c "python -m streamlit run app.py --server.port %PORT%"

:: 2. Wait for Streamlit to wake up
echo Waiting 5 seconds for app to initialize...
timeout /t 5 /nobreak >nul

echo.
echo ========================================================
echo   OPENING PUBLIC TUNNEL
echo ========================================================
echo.
echo Looking for cloudflared.exe...

if exist "cloudflared.exe" (
    echo Found cloudflared! Starting tunnel...
    echo.
    echo -----------------------------------------------------------
    echo   COPY THE LINK BELOW (ending in .trycloudflare.com)
    echo -----------------------------------------------------------
    echo.
    :: Run the tunnel connecting to port 8501
    cloudflared.exe tunnel --url http://localhost:%PORT%
) else (
    echo.
    echo [ERROR] cloudflared.exe not found!
    echo Please download it, rename it to 'cloudflared.exe'
    echo and put it in this folder: %~dp0
    pause
)