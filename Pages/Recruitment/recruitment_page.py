# Recruitment page object

# --------------------------------------------------
# Imports
# --------------------------------------------------

from selenium.webdriver.common.by import By

from core.BasePage import BasePage


# --------------------------------------------------
# Page
# --------------------------------------------------

class RecruitmentPage(BasePage):
    # Page object for OrangeHRM Recruitment page

    def __init__(self, driver):
        # Initialize RecruitmentPage with driver
        super().__init__(driver)

    def wait_for_recruitment_page(self):
        # Wait for recruitment page to load
        recruitment_header = (By.XPATH, "//h6[text()='Recruitment']")
        self.wait_for_element_visible(recruitment_header)
