@echo off
chcp 65001 >nul
cd /d "%~dp0"
title FanUnfollowInsta

if not exist ".venv\Scripts\python.exe" (
    echo Program henüz kurulmamış. Önce kurulum.bat dosyasını çalıştır.
    pause
    exit /b 1
)

".venv\Scripts\python.exe" bot.py
pause
