#!/bin/bash
# Build script for creating CloudSathi CLI executable locally

set -e

echo "🔨 Building CloudSathi CLI executable..."

# Check if PyInstaller is installed
if ! command -v pyinstaller &> /dev/null; then
    echo "📦 Installing PyInstaller..."
    pip install pyinstaller
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r backend/requirements.txt

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build dist

# Build executable
echo "🏗️  Building executable with PyInstaller..."
pyinstaller cloudsathi.spec --clean

# Get OS type
OS_TYPE=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m)

# Rename based on OS
if [ "$OS_TYPE" = "darwin" ]; then
    EXECUTABLE_NAME="cloudsathi-macos-${ARCH}"
elif [ "$OS_TYPE" = "linux" ]; then
    EXECUTABLE_NAME="cloudsathi-linux-${ARCH}"
else
    EXECUTABLE_NAME="cloudsathi-${OS_TYPE}-${ARCH}"
fi

echo "📝 Renaming executable to ${EXECUTABLE_NAME}..."
mv dist/cloudsathi "dist/${EXECUTABLE_NAME}"

echo "✅ Build complete!"
echo "📍 Executable location: dist/${EXECUTABLE_NAME}"
echo ""
echo "To install globally:"
echo "  sudo mv dist/${EXECUTABLE_NAME} /usr/local/bin/cloudsathi"
echo "  chmod +x /usr/local/bin/cloudsathi"
echo ""
echo "To test:"
echo "  ./dist/${EXECUTABLE_NAME} --version"
