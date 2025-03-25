#!/bin/bash

echo "🔧 Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "📦 Installing dependencies..."
pip install -r requirement.txt
echo "✅ Dependencies installed."

echo "🚀 Running main script..."
python lms_download.py
