from selenium.webdriver.common.by import By
from core.BasePage import BasePage


class TimePage(BasePage):
    # Page object for OrangeHRM Time page

    def __init__(self, driver):
        # Initialize TimePage with driver
        super().__init__(driver)

    def wait_for_time_page(self):
        # Wait for time page to load
        time_header = (By.XPATH, "//h6[text()='Time']")
        self.wait_for_element_visible(time_header)
