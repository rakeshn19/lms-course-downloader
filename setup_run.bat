@echo off
echo 🔧 Setting up Python virtual environment...
python -m venv venv

call venv\Scripts\activate

echo 📦 Installing dependencies...
pip install -r requirement.txt
echo ✅ Dependencies installed.

echo 🚀 Running main script...
python lms_download.py