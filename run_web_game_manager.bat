@echo off
title Game Manager Web - GOG Galaxy Collection
echo.
echo [STARTING] Web Game Manager...
echo.

REM Simple Python check
echo [INFO] Checking Python...
python -c "print('Python OK')" 2>nul
if errorlevel 1 (
    echo [ERROR] Python is not installed or not available
    echo Please install Python 3.x and add it to your PATH
    echo.
    pause
    exit /b 1
)

REM Check if the web script exists
if not exist "web_game_manager.py" (
    echo [ERROR] web_game_manager.py not found
    echo Make sure you're in the correct directory
    echo.
    pause
    exit /b 1
)

REM Check if Flask is installed
echo [INFO] Checking Flask installation...
python -c "import flask; print('Flask OK')" 2>nul
if errorlevel 1 (
    echo [INFO] Flask not found. Installing dependencies...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        echo Please install Flask manually: pip install flask
        echo.
        pause
        exit /b 1
    )
)

echo [OK] All checks passed - starting Web Game Manager
echo.
echo [INFO] Web interface will be available at:
echo         http://localhost:5000
echo.
echo [INFO] Starting server and opening browser...
echo [INFO] Press Ctrl+C to stop the server
echo.

REM Start the Web Game Manager in background and open browser
start /b python web_game_manager.py

REM Wait a moment for the server to start
timeout /t 3 /nobreak >nul

REM Open the web page in default browser
start http://localhost:5000

REM Keep the window open and wait for the server
echo [INFO] Server is running. Close this window or press Ctrl+C to stop.
pause >nul 