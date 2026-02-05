# Dashboard page object

# --------------------------------------------------
# Imports
# --------------------------------------------------

from selenium.webdriver.common.by import By

from core.BasePage import BasePage


# --------------------------------------------------
# Page
# --------------------------------------------------

class DashboardPage(BasePage):
    # Page object for OrangeHRM Dashboard page

    def __init__(self, driver):
        # Initialize DashboardPage with driver
        super().__init__(driver)

    def wait_for_dashboard(self):
        # Wait for dashboard page to load
        dashboard_header = (By.XPATH, "//h6[text()='Dashboard']")
        self.wait_for_element_visible(dashboard_header)

    # ...existing code...

    def go_to_admin(self):
        # Navigate to Admin module
        admin_menu = (By.XPATH, "//span[text()='Admin']")
        self.click_element(admin_menu)

    def go_to_pim(self):
        # Navigate to PIM (Personal Information Management) module
        pim_menu = (By.XPATH, "//span[text()='PIM']")
        self.click_element(pim_menu)

    def go_to_leave(self):
        # Navigate to Leave module
        leave_menu = (By.XPATH, "//span[text()='Leave']")
        self.click_element(leave_menu)

    def go_to_time(self):
        # Navigate to Time module
        time_menu = (By.XPATH, "//span[text()='Time']")
        self.click_element(time_menu)

    def go_to_recruitment(self):
        # Navigate to Recruitment module
        recruitment_menu = (By.XPATH, "//span[text()='Recruitment']")
        self.click_element(recruitment_menu)

    def go_to_my_info(self):
        # Navigate to My Info module
        my_info_menu = (By.XPATH, "//span[text()='My Info']")
        self.click_element(my_info_menu)

    def go_to_performance(self):
        # Navigate to Performance module
        performance_menu = (By.XPATH, "//span[text()='Performance']")
        self.click_element(performance_menu)

    def go_to_directory(self):
        # Navigate to Directory module
        directory_menu = (By.XPATH, "//span[text()='Directory']")
        self.click_element(directory_menu)

    def go_to_maintenance(self):
        # Navigate to Maintenance module
        maintenance_menu = (By.XPATH, "//span[text()='Maintenance']")
        self.click_element(maintenance_menu)

    def go_to_claim(self):
        # Navigate to Claim module
        claim_menu = (By.XPATH, "//span[text()='Claim']")
        self.click_element(claim_menu)

    def go_to_buzz(self):
        # Navigate to Buzz module
        buzz_menu = (By.XPATH, "//span[text()='Buzz']")
        self.click_element(buzz_menu)
