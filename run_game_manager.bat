@echo off
title Game Manager - GOG Galaxy Collection
echo.
echo [STARTING] Game Manager...
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

REM Check if the script exists
if not exist "game_manager.py" (
    echo [ERROR] game_manager.py not found
    echo Make sure you're in the correct directory
    echo.
    pause
    exit /b 1
)

echo [OK] All checks passed - starting Game Manager
echo.

REM Run the Game Manager
python game_manager.py

REM Pause if there was an error
if errorlevel 1 (
    echo.
    echo [ERROR] Something went wrong
    pause
) 