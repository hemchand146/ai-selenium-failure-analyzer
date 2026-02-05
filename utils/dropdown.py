# Dropdown helper utilities
# Contains reusable helpers for interacting with OrangeHRM-style dropdowns

# --------------------------------------------------
# Imports
# --------------------------------------------------

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# --------------------------------------------------
# Helper
# --------------------------------------------------

class DropdownHelper:
    # Helper class for handling dropdown interactions
    # Provides common/generic methods for selecting dropdown options

    def __init__(self, driver, wait_timeout=15):
        # Initialize DropdownHelper with driver and wait timeout
        # Args: driver - Selenium WebDriver instance, wait_timeout (int) - Explicit wait timeout in seconds (default: 15)
        self.driver = driver
        self.wait = WebDriverWait(driver, wait_timeout)

    def select_dropdown_by_label(self, label_text, option_text):
        # Select a dropdown option by label text and option text
        # Generic method that works for any dropdown
        # Args: label_text (str) - The label text of the dropdown, option_text (str) - The text of the option to select
        # Example: dropdown_helper.select_dropdown_by_label('Job Title', 'Software Engineer')
        try:
            # Click on dropdown to open it
            dropdown_input = (By.XPATH, f"//label[text()='{label_text}']/following::div[contains(@class, 'oxd-select-text-input')][1]")
            dropdown = self.wait.until(EC.element_to_be_clickable(dropdown_input))
            dropdown.click()
            time.sleep(0.8)

            # Select the option from dropdown menu
            option = (By.XPATH, f"//div[@role='option']//span[contains(text(), '{option_text}')]")
            selected_option = self.wait.until(EC.element_to_be_clickable(option))
            selected_option.click()
            time.sleep(0.8)

        except Exception as e:
            raise

    def select_by_xpath(self, dropdown_xpath, option_text):
        # Select a dropdown option using custom XPath locators
        # Args: dropdown_xpath (str) - XPath to the dropdown input element, option_text (str) - The text of the option to select
        # Example: dropdown_helper.select_by_xpath("//label[text()='Custom Label']/following::div[contains(@class, 'oxd-select-text-input')][1]", "Option Text")
        try:
            # Click on dropdown to open it
            dropdown = self.wait.until(EC.element_to_be_clickable((By.XPATH, dropdown_xpath)))
            dropdown.click()
            time.sleep(0.8)

            # Select the option from dropdown menu
            option = (By.XPATH, f"//div[@role='option']//span[contains(text(), '{option_text}')]")
            selected_option = self.wait.until(EC.element_to_be_clickable(option))
            selected_option.click()
            time.sleep(0.8)

        except Exception as e:
            raise

    def select_by_partial_text(self, label_text, partial_option_text):
        # Select a dropdown option using partial text matching
        # Args: label_text (str) - The label text of the dropdown, partial_option_text (str) - Partial text of the option to select
        # Example: dropdown_helper.select_by_partial_text('Status', 'Application')
        try:
            # Click on dropdown to open it
            dropdown_input = (By.XPATH, f"//label[text()='{label_text}']/following::div[contains(@class, 'oxd-select-text-input')][1]")
            dropdown = self.wait.until(EC.element_to_be_clickable(dropdown_input))
            dropdown.click()
            time.sleep(0.8)

            # Select the option using partial text match
            option = (By.XPATH, f"//div[@role='option']//span[contains(text(), '{partial_option_text}')]")
            selected_option = self.wait.until(EC.element_to_be_clickable(option))
            selected_option.click()
            time.sleep(0.8)

        except Exception as e:
            raise

    def get_dropdown_options(self, label_text):
        # Get all available options from a dropdown
        # Args: label_text (str) - The label text of the dropdown
        # Returns: list - List of option texts available in the dropdown
        try:
            # Click on dropdown to open it
            dropdown_input = (By.XPATH, f"//label[text()='{label_text}']/following::div[contains(@class, 'oxd-select-text-input')][1]")
            dropdown = self.wait.until(EC.element_to_be_clickable(dropdown_input))
            dropdown.click()
            time.sleep(0.8)

            # Get all option elements
            options = (By.XPATH, f"//div[@role='option']//span")
            option_elements = self.wait.until(EC.presence_of_all_elements_located(options))

            option_texts = [opt.text for opt in option_elements if opt.text]

            # Close dropdown by pressing Escape
            self.driver.execute_script("arguments[0].dispatchEvent(new KeyboardEvent('keydown', {key: 'Escape'}))")
            time.sleep(0.5)

            return option_texts

        except Exception as e:
            raise

    def is_option_available(self, label_text, option_text):
        # Check if a specific option is available in a dropdown
        # Args: label_text (str) - The label text of the dropdown, option_text (str) - The text of the option to check
        # Returns: bool - True if option is available, False otherwise
        try:
            available_options = self.get_dropdown_options(label_text)
            is_available = any(option_text in option for option in available_options)
            return is_available

        except Exception as e:
            return False

    def clear_dropdown(self, label_text):
        # Clear (deselect) a dropdown selection
        # Args: label_text (str) - The label text of the dropdown
        try:
            # Click on dropdown to open it
            dropdown_input = (By.XPATH, f"//label[text()='{label_text}']/following::div[contains(@class, 'oxd-select-text-input')][1]")
            dropdown = self.wait.until(EC.element_to_be_clickable(dropdown_input))
            dropdown.click()
            time.sleep(0.8)

            # Select "-- Select --" option
            option = (By.XPATH, "//div[@role='option']//span[contains(text(), '-- Select --')]")
            selected_option = self.wait.until(EC.element_to_be_clickable(option))
            selected_option.click()
            time.sleep(0.8)

        except Exception as e:
            raise
