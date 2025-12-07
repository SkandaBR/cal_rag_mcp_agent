#!/bin/bash

# Script to set up virtual environment and install dependencies
# Usage: bash runme.sh

set -e  # Exit on error

echo "==================================="
echo "Setting up Python Virtual Environment"
echo "==================================="

# Step 1: Create virtual environment
echo "Step 1: Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Skipping creation."
else
    python -m venv venv
    echo "Virtual environment created successfully."
fi

# Step 2: Activate virtual environment
echo ""
echo "Step 2: Activating virtual environment..."
# Detect OS and activate accordingly
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows (Git Bash)
    source venv/Scripts/activate
else
    # Linux/Mac
    source venv/bin/activate
fi
echo "Virtual environment activated."

# Step 3: Upgrade pip
echo ""
echo "Step 3: Upgrading pip..."
python -m pip install --upgrade pip

# Step 4: Install requirements
echo ""
echo "Step 4: Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo ""
echo "==================================="
echo "Setup completed successfully!"
echo "==================================="
echo ""
echo "To activate the virtual environment in the future, run:"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "  source venv/Scripts/activate"
else
    echo "  source venv/bin/activate"
fi
echo ""
echo "To deactivate, run:"
echo "  deactivate"
