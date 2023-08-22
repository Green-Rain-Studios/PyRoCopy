@echo off

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed.
    exit /b
)

REM Check if venv exists in the current directory
if not exist ".\venv\" (
    echo Virtual environment does not exist. Creating one...
    python -m venv venv
)

REM Activate the virtual environment
call .\venv\Scripts\activate

REM Install requirements
python -m pip install -r requirements.txt

REM Run main.py
python main.py
