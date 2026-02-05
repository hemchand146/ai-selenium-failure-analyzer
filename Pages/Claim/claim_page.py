# Claim page object

# --------------------------------------------------
# Imports
# --------------------------------------------------

import time

from selenium.webdriver.common.by import By

from core.BasePage import BasePage
from utils.dropdown import DropdownHelper


# --------------------------------------------------
# Page
# --------------------------------------------------

class ClaimPage(BasePage):
    # Page object for OrangeHRM Claim page

    def __init__(self, driver):
        # Initialize ClaimPage with driver
        super().__init__(driver)
        self.dropdown_helper = DropdownHelper(driver)

    def wait_for_claim_page(self):
        # Wait for claim page to load
        claim_header = (By.XPATH, "//h6[text()='Claim']")
        self.wait_for_element_visible(claim_header)

    def enter_employee_name(self, employee_name):
        # Enter employee name in the search field
        # Args: employee_name (str) - Employee name to enter
        # Find the input field within the autocomplete wrapper for Employee Name
        employee_field = (By.XPATH, "//label[text()='Employee Name']/ancestor::div[contains(@class, 'oxd-input-group')]//input[@placeholder='Type for hints...']")
        self.send_keys_to_element(employee_field, employee_name)
        time.sleep(4)

        # Wait for dropdown container to appear first
        dropdown_container = (By.XPATH, "//div[@role='listbox']")
        self.wait_for_element_visible(dropdown_container)
        time.sleep(2)

        # Wait for dropdown suggestions to appear and click the matching one
        suggestion = (By.XPATH, "//div[@role='option']//span[text()='" + employee_name + "']")
        self.wait_for_element_visible(suggestion)
        self.click_element(suggestion)
        time.sleep(1)

    def select_event_name(self, event_name):
        # Select event name from dropdown
        # Args: event_name (str) - Event name to select (e.g., 'Accommodation', 'Medical Reimbursement', 'Travel Allowance')
        self.dropdown_helper.select_dropdown_by_label("Event Name", event_name)

    def select_status(self, status):
        # Select status from dropdown
        # Args: status (str) - Status to select (e.g., 'Paid', 'Rejected', 'Pending Approval')
        self.dropdown_helper.select_dropdown_by_label("Status", status)

    def enter_from_date(self, date):
        # Enter From Date
        # Args: date (str) - Date in format 'dd-mm-yyyy'
        # Navigate to the first date input (From Date)
        from_date_field = (By.XPATH, "//label[text()='From Date']/ancestor::div[contains(@class, 'oxd-input-group')]//input[@placeholder='dd-mm-yyyy']")
        self.clear_and_send_keys(from_date_field, date)
        time.sleep(0.8)

    def enter_to_date(self, date):
        # Enter To Date
        # Args: date (str) - Date in format 'dd-mm-yyyy'
        # Navigate to the second date input (To Date)
        to_date_field = (By.XPATH, "//label[text()='To Date']/ancestor::div[contains(@class, 'oxd-input-group')]//input[@placeholder='dd-mm-yyyy']")
        self.clear_and_send_keys(to_date_field, date)
        time.sleep(0.8)

    def click_search(self):
        # Click the Search button
        # Use a more specific selector for the Search button
        search_button = (By.XPATH, "//div[contains(@class, 'oxd-form-actions')]//button[contains(., 'Search')]")
        self.click_element(search_button)
        time.sleep(1.5)
