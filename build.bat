@echo off
REM Build script for EXIF Viewer on Windows

echo Building EXIF Viewer application...

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Run tests
echo Running tests...
python -m pytest tests\ -v

REM Build with PyInstaller
echo Building executable...
pyinstaller build.spec

echo Build complete! Executable is in the dist\ folder.
pause