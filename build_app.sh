#!/bin/bash

# Build script for Flappy Bird macOS App
set -e

echo "Building Flappy Bird macOS App..."

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Error: venv not found. Please create a virtual environment first."
    exit 1
fi

# Install PyInstaller if not already installed
pip install pyinstaller > /dev/null 2>&1 || pip install pyinstaller

# Create exe directory if it doesn't exist
mkdir -p exe

# Clean previous builds
rm -rf exe/FlappyBird.app
rm -rf build dist

# Build the app
echo "Running PyInstaller..."
pyinstaller flappybird.spec --clean --noconfirm

# Move the app to exe folder
if [ -d "dist/FlappyBird.app" ]; then
    mv dist/FlappyBird.app exe/
    echo "✓ App built successfully: exe/FlappyBird.app"
else
    echo "Error: App bundle not found in dist/"
    exit 1
fi

# Clean up build artifacts (but keep the spec file)
rm -rf build dist

echo "Build complete! App is in exe/FlappyBird.app"
echo ""
echo "To add an icon later:"
echo "1. Create or convert your icon to .icns format"
echo "2. Update flappybird.spec: change icon=None to icon='path/to/icon.icns'"
echo "3. Rebuild with: ./build_app.sh"

