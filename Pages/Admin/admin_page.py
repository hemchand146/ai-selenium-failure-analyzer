# Admin page object

# --------------------------------------------------
# Imports
# --------------------------------------------------

from selenium.webdriver.common.by import By

from core.BasePage import BasePage


# --------------------------------------------------
# Page
# --------------------------------------------------

class AdminPage(BasePage):
    # Page object for OrangeHRM Admin page

    def __init__(self, driver):
        # Initialize AdminPage with driver
        super().__init__(driver)

    def wait_for_admin_page(self):
        # Wait for admin page to load
        admin_header = (By.XPATH, "//h6[text()='Admin']")
        self.wait_for_element_visible(admin_header)
