@echo off
title Refresh Games from GOG Galaxy
echo.
echo [REFRESH] Refreshing game collection from GOG Galaxy...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.x and try again
    echo.
    pause
    exit /b 1
)

REM Check if the Galaxy export script exists
if not exist "galaxy_library_export.py" (
    echo [ERROR] galaxy_library_export.py not found in current directory
    echo Please make sure you have the Galaxy export script
    echo.
    pause
    exit /b 1
)

REM Create backup of existing gameDB.csv if it exists
if exist "gameDB.csv" (
    echo [BACKUP] Creating backup of current gameDB.csv...
    copy "gameDB.csv" "gameDB_backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%.csv" >nul 2>&1
)

echo [RUNNING] Running Galaxy export script...
echo This may take a moment...
echo.

REM Run the Galaxy export script
python galaxy_library_export.py

REM Check if it was successful
if errorlevel 1 (
    echo.
    echo [ERROR] Galaxy export failed
    echo Please check the error messages above
    pause
    exit /b 1
) else (
    echo.
    echo [OK] Galaxy export completed successfully!
    echo [INFO] Your gameDB.csv has been updated with the latest games
    echo.
    echo You can now run Game Manager to pick from your updated collection
    echo.
    timeout /t 5 /nobreak >nul
) 