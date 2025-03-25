# 📚 LMS Course Downloader

This project automates the download of course content from your LMS (e.g., Moodle) using Selenium.

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
- To verify python installation on your machine , run python --version in command prompt(terminal)

---
###  🖥 Windows
cd lms\
setup_run.bat

### 🖥 macOS/Linux

```bash
# Clone repo and navigate into it
cd lms/

# Run setup and start script
chmod +x setup_run.sh
./setup_run.sh



### Contribution
