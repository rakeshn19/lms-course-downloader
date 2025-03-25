# 📚 LMS Course Downloader

This project automates the download of course content from your LMS (e.g., Moodle) using Selenium.

### IMPORTANT: Before pushing to git or making your repository public:

## Never commit sensitive information:

Moodle credentials
Institution-specific URLs
Personal course IDs
Downloaded course materials
Files to exclude from git:

moodle_downloads/
course_ids.txt
debug_*.json
__pycache__/
*.pyc
.env
Using credentials safely:

### Use environment variables (recommended)
Never hardcode credentials
Keep credentials in a separate, non-committed file
Before each commit:

Remove downloaded materials
Remove course_ids.txt
Remove debug files
Check for sensitive data in comments

## 🚀 Features

- Automatic login using credentials from `.env`
- Downloads PDFs, DOCs, PPTs, Videos, etc.
- Headless browser support
- Cross-platform: works on macOS, Linux, and Windows

---

---

## 🚀 Enviornment variables

USERNAME=your_lms_username
PASSWORD=your_lms_password
LOGIN_URL=https://your-lms-site/login/index.php
DASHBOARD_URL=https://your-lms-site/my/


## ⚙️ Setup Instructions

### 🧪 1. Prerequisites

- Python 3.7+
- [Google Chrome](https://www.google.com/chrome/)
- To verify python installation on your machine , run "python --version" in command prompt(terminal)

---
###  🖥 Windows
cd lms\
setup_run.bat

### 🖥 macOS/Linux


# Clone repo and navigate into it
cd lms/

# Run setup and start script
chmod +x setup_run.sh
./setup_run.sh



### Contribution
Code reused from git repo 

https://github.com/ronit1495/moodle_downloader?tab=readme-ov-file#moodle-downloader
by Ronit Kumar

### Disclaimer

This software is provided "as is", without warranty of any kind. The authors are not responsible for any misuse of this software or any violations of institutional policies. Users are responsible for ensuring their use complies with their institution's policies and terms of service.