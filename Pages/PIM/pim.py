# PIM page objects

# --------------------------------------------------
# Imports
# --------------------------------------------------

from selenium.webdriver.common.by import By

from core.BasePage import BasePage


# --------------------------------------------------
# Page
# --------------------------------------------------

class PIMPage(BasePage):
    # Page Object for PIM main page (Employee List)
    # Responsibilities:
    # - Ensure PIM page is loaded
    # - Click Add Employee

    def __init__(self, driver):
        # Initialize PIMPage with driver
        super().__init__(driver)

    def wait_for_pim_page(self):
        # Wait until PIM page is visible
        pim_header = (By.XPATH, "//h6[text()='PIM']")
        self.wait_for_element_visible(pim_header)

    def click_add_employee(self):
        # Click Add Employee button
        add_employee_button = (By.XPATH, "//button[.=' Add ']")
        self.click_element(add_employee_button)
