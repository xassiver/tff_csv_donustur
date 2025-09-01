@echo off
where python >nul 2>nul
if errorlevel 1 (
    echo Python yüklü değil! Lütfen Python kurun ve tekrar deneyin.
    pause
    exit /b
)
cd /d %~dp0
python main.py
pause
