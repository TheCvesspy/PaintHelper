@echo off
echo Stopping MiniPaint Tracker...

:: Kill processes on port 3000 (Frontend)
for /f "tokens=5" %%a in ('netstat -aon ^| find ":3000" ^| find "LISTENING"') do (
    echo Killing Frontend process PID %%a...
    taskkill /f /pid %%a >nul 2>&1
)

:: Kill processes on ports 8000-8020 (Backend - wider range to catch all orphaned processes)
for /L %%i in (8000,1,8020) do (
    for /f "tokens=5" %%a in ('netstat -aon ^| find ":%%i" ^| find "LISTENING"') do (
        echo Killing Backend process on port %%i PID %%a...
        taskkill /f /pid %%a >nul 2>&1
    )
)

:: Fallback: Kill any remaining Python processes (Reflex workers)
echo Killing any remaining Python processes...
taskkill /f /im python.exe >nul 2>&1

echo.
echo MiniPaint Tracker has been stopped.
pause
