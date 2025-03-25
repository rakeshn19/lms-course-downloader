"""Download service for handling file downloads."""

import os
import time
import logging
import urllib.parse
from bs4 import BeautifulSoup
#from moodle.moodle import BASE_URL, DOWNLOAD_DIR
from utils.request_utils import safe_request
from utils.file_utils import create_folder, get_best_filename, clean_filename

logger = logging.getLogger(__name__)
DOWNLOAD_DIR = "lms_downloads"
BASE_URL = "https://lms.iimk.ac.in/"

def get_course_name(session, course_id):
    """Get course name from course ID."""
    course_url = f"{BASE_URL}/course/view.php?id={course_id}"
    
    try:
        response = safe_request(session, "GET", course_url)
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

def download_course_files(session, course_id):
    """Download all files from a course."""
    print(course_id)
    course_url = f"{BASE_URL}/course/view.php?id={course_id}"
    
    try:
        # Get course name and create folder
        course_name = get_course_name(session, course_id)
        logger.info(f"\nProcessing: {course_name} (ID: {course_id})")
        
        course_folder = os.path.join(DOWNLOAD_DIR, clean_filename(course_name))
        create_folder(course_folder)
        
        course_page = safe_request(session, "GET", course_url)
        if not course_page:
            logger.error("Failed to fetch course page")
            return
            
        soup = BeautifulSoup(course_page.text, "html.parser")
        
        # Find all links
        links = soup.find_all("a", href=True)
        logger.debug(f"Found {len(links)} total links in course page")
        
        file_count = 0
        for link in links:
            file_url = link["href"]
            
            if "pluginfile.php" in file_url or "/resource/" in file_url:
                try:
                    # Get file URL
                    if not file_url.startswith("http"):
                        file_url = urllib.parse.urljoin(BASE_URL, file_url)
                    
                    # Make HEAD request to get headers
                    head_response = safe_request(session, "HEAD", file_url)
                    if not head_response:
                        continue
                    
                    # Get file content start for signature detection
                    file_content = None
                    file_response = safe_request(session, "GET", file_url, stream=True)
                    if file_response:
                        file_content = next(file_response.iter_content(chunk_size=8), None)
                    
                    # Get best filename with extension
                    filename = get_best_filename(link, file_url, head_response, file_content)
                    file_path = os.path.join(course_folder, filename)
                    
                    # Handle duplicate filenames
                    counter = 1
                    base_name, ext = os.path.splitext(filename)
                    while os.path.exists(file_path):
                        new_filename = f"{base_name}_{counter}{ext}"
                        file_path = os.path.join(course_folder, new_filename)
                        counter += 1
                    
                    logger.info(f"Downloading: {os.path.basename(file_path)}")
                    
                    # Download the file
                    if not file_response:
                        file_response = safe_request(session, "GET", file_url, stream=True)
                    if not file_response:
                        continue
                    
                    if file_response.status_code == 200:
                        with open(file_path, "wb") as f:
                            # If we already read the start of the file, write it
                            if file_content:
                                f.write(file_content)
                            # Write the rest of the file
                            for chunk in file_response.iter_content(chunk_size=8192):
                                if chunk:
                                    f.write(chunk)
                        logger.info(f"Successfully downloaded: {os.path.basename(file_path)}")
                        file_count += 1
                    else:
                        logger.error(f"Failed to download {os.path.basename(file_path)}: {file_response.status_code}")
                
                except Exception as e:
                    logger.error(f"Error downloading file: {str(e)}")
                    continue
        
        logger.info(f"Downloaded {file_count} files from {course_name}")
        
    except Exception as e:
        logger.error(f"Error processing course {course_id}: {str(e)}")

def download_all_courses(session, course_ids):
    """Download files from all courses."""
    logger.info("\nStarting file downloads...")
    
    # Create downloads folder
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    
    # Download files from each course
    for course_id in course_ids:
        download_course_files(session, course_id)
        time.sleep(2)  # Add delay between processing courses
    
    logger.info("\nDownload process completed!") 