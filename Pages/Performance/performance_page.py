# Performance page object

# --------------------------------------------------
# Imports
# --------------------------------------------------

from selenium.webdriver.common.by import By

from core.BasePage import BasePage


# --------------------------------------------------
# Page
# --------------------------------------------------

class PerformancePage(BasePage):
    # Page object for OrangeHRM Performance page

    def __init__(self, driver):
        # Initialize PerformancePage with driver
        super().__init__(driver)

    def wait_for_performance_page(self):
        # Wait for performance page to load
        performance_header = (By.XPATH, "//h6[text()='Performance']")
        self.wait_for_element_visible(performance_header)
