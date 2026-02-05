# Test Case 103: Candidates Search Test
# Description: Verify that the recruitment candidates search functionality works with multiple filters

# --------------------------------------------------
# Imports
# --------------------------------------------------

from core import BaseTest
from Pages.Dashboard.dashboard import DashboardPage
from Pages.Recruitment.candidates_page import CandidatesPage


# --------------------------------------------------
# Test Case
# --------------------------------------------------

class TestCase(BaseTest):
    # Test Case 103: Candidates Search Test
    # Description: Verify that the recruitment candidates search functionality works with multiple filters

    def __init__(self, test_data, logger):
        super().__init__(test_data, logger)
        self.test_case_name = "Candidates Search Test"

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
        candidates_data = self.test_data["candidates_search"]

        try:
            # Navigate to Recruitment module
            dashboard = DashboardPage(self.driver)
            dashboard.go_to_recruitment()
            self.ready()

            # Wait for Candidates page to load
            candidates = CandidatesPage(self.driver)
            candidates.wait_for_candidates_page()

            # Select Job Title
            if candidates_data.get("job_title"):
                self.logger.info(f"Job Title: {candidates_data['job_title']}")
                candidates.select_job_title(candidates_data["job_title"])
                self.ready()

            # Select Vacancy
            if candidates_data.get("vacancy"):
                self.logger.info(f"Vacancy: {candidates_data['vacancy']}")
                candidates.select_vacancy(candidates_data["vacancy"])
                self.ready()

            # Select Hiring Manager
            if candidates_data.get("hiring_manager"):
                self.logger.info(f"Hiring Manager: {candidates_data['hiring_manager']}")
                candidates.select_hiring_manager(candidates_data["hiring_manager"])
                self.ready()

            # Select Status
            if candidates_data.get("status"):
                self.logger.info(f"Status: {candidates_data['status']}")
                candidates.select_status(candidates_data["status"])
                self.ready()

            # Enter Keywords
            if candidates_data.get("keywords"):
                self.logger.info(f"Keywords: {candidates_data['keywords']}")
                candidates.enter_keywords(candidates_data["keywords"])
                self.ready()

            # Enter Application Date From
            if candidates_data.get("date_from"):
                self.logger.info(f"Date From: {candidates_data['date_from']}")
                candidates.enter_application_date_from(candidates_data["date_from"])
                self.ready()

            # Enter Application Date To
            if candidates_data.get("date_to"):
                self.logger.info(f"Date To: {candidates_data['date_to']}")
                candidates.enter_application_date_to(candidates_data["date_to"])
                self.ready()

            # Select Method of Application
            if candidates_data.get("method_of_application"):
                self.logger.info(f"Method of Application: {candidates_data['method_of_application']}")
                candidates.select_method_of_application(candidates_data["method_of_application"])
                self.ready()

            # Click Search
            candidates.click_search()
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
        # Only close the browser if the test passed
        # if self.result.get("status") == "PASS" and self.browser:
        #     self.logger.info("Test passed - closing browser")
        #     self.browser.quit()
        # elif self.browser:
        #     self.logger.info("Test failed - keeping browser open for debugging")

