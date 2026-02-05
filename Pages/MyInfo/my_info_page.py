from selenium.webdriver.common.by import By
from core.BasePage import BasePage


class MyInfoPage(BasePage):
    # Page object for OrangeHRM My Info page

    def __init__(self, driver):
        # Initialize MyInfoPage with driver
        super().__init__(driver)

    def wait_for_my_info_page(self):
        # Wait for my info page to load
        my_info_header = (By.XPATH, "//h6[text()='My Info']")
        self.wait_for_element_visible(my_info_header)
