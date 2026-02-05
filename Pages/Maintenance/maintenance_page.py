# Maintenance page object

# --------------------------------------------------
# Imports
# --------------------------------------------------

from selenium.webdriver.common.by import By

from core.BasePage import BasePage


# --------------------------------------------------
# Page
# --------------------------------------------------

class MaintenancePage(BasePage):
    # Page object for OrangeHRM Maintenance page

    def __init__(self, driver):
        # Initialize MaintenancePage with driver
        super().__init__(driver)

    def wait_for_maintenance_page(self):
        # Wait for maintenance page to load
        maintenance_header = (By.XPATH, "//h6[text()='Maintenance']")
        self.wait_for_element_visible(maintenance_header)
