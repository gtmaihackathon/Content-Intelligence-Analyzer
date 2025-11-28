#!/bin/bash

# Content Intelligence Analyzer - Installation Script
# This script automates the setup process

echo "============================================================"
echo "📊 Content Intelligence Analyzer - Installation"
echo "============================================================"
echo ""

# Check if Python is installed
echo "🔍 Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ $PYTHON_VERSION found"
else
    echo "❌ Python 3 is not installed"
    echo "Please install Python 3.8 or higher from https://python.org"
    exit 1
fi

# Check if pip is installed
echo ""
echo "🔍 Checking pip installation..."
if command -v pip3 &> /dev/null; then
    PIP_VERSION=$(pip3 --version)
    echo "✅ pip found"
else
    echo "❌ pip is not installed"
    echo "Installing pip..."
    python3 -m ensurepip --upgrade
fi

# Create virtual environment (optional but recommended)
echo ""
read -p "📦 Create virtual environment? (recommended) [y/N]: " CREATE_VENV
if [[ $CREATE_VENV =~ ^[Yy]$ ]]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    
    # Activate virtual environment
    if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
    
    echo "✅ Virtual environment created and activated"
fi

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ All dependencies installed successfully"
else
    echo "❌ Error installing dependencies"
    exit 1
fi

# Create data directory
echo ""
echo "📁 Creating data directory..."
mkdir -p analyzer_data
echo "✅ Data directory created"

# Run system test
echo ""
read -p "🧪 Run system tests? [Y/n]: " RUN_TESTS
if [[ ! $RUN_TESTS =~ ^[Nn]$ ]]; then
    echo ""
    echo "Running system tests..."
    python3 test_system.py
fi

# Installation complete
echo ""
echo "============================================================"
echo "✅ Installation Complete!"
echo "============================================================"
echo ""
echo "🚀 To start the application, run:"
echo "   streamlit run content_analyzer.py"
echo ""
echo "📚 Documentation:"
echo "   README.md         - Complete documentation"
echo "   QUICK_START.md    - Quick start guide"
echo "   DEPLOYMENT.md     - Deployment guide"
echo ""
echo "🎉 Happy analyzing!"
echo ""
