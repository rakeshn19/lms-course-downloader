"""Request handling utilities for the Moodle Downloader."""

import time
import logging
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from config.config import (
    RETRY_ATTEMPTS,
    RETRY_BACKOFF_FACTOR,
    RETRY_STATUS_FORCELIST,
    REQUEST_DELAY
)

logger = logging.getLogger(__name__)

def create_session():
    """Create a session with retry logic."""
    session = requests.Session()
    
    # Configure retry strategy
    retry_strategy = Retry(
        total=RETRY_ATTEMPTS,
        backoff_factor=RETRY_BACKOFF_FACTOR,
        status_forcelist=RETRY_STATUS_FORCELIST
    )
    
    # Mount the adapter with retry strategy for both HTTP and HTTPS
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session

def safe_request(session, method, url, **kwargs):
    """Make a request with proper error handling and delays."""
    try:
        # Add a small delay before each request
        time.sleep(REQUEST_DELAY)
        
        # Make the request
        response = session.request(method, url, **kwargs)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {str(e)}")
        if kwargs.get('stream'):
            # For file downloads, we want to fail
            raise
        return None 