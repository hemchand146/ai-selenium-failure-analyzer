# Base test class
# Provides browser lifecycle, authentication, and common utilities for testcases

# --------------------------------------------------
# Imports
# --------------------------------------------------

import json

from core.helper import Helper
from Pages.Login.login_page import LoginPage
from browser import Browser


# --------------------------------------------------
# Base Test
# --------------------------------------------------

class BaseTest:
    # Base class for all test cases
    # Handles browser initialization, login, and common test operations

    def __init__(self, test_data, logger):
        # Initialize base test with test data and logger
        # Args: test_data (dict) - Test data from JSON file, logger - Logger instance
        self.test_data = test_data
        self.logger = logger
        self.helper = Helper()  # Create Helper instance

        self.browser = None
        self.driver = None

        # Common page object slots (tests can use what they need)
        self.dashboard = None
        self.pim = None
        self.add_emp = None
        self.directory = None
        self.candidates = None
        self.claim = None

        self.result = {
            "status": "PASS",
            "error": None
        }

        with open("config.json", "r") as f:
            self.config = json.load(f)

    def login(self, url, username, password):
        # Initialize browser and perform login
        # Args: url (str) - URL to open, username (str) - Username for login, password (str) - Password for login
        browser_name = self.config.get("browser", "chrome")

        self.browser = Browser(browser_name, config=self.config)
        self.driver = self.browser.start()

        self.browser.open_url(url)

        LoginPage(self.driver).login(username, password)


    def ready(self):
        # Waits until the page is fully loaded (Max wait time: 300 minutes)
        self.helper.ready(self.driver, self.logger, timeout_minutes=300)

    def exists(self, locator_type, locator_value):
        # Check if an element exists on the page
        # Args: locator_type (str) - Type of locator, locator_value (str) - The locator value
        # Returns: bool - True if element exists, False otherwise
        return self.helper.exists(
            self.driver, locator_type, locator_value
        )

    def error(self):
        # Get error message from the page if it exists
        # This method is specifically designed for OrangeHRM forms
        # Returns: str - Error message text if found, empty string otherwise
        return self.helper.error(self.driver, self.logger)
