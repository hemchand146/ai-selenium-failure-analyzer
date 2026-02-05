# Candidates page object
# Page object for OrangeHRM Candidates search and filter page

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

class CandidatesPage(BasePage):
    # Page object for OrangeHRM Candidates search and filter page

    def __init__(self, driver):
        # Initialize CandidatesPage with driver
        super().__init__(driver)
        self.dropdown_helper = DropdownHelper(driver)

    def wait_for_candidates_page(self):
        # Wait for Candidates page to load
        # Wait for candidates filter section with h5 title
        candidates_header = (By.XPATH, "//h5[normalize-space()='Candidates']")
        self.wait_for_element_visible(candidates_header)
        time.sleep(2)

    def select_job_title(self, job_title):
        # Select Job Title from dropdown
        # Args: job_title (str) - Job title to select
        self.dropdown_helper.select_dropdown_by_label('Job Title', job_title)

    def select_vacancy(self, vacancy):
        # Select Vacancy from dropdown
        # Args: vacancy (str) - Vacancy to select
        self.dropdown_helper.select_dropdown_by_label('Vacancy', vacancy)

    def select_hiring_manager(self, hiring_manager):
        # Select Hiring Manager from dropdown
        # Args: hiring_manager (str) - Hiring manager name to select
        self.dropdown_helper.select_dropdown_by_label('Hiring Manager', hiring_manager)

    def select_status(self, status):
        # Select Status from dropdown
        # Args: status (str) - Status to select
        self.dropdown_helper.select_dropdown_by_label('Status', status)

    def select_method_of_application(self, method):
        # Select Method of Application from dropdown
        # Args: method (str) - Application method to select
        self.dropdown_helper.select_dropdown_by_label('Method of Application', method)

    def enter_candidate_name(self, candidate_name):
        # Enter Candidate Name in autocomplete field
        # Args: candidate_name (str) - Candidate name to search
        candidate_input = (By.XPATH, "//label[text()='Candidate Name']/following::input[@placeholder='Type for hints...'][1]")
        input_field = self.wait_for_element_visible(candidate_input)
        input_field.click()
        input_field.send_keys(candidate_name)
        time.sleep(1)

    def enter_keywords(self, keywords):
        # Enter Keywords in the keywords field
        # Args: keywords (str) - Comma-separated keywords to search
        keywords_input = (By.XPATH, "//label[text()='Keywords']/following::input[@placeholder='Enter comma seperated words...'][1]")
        input_field = self.wait_for_element_visible(keywords_input)
        input_field.click()
        input_field.clear()
        input_field.send_keys(keywords)
        time.sleep(0.5)

    def enter_application_date_from(self, date_from):
        # Enter 'From' date in Date of Application field using calendar picker
        # Args: date_from (str) - Date in format YYYY-MM-DD (e.g., "2025-01-01")
        date_from_input = (By.XPATH, "//label[text()='Date of Application']/following::input[@placeholder='From'][1]")
        input_field = self.wait_for_element_visible(date_from_input)
        input_field.click()
        time.sleep(0.5)
        input_field.clear()
        input_field.send_keys(date_from)
        time.sleep(0.5)

    def enter_application_date_to(self, date_to):
        # Enter 'To' date in Date of Application field using calendar picker
        # Args: date_to (str) - Date in format YYYY-MM-DD (e.g., "2026-02-04")
        date_to_input = (By.XPATH, "//label[text()='Date of Application']/following::input[@placeholder='To'][1]")
        input_field = self.wait_for_element_visible(date_to_input)
        input_field.click()
        time.sleep(0.5)
        input_field.clear()
        input_field.send_keys(date_to)
        time.sleep(0.5)

    def click_search(self):
        # Click the Search button
        search_button = (By.XPATH, "//*[@id='app']/div[1]/div[2]/div[2]/div/div[1]/div[2]/form/div[4]/button[2]")
        btn = self.wait_for_element_clickable(search_button)
        btn.click()
        time.sleep(1)

    def click_reset(self):
        # Click the Reset button
        reset_button = (By.XPATH, "//*[@id='app']/div[1]/div[2]/div[2]/div/div[1]/div[2]/form/div[4]/button[1]")
        btn = self.wait_for_element_clickable(reset_button)
        btn.click()
        time.sleep(0.5)
