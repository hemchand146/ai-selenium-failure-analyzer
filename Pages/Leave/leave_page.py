# Leave page object

# --------------------------------------------------
# Imports
# --------------------------------------------------

from selenium.webdriver.common.by import By

from core.BasePage import BasePage


# --------------------------------------------------
# Page
# --------------------------------------------------

class LeavePage(BasePage):
    # Page object for OrangeHRM Leave page

    def __init__(self, driver):
        # Initialize LeavePage with driver
        super().__init__(driver)

    def wait_for_leave_page(self):
        # Wait for leave page to load
        leave_header = (By.XPATH, "//h6[text()='Leave']")
        self.wait_for_element_visible(leave_header)
