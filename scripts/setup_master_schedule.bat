@echo off
title 24/7 Master Lead Scraper & CRM Sync Scheduler
echo ===============================================================================
echo   CONFIGURING 24/7 AUTOMATED SCHEDULE FOR SCRAPERS & ZOHO CRM SYNC
echo ===============================================================================
echo.

set PYTHON_EXE=C:\Python312\python.exe
if not exist "%PYTHON_EXE%" (
    set PYTHON_EXE=python
)

set SCRIPT_PATH=%~dp0run_all_scrapers_cron.py
set TASK_NAME=InfonixMasterLeadScraperSync

echo [+] Creating Windows Scheduled Task '%TASK_NAME%'...
echo [+] Trigger: Daily Every 2 Hours (24/7 background sync)
echo.

schtasks /create /tn "%TASK_NAME%" /tr "\"%PYTHON_EXE%\" \"%SCRIPT_PATH%\"" /sc hourly /mo 2 /f /rl HIGHEST

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ===============================================================================
    echo [✓] SUCCESS! Master 24/7 Scraper Scheduled Task Created.
    echo [+] Scrapers will run automatically in background every 2 hours.
    echo [+] Data will be verified and uploaded to Google Sheets & Zoho CRM continuously.
    echo ===============================================================================
) else (
    echo.
    echo [-] Note: If access was denied, please right-click this batch file and select 'Run as administrator'.
)

echo.
pause
