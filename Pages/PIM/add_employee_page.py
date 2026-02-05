# Add Employee page object

# --------------------------------------------------
# Imports
# --------------------------------------------------

import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from core.BasePage import BasePage


# --------------------------------------------------
# Page
# --------------------------------------------------

class AddEmployeePage(BasePage):
    # Page object for OrangeHRM Add Employee page

    def __init__(self, driver):
        # Initialize AddEmployeePage with driver
        super().__init__(driver)
        self.logger = logging.getLogger(self.__class__.__name__)

    def __clear_input_field(self, element):
        # Clear input field using keyboard shortcuts
        # Args: element - Selenium WebElement to clear
        # Click to focus the field
        element.click()

        # Select all text with Ctrl+A
        element.send_keys(Keys.CONTROL + "a")

        # Delete the selected text
        element.send_keys(Keys.DELETE)

        # Also send backspace to ensure clearing
        element.send_keys(Keys.BACKSPACE)

    def wait_for_page(self):
        # Wait for Add Employee page to load
        self.logger.info("Waiting for Add Employee page to load")
        page_title = (By.XPATH, "//h6[text()='Add Employee']")
        self.wait_for_element_visible(page_title)
        self.wait_for_form_loader_to_disappear()
        time.sleep(0.5)
        self.logger.info("Add Employee page loaded successfully")

    def wait_for_form_loader_to_disappear(self):
        # Wait for form loader overlay to disappear
        form_loader = (By.XPATH, "//div[contains(@class, 'oxd-form-loader')]")
        try:
            self.wait.until(EC.invisibility_of_element_located(form_loader))
        except Exception:
            # If element doesn't exist or already invisible, that's fine
            pass

    def fill_employee_name(self, first, middle, last):
        # Fill employee name fields
        # Args: first (str) - First name, middle (str) - Middle name, last (str) - Last name
        self.logger.info(f"Filling employee name fields - First: {first}, Middle: {middle}, Last: {last}")
        # Wait for form loader to disappear before interacting
        self.wait_for_form_loader_to_disappear()

        first_name = (By.NAME, "firstName")
        fn = self.wait_for_element_visible(first_name)
        self.__clear_input_field(fn)
        fn.send_keys(first)
        time.sleep(0.8)

        middle_name = (By.NAME, "middleName")
        middle_field = self.find_element(middle_name)
        self.__clear_input_field(middle_field)
        middle_field.send_keys(middle)
        time.sleep(0.8)

        last_name = (By.NAME, "lastName")
        last_field = self.find_element(last_name)
        self.__clear_input_field(last_field)
        last_field.send_keys(last)
        time.sleep(0.8)
        self.logger.info("Employee name fields filled successfully")

    def fill_employee_id(self, emp_id):
        # Fill Employee ID field
        # Args: emp_id (str) - Employee ID
        self.logger.info(f"Filling employee ID: {emp_id}")
        # Wait for form loader to disappear before interacting
        self.wait_for_form_loader_to_disappear()

        employee_id = (By.XPATH, "//label[text()='Employee Id']/following::input[1]")
        emp_id_field = self.wait_for_element_visible(employee_id)
        self.__clear_input_field(emp_id_field)
        emp_id_field.send_keys(emp_id)
        time.sleep(0.8)
        self.logger.info("Employee ID filled successfully")

    def enable_login_details(self):
        # Enable 'Create Login Details' toggle
        self.logger.info("Enabling 'Create Login Details' toggle")
        create_login_toggle = (By.XPATH, "//p[normalize-space()='Create Login Details']/ancestor::div[contains(@class,'oxd-form-row')]//label")
        toggle = self.wait_for_element_clickable(create_login_toggle)
        toggle.click()
        time.sleep(1)
        self.logger.info("'Create Login Details' toggle enabled successfully")

    def fill_login_details(self, username, password):
        # Fill login credentials
        # Args: username (str) - Username, password (str) - Password
        self.logger.info(f"Filling login details - Username: {username}")
        # Wait for form loader to disappear before interacting
        self.wait_for_form_loader_to_disappear()

        username_locator = (By.XPATH, "//label[text()='Username']/following::input[1]")
        user = self.wait_for_element_visible(username_locator)
        self.__clear_input_field(user)
        user.send_keys(username)
        time.sleep(0.8)

        password_locator = (By.XPATH, "//label[text()='Password']/following::input[1]")
        password_field = self.find_element(password_locator)
        self.__clear_input_field(password_field)
        password_field.send_keys(password)
        time.sleep(0.8)

        confirm_password_locator = (By.XPATH, "//label[text()='Confirm Password']/following::input[1]")
        confirm_pwd_field = self.find_element(confirm_password_locator)
        self.__clear_input_field(confirm_pwd_field)
        confirm_pwd_field.send_keys(password)
        time.sleep(0.8)
        self.logger.info("Login details filled successfully")

    def save(self):
        # Click Save button
        self.logger.info("Clicking Save button")
        save_button = (By.XPATH, "//button[@type='submit' and .=' Save ']")
        btn = self.wait_for_element_clickable(save_button)
        btn.click()
        time.sleep(1.2)
        self.logger.info("Save button clicked successfully")
