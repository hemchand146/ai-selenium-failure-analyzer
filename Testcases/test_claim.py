# Test Case 104: Claim Test
# Description: Verify that the claim search functionality works with various filters

# --------------------------------------------------
# Imports
# --------------------------------------------------

from datetime import datetime, timedelta
import random

from core import BaseTest
from Pages.Claim.claim_page import ClaimPage
from Pages.Dashboard.dashboard import DashboardPage


# --------------------------------------------------
# Test Case
# --------------------------------------------------

class TestCase(BaseTest):
    # Test Case 104: Claim Test
    # Description: Verify that the claim search functionality works with various filters

    def __init__(self, test_data, logger):
        super().__init__(test_data, logger)
        self.test_case_name = "Claim Test"

    def setup(self):
        self.logger.info("Test setup started")

        self.login(
            self.test_data["base_url"],
            self.test_data["credentials"]["username"],
            self.test_data["credentials"]["password"]
        )

        self.ready()
        self.logger.info("Login successful")

        self.claim = ClaimPage(self.driver)
        self.dashboard = DashboardPage(self.driver)

    def run(self):
        claim_data = self.test_data["claim"]

        try:
            # Navigate to Claim module
            self.dashboard.go_to_claim()
            self.ready()

            # Wait for Claim page to load
            self.claim.wait_for_claim_page()
            self.logger.info("Claim page loaded")

            # Enter Employee Name - SKIPPED FOR NOW
            # employee_name = claim_data.get("employee_name")
            # if employee_name:
            #     claim.enter_employee_name(employee_name)
            #     self.logger.info(f"Entered employee name: {employee_name}")
            #     self.ready()

            # Select Event Name
            event_name = claim_data.get("event_name")
            if event_name:
                self.claim.select_event_name(event_name)
                self.logger.info(f"Selected event name: {event_name}")
                self.ready()

            # Select Status
            status = claim_data.get("status")
            if status:
                self.claim.select_status(status)
                self.logger.info(f"Selected status: {status}")
                self.ready()

            # Generate random dates
            from_date = self.generate_random_date()
            to_date = self.generate_random_date(from_date)

            # Enter From Date
            self.claim.enter_from_date(from_date)
            self.logger.info(f"Entered from date: {from_date}")
            self.ready()

            # Enter To Date
            self.claim.enter_to_date(to_date)
            self.logger.info(f"Entered to date: {to_date}")
            self.ready()

            # Click Search
            self.claim.click_search()
            self.logger.info("Clicked Search button")
            self.ready()

            # Check for errors
            error = self.error()
            if error:
                raise Exception(f"Error occurred: {error}")

            self.logger.info("Claim search completed successfully")

        except Exception as e:
            self.logger.error(f"Error in test: {str(e)}")
            self.result["status"] = "FAIL"
            self.result["error"] = str(e)
            raise

    def generate_random_date(self, start_date=None):
        # Generate a random date in dd-mm-yyyy format
        # Args: start_date (str) - Optional start date in dd-mm-yyyy format
        # Returns: str - Random date in dd-mm-yyyy format
        if start_date:
            # Parse the start date
            date_obj = datetime.strptime(start_date, "%d-%m-%Y")
            # Add random days (1-30)
            random_days = random.randint(1, 30)
            random_date = date_obj + timedelta(days=random_days)
        else:
            # Generate a date in the past (last 365 days)
            days_ago = random.randint(1, 365)
            random_date = datetime.now() - timedelta(days=days_ago)

        return random_date.strftime("%d-%m-%Y")

    def teardown(self):
        self.logger.info("Teardown started")
        # Only close the browser if the test passed
        if self.result.get("status") == "PASS" and self.browser:
            self.logger.info("Test passed - closing browser")
            self.browser.quit()
        elif self.browser:
            self.logger.info("Test failed - keeping browser open for debugging")

