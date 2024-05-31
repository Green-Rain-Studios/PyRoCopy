@echo off

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python and try again.
    exit /b
)

REM Set the virtual environment directory
set VENV_DIR=%~dp0venv

REM Check if venv exists in the current directory
if not exist "%VENV_DIR%\" (
    echo Virtual environment does not exist. Creating one...
    python -m venv venv
)

REM Activate the virtual environment
call "%VENV_DIR%\Scripts\activate"

REM Check if activation was successful
if "%VIRTUAL_ENV%" == "" (
    echo Failed to activate the virtual environment.
    exit /b
)

REM Install requirements
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

REM Run main.py
python main.py
