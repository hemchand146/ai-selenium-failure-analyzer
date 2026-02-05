# Buzz page object

# --------------------------------------------------
# Imports
# --------------------------------------------------

from selenium.webdriver.common.by import By

from core.BasePage import BasePage


# --------------------------------------------------
# Page
# --------------------------------------------------

class BuzzPage(BasePage):
    # Page object for OrangeHRM Buzz page

    def __init__(self, driver):
        # Initialize BuzzPage with driver
        super().__init__(driver)

    def wait_for_buzz_page(self):
        # Wait for buzz page to load
        buzz_header = (By.XPATH, "//h6[text()='Buzz']")
        self.wait_for_element_visible(buzz_header)
