# Test Case 102: Directory Search Test
# Description: Verify that the directory search functionality works correctly with employee filters

# --------------------------------------------------
# Imports
# --------------------------------------------------

from core import BaseTest
from Pages.Dashboard.dashboard import DashboardPage
from Pages.Directory.directory_page import DirectoryPage


# --------------------------------------------------
# Test Case
# --------------------------------------------------

class TestCase(BaseTest):
    # Test Case 102: Directory Search Test
    # Description: Verify that the directory search functionality works correctly with employee filters

    def __init__(self, test_data, logger):
        super().__init__(test_data, logger)
        self.test_case_name = "Directory Search Test"

    def setup(self):
        self.login(
            self.test_data["base_url"],
            self.test_data["credentials"]["username"],
            self.test_data["credentials"]["password"]
        )
        self.ready()

    def run(self):
        directory_data = self.test_data["directory_search"]

        try:
            # Navigate to Directory module
            dashboard = DashboardPage(self.driver)
            dashboard.go_to_directory()
            self.ready()

            # Wait for Directory page to load
            directory = DirectoryPage(self.driver)
            directory.wait_for_directory_page()

            # Enter Employee Name
            if directory_data.get("employee_name"):
                directory.enter_employee_name(directory_data["employee_name"])
                self.ready()

            # Select Job Title
            if directory_data.get("job_title"):
                directory.select_job_title(directory_data["job_title"])
                self.ready()

            # Select Location
            if directory_data.get("location"):
                directory.select_location(directory_data["location"])
                self.ready()

            # Click Search
            directory.click_search()
            self.ready()

            # Check for errors
            error = self.error()
            if error:
                raise Exception(f"Error during search: {error}")

            self.logger.info("Test completed successfully")

        except Exception as e:
            self.logger.error(f"Test execution failed: {str(e)}")
            raise

    def teardown(self):
        self.logger.info("Teardown started")

