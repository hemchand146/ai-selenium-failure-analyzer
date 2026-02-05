# Helper utilities for test execution
# Contains shared helper functions used across tests

# --------------------------------------------------
# Imports
# --------------------------------------------------

import time

from selenium.webdriver.common.by import By


# --------------------------------------------------
# Utilities
# --------------------------------------------------

class Helper:
    # Helper methods for test execution
    # Instantiate as: helper = Helper()
    # Then use: helper.ready(driver, logger)

    def ready(self, driver, logger, timeout_minutes=300):
        # Waits until the page is fully loaded
        # Args: driver - Selenium WebDriver instance, logger - Logger instance,
        # timeout_minutes (int) - Max wait time in minutes (default: 300)
        # Returns: bool - True if page loaded successfully
        # Raises: TimeoutError - If page does not complete loading within timeout
        logger.info("Waiting for page to reach stable state")

        timeout_seconds = timeout_minutes * 60
        poll_interval = 5  # seconds
        start_time = time.time()

        while True:
            if time.time() - start_time > timeout_seconds:
                raise TimeoutError(
                    f"Page did not complete loading within {timeout_minutes} minutes"
                )

            try:
                state = driver.execute_script("return document.readyState")

                if state == "complete":
                    logger.info("Page load completed")
                    return True

            except Exception:
                pass

            time.sleep(poll_interval)

    def exists(self, driver, locator_type, locator_value):
        # Check if an element exists on the page
        # Args: driver - Selenium WebDriver instance, locator_type (str) - Type of locator,
        # locator_value (str) - The locator value
        # Returns: bool - True if element exists, False otherwise
        try:
            locator_map = {
                "xpath": By.XPATH,
                "id": By.ID,
                "class": By.CLASS_NAME,
                "css": By.CSS_SELECTOR,
                "name": By.NAME,
                "tag": By.TAG_NAME,
                "link": By.LINK_TEXT,
            }

            locator_type_lower = locator_type.lower()
            if locator_type_lower not in locator_map:
                return False

            driver.find_element(locator_map[locator_type_lower], locator_value)
            return True
        except Exception:
            return False

    def error(self, driver, logger):
        # Get error message from the page if it exists
        # This method is specifically designed for OrangeHRM forms
        # Args: driver - Selenium WebDriver instance, logger - Logger instance
        # Returns: str - Error message text if found, empty string otherwise
        error_message = ""

        # List of XPath selectors for error messages - OrangeHRM specific
        xpath_list = [
            # OrangeHRM form validation errors
            "//span[contains(@class, 'oxd-input-field-error-message')]",  # Inline field errors
            "//span[contains(text(), 'already exists')]",  # "already exists" errors
            "//div[contains(text(), 'already exists')]",  # Alternative div version
            # OrangeHRM toast/alert messages
            "//div[contains(@class, 'oxd-toast')]",
            "//div[contains(@class, 'oxd-alert')]",
            # Generic error messages
            "//span[contains(@class, 'error')]",
            "//*[@class='help-block']",
            "//div[@role='alert']"
        ]

        # Combine all XPath selectors with OR operator
        final_xpath = "|".join(xpath_list)

        # Check if any error element exists
        if self.exists(driver, "xpath", final_xpath):
            try:
                elements = driver.find_elements(By.XPATH, final_xpath)
                if elements:
                    # Get text from first visible error element
                    for element in elements:
                        text = element.text.strip()
                        if text:
                            error_message = text
                            break
            except Exception as e:
                logger.warning(f"Error while extracting error message: {str(e)}")

        return error_message

    def sleep(self, seconds):
        # Sleep for specified seconds
        # Args: seconds (float) - Number of seconds to sleep
        time.sleep(seconds)

