@echo off
REM Path to your project
set "PROJECT_DIR=D:\Projects\Mindhive_Cb"

REM 1) Launch Admin CMD #1: activate venv and start Uvicorn
powershell -NoProfile -Command ^
  "Start-Process cmd.exe -ArgumentList '/k cd /d \"%PROJECT_DIR%\" && venv\Scripts\activate.bat && uvicorn app.main:app --reload' -Verb RunAs"

REM 2) Launch Admin CMD #2: activate venv only
powershell -NoProfile -Command ^
  "Start-Process cmd.exe -ArgumentList '/k cd /d \"%PROJECT_DIR%\" && venv\Scripts\activate.bat' -Verb RunAs"
