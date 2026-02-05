# Login page object

# --------------------------------------------------
# Imports
# --------------------------------------------------

from selenium.webdriver.common.by import By

from core.BasePage import BasePage


# --------------------------------------------------
# Page
# --------------------------------------------------

class LoginPage(BasePage):
    # Page object for OrangeHRM Login page

    def __init__(self, driver):
        # Initialize LoginPage with driver
        super().__init__(driver)

    def login(self, username, password):
        # Perform login with username and password
        # Args: username (str) - Username, password (str) - Password
        # Wait for username field and enter value
        username_field = (By.NAME, "username")
        self.clear_and_send_keys(username_field, username)

        # Wait for password field and enter value
        password_field = (By.NAME, "password")
        self.clear_and_send_keys(password_field, password)

        # Wait for login button and click
        login_btn = (By.XPATH, "//button[@type='submit']")
        self.click_element(login_btn)
