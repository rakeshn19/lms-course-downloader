import sys
from pathlib import Path
from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
import logging
import time
import course_info_provider as course_info_provider
import urllib
from utils.file_utils import  get_best_filename, clean_filename
import download_service

ROOT = str(Path(__file__).resolve().parents[1])
sys.path.append(ROOT)
# Configure the logging system
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv(verbose=True)

base_url = os.environ.get('BASE_URL')
BASE_URL = os.environ.get('BASE_URL')
LOGIN_URL = os.environ.get('LOGIN_URL')
COURSE_URL = os.environ.get('COURSE_URL') # Replace with actual course page
USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')
DOWNLOAD_DIR = os.environ.get('DOWNLOAD_DIR')
REQUEST_DELAY = os.environ.get('REQUEST_DELAY')
INVALID_FILENAME_CHARS = '<>:"/\\|?*' 

print(DOWNLOAD_DIR)


def request(session, method, url, **kwargs):
    try:
        time.sleep(int(REQUEST_DELAY))
        response = session.request(method, url, **kwargs)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {str(e)}")
        if kwargs.get('stream'):
            raise
        return None 
    
def login(session):
    # Get login page and extract token (if needed)
    login_page = session.get(LOGIN_URL)
    soup = BeautifulSoup(login_page.text, "html.parser")
    token_input = soup.find("input", {"name": "logintoken"})
    logintoken = token_input['value'] if token_input else ""

    # Prepare login data
    payload = {
        "username": USERNAME,
        "password": PASSWORD,
        "logintoken": logintoken
    }

    # Submit login form
    login_response = request(session=session,url=LOGIN_URL,method='POST', data=payload)#session.request(#post(LOGIN_URL, data=payload)
    if "login" in login_response.url:
        logger.error("❌ Login failed. Check credentials.")
        exit()

    logger.info("✅ Logged in successfully!")
    return login_response


def get_course_ids(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Step 4: Extract all elements with data-course-id attribute
    course_elements = soup.find_all(attrs={"data-course-id": True})
    #print(course_elements)
    # Step 5: Extract the attribute values
    course_ids = [element["data-course-id"] for element in course_elements]
    return course_ids

def get_course_name(session, course_id):
    """Get course name from course ID."""
    course_url = f"{BASE_URL}/course/view.php?id={course_id}"
    
    try:
        response = request(session, "GET", course_url)
        if not response:
            logger.error(f"Failed to fetch course page for ID {course_id}")
            return f"Course_{course_id}"
            
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Try to find course name in page title
        title = soup.find("title")
        if title:
            # Split by ':' and take the last part for better course name
            parts = title.text.split(':')
            if len(parts) > 1:
                course_name = parts[-1].strip()
            else:
                course_name = parts[0].strip()
            if course_name:
                return clean_filename(course_name)
                
        # Fallback to h1 heading
        heading = soup.find("h1")
        if heading:
            return clean_filename(heading.text.strip())
            
        # Last resort - use course ID
        return f"Course_{course_id}"
        
    except Exception as e:
        logger.error(f"Error getting course name for ID {course_id}: {str(e)}")
        return f"Course_{course_id}"
    
def fetch_saved_courses(file_name):
    #file_path = 'my_courses.txt'
    course_ids = []
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            course_ids = [line.strip() for line in f]
    return course_ids

def save_my_course_ids(file_name, course_ids):
    with open(file_name, "w") as f:
        for item in course_ids:
            f.write(item + "\n")



def download(session):
    completed_courses= fetch_saved_courses('download_completed.txt')
    course_id = ''
    try:
        course_ids = fetch_saved_courses(file_name='my_courses.txt')
        if  course_ids is None or len(course_ids) == 0:
            course_ids = course_info_provider.get_course_ids(login_url=LOGIN_URL,user_name=USERNAME,password=PASSWORD)
            save_my_course_ids('my_courses.txt' ,course_ids)
        for cid in course_ids:
            course_id= cid
            print (cid)
            if cid and cid not in completed_courses :
                download_service.download_course_files(session=session,course_id=cid)
                completed_courses.append(cid)
            break
    except Exception as e:
        logger.error(f"Error processing course {course_id}: {str(e)}")
    finally:
        save_my_course_ids('download_completed.txt' ,completed_courses)

def main():
    # Create download folder
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    # Start a session
    session = requests.Session()
    login_response = login(session=session)
    #print(course_info_provider.get_course_ids(login_url=LOGIN_URL,user_name=USERNAME,password=PASSWORD))
    download(session=session)

main()