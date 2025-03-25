from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Setup Chrome options for headless mode (optional)
chrome_options = Options()
chrome_options.add_argument("--headless")  # comment this out if you want to see the browser
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Setup driver using webdriver-manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


def get_course_ids(login_url, user_name , password):
    # Setup Chrome (make sure chromedriver is installed and PATH is set)
    #driver = webdriver.Chrome()

    # Open login page
    driver.get(login_url)
    time.sleep(2)

    # === Fill login form ===
    username_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")

    username_input.send_keys(user_name)
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)

    time.sleep(5)  # Wait for redirect

    # Load the page
    driver.get("https://lms.iimk.ac.in/my/")  # Example URL

    # Wait for JS to load
    time.sleep(5)

    # Find course cards with data-course-id
    course_cards = driver.find_elements(By.CSS_SELECTOR, 'div[data-course-id]')

    # Extract course IDs
    course_ids = [card.get_attribute("data-course-id") for card in course_cards]
    course_ids = list(filter(lambda x: x.strip(),set(course_ids)))
    #course_ids.remove('')

    print("Extracted course IDs:", course_ids)

    driver.quit()
    return course_ids
