# Test Case 101: Add Employee Test
# Description: Verify that a new employee can be added to the system with all required details

# --------------------------------------------------
# Imports
# --------------------------------------------------

from core import BaseTest
from Pages.Dashboard.dashboard import DashboardPage
from Pages.PIM.add_employee_page import AddEmployeePage
from Pages.PIM.pim import PIMPage


# --------------------------------------------------
# Test Case
# --------------------------------------------------

class TestCase(BaseTest):
    # Test Case 101: Add Employee Test
    # Description: Verify that a new employee can be added to the system with all required details

    def __init__(self, test_data, logger):
        super().__init__(test_data, logger)
        self.test_case_name = "Add Employee Test"

    def setup(self):
        self.logger.info("Test setup started")

        self.login(
            self.test_data["base_url"],
            self.test_data["credentials"]["username"],
            self.test_data["credentials"]["password"]
        )

        self.ready()
        self.logger.info("Login successful")

    def run(self):
        emp = self.test_data["employee"]

        try:
            # Navigate to PIM
            dashboard = DashboardPage(self.driver)
            dashboard.go_to_pim()
            self.ready()

            # Click Add Employee
            pim = PIMPage(self.driver)
            pim.wait_for_pim_page()
            pim.click_add_employee()
            self.ready()

            # Now we are on Add Employee page
            add_emp = AddEmployeePage(self.driver)
            add_emp.wait_for_page()

            # Log employee data
            self.logger.info(f"First Name: {emp['first_name']}")
            self.logger.info(f"Middle Name: {emp['middle_name']}")
            self.logger.info(f"Last Name: {emp['last_name']}")

            add_emp.fill_employee_name(
                emp["first_name"],
                emp["middle_name"],
                emp["last_name"]
            )
            # Check for errors after filling name
            error = self.error()
            if error:
                raise Exception(f"Error after filling employee name: {error}")

            self.logger.info(f"Employee ID: {emp['employee_id']}")
            add_emp.fill_employee_id(emp["employee_id"])
            # Check for errors after filling employee ID
            error = self.error()
            if error:
                raise Exception(f"Error with employee ID: {error}")

            add_emp.enable_login_details()

            self.logger.info(f"Login Username: {emp['login']['username']}")
            add_emp.fill_login_details(
                emp["login"]["username"],
                emp["login"]["password"]
            )
            # Check for errors after filling login credentials
            error = self.error()
            if error:
                raise Exception(f"Error with login credentials: {error}")

            add_emp.save()
            self.ready()

            # Check for errors after saving
            error = self.error()
            if error:
                raise Exception(f"Error during employee creation: {error}")

            self.logger.info("Test completed successfully")

        except Exception as e:
            self.logger.error(f"Test execution failed: {str(e)}")
            raise


    def teardown(self):
        self.logger.info("Teardown started")
        # Only close the browser if the test passed
        if self.result.get("status") == "PASS" and self.browser:
            self.logger.info("Test passed - closing browser")
            self.browser.quit()
        elif self.browser:
            self.logger.info("Test failed - keeping browser open for debugging")

