# Directory page object

# --------------------------------------------------
# Imports
# --------------------------------------------------

import logging
import time
from selenium.webdriver.common.by import By
from core.BasePage import BasePage
from utils.dropdown import DropdownHelper


# --------------------------------------------------
# Page
# --------------------------------------------------

class DirectoryPage(BasePage):
    # Page object for OrangeHRM Directory page

    def __init__(self, driver):
        # Initialize DirectoryPage with driver
        super().__init__(driver)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.dropdown_helper = DropdownHelper(driver)

    def wait_for_directory_page(self):
        # Wait for directory page to load
        directory_header = (By.XPATH, "//h6[text()='Directory']")
        self.wait_for_element_visible(directory_header)
        time.sleep(1)

    def enter_employee_name(self, employee_name):
        # Enter employee name in the search field
        # Args: employee_name (str) - Employee name to search
        self.logger.info(f"Employee Name: {employee_name}")
        employee_input = (By.XPATH, "//label[text()='Employee Name']/following::input[@placeholder='Type for hints...'][1]")
        input_field = self.wait_for_element_visible(employee_input)
        input_field.click()
        input_field.send_keys(employee_name)
        time.sleep(1)

    def select_job_title(self, job_title):
        # Select Job Title from dropdown
        # Args: job_title (str) - Job title to select
        self.logger.info(f"Job Title: {job_title}")
        self.dropdown_helper.select_dropdown_by_label('Job Title', job_title)

    def select_location(self, location):
        # Select Location from dropdown
        # Args: location (str) - Location to select
        self.logger.info(f"Location: {location}")
        self.dropdown_helper.select_dropdown_by_label('Location', location)

    def click_search(self):
        # Click the Search button
        search_button = (By.XPATH, "//*[@id='app']/div[1]/div[2]/div[2]/div/div[1]/div[2]/form/div[3]/button[2]")
        btn = self.wait_for_element_clickable(search_button)
        btn.click()
        time.sleep(1)
