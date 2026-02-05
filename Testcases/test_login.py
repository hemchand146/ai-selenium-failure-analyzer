# Test Case 100: Login Test
# Description: Verify that a user can successfully login with valid credentials

# --------------------------------------------------
# Imports
# --------------------------------------------------

from core import BaseTest


# --------------------------------------------------
# Test Case
# --------------------------------------------------

class TestCase(BaseTest):
    # Test Case 100: Login Test
    # Description: Verify that a user can successfully login with valid credentials

    def __init__(self, test_data, logger):
        super().__init__(test_data, logger)
        self.test_case_name = "Login Test"

    def setup(self):
        self.login(
            self.test_data["base_url"],
            self.test_data["credentials"]["username"],
            self.test_data["credentials"]["password"]
        )
        self.ready()

    def run(self):
        if "/dashboard/index" not in self.driver.current_url:
            raise Exception("Login failed")

        self.logger.info("Login successful")

    def teardown(self):
        self.logger.info("Teardown started")
        # Only close the browser if the test passed
        if self.result.get("status") == "PASS" and self.browser:
            self.logger.info("Test passed - closing browser")
            self.browser.quit()
        elif self.browser:
            self.logger.info("Test failed - keeping browser open for debugging")

