#!/bin/bash

# Build script for EXIF Viewer

echo "Building EXIF Viewer application..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run tests
echo "Running tests..."
python -m pytest tests/ -v

# Build with PyInstaller
echo "Building executable..."
pyinstaller build.spec

echo "Build complete! Executable is in the dist/ folder."