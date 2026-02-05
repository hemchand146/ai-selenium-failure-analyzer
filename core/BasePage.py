# BasePage class - Contains common page object functions
# All page object classes should inherit from this class

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Tuple
import logging


class BasePage:
    # Base class for all page objects
    # Provides common methods for element interaction and waiting

    def __init__(self, driver, wait_timeout=15):
        # Initialize BasePage with driver and wait timeout
        # Args: driver - Selenium WebDriver instance, wait_timeout (int) - Explicit wait timeout in seconds (default: 15)
        self.driver = driver
        self.wait = WebDriverWait(driver, wait_timeout)
        self.logger = logging.getLogger(self.__class__.__name__)

    def find_element(self, locator: Tuple[str, str]):
        # Find and return a single element
        # Args: locator (tuple) - Tuple of (By.*, locator_value)
        # Returns: WebElement - The found element
        return self.driver.find_element(*locator)

    def find_elements(self, locator: Tuple[str, str]):
        # Find and return multiple elements
        # Args: locator (tuple) - Tuple of (By.*, locator_value)
        # Returns: list - List of found elements
        return self.driver.find_elements(*locator)

    def wait_for_element_visible(self, locator: Tuple[str, str]):
        # Wait for element to be visible
        # Args: locator (tuple) - Tuple of (By.*, locator_value)
        # Returns: WebElement - The visible element
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_for_element_clickable(self, locator: Tuple[str, str]):
        # Wait for element to be clickable
        # Args: locator (tuple) - Tuple of (By.*, locator_value)
        # Returns: WebElement - The clickable element
        return self.wait.until(EC.element_to_be_clickable(locator))

    def wait_for_element_present(self, locator: Tuple[str, str]):
        # Wait for element to be present in DOM
        # Args: locator (tuple) - Tuple of (By.*, locator_value)
        # Returns: WebElement - The present element
        return self.wait.until(EC.presence_of_element_located(locator))

    def wait_for_elements_visible(self, locator: Tuple[str, str]):
        # Wait for elements to be visible
        # Args: locator (tuple) - Tuple of (By.*, locator_value)
        # Returns: list - List of visible elements
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    def click_element(self, locator: Tuple[str, str]) -> None:
        # Wait for element to be clickable and click it
        # Args: locator (tuple) - Tuple of (By.*, locator_value)
        element = self.wait_for_element_clickable(locator)
        element.click()

    def send_keys_to_element(self, locator: Tuple[str, str], keys: str) -> None:
        # Wait for element and send keys to it
        # Args: locator (tuple) - Tuple of (By.*, locator_value), keys (str) - Text to send to the element
        element = self.wait_for_element_visible(locator)
        element.send_keys(keys)

    def clear_and_send_keys(self, locator: Tuple[str, str], keys: str) -> None:
        # Clear element and send keys to it
        # Args: locator (tuple) - Tuple of (By.*, locator_value), keys (str) - Text to send to the element
        element = self.wait_for_element_visible(locator)
        element.clear()
        element.send_keys(keys)

    def get_element_text(self, locator: Tuple[str, str]) -> str:
        # Get text from an element
        # Args: locator (tuple) - Tuple of (By.*, locator_value)
        # Returns: str - Text content of the element
        element = self.wait_for_element_visible(locator)
        return element.text

    def is_element_visible(self, locator: Tuple[str, str]) -> bool:
        # Check if element is visible (without waiting)
        # Args: locator (tuple) - Tuple of (By.*, locator_value)
        # Returns: bool - True if visible, False otherwise
        try:
            element = self.driver.find_element(*locator)
            return element.is_displayed()
        except Exception:
            return False

    def is_element_present(self, locator: Tuple[str, str]) -> bool:
        # Check if element exists in DOM (without waiting)
        # Args: locator (tuple) - Tuple of (By.*, locator_value)
        # Returns: bool - True if present, False otherwise
        try:
            self.driver.find_element(*locator)
            return True
        except Exception:
            return False

    def scroll_to_element(self, locator: Tuple[str, str]) -> None:
        # Scroll to element location
        # Args: locator (tuple) - Tuple of (By.*, locator_value)
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def get_element_attribute(self, locator: Tuple[str, str], attribute_name: str) -> str:
        # Get attribute value from an element
        # Args: locator (tuple) - Tuple of (By.*, locator_value), attribute_name (str) - Name of the attribute
        # Returns: str - Attribute value
        element = self.wait_for_element_visible(locator)
        return element.get_attribute(attribute_name)

    def switch_to_frame(self, locator: Tuple[str, str]) -> None:
        # Switch to iframe
        # Args: locator (tuple) - Tuple of (By.*, locator_value)
        frame = self.wait_for_element_present(locator)
        self.driver.switch_to.frame(frame)

    def switch_to_parent_frame(self) -> None:
        # Switch back to parent frame
        self.driver.switch_to.parent_frame()

    def switch_to_default_content(self) -> None:
        # Switch to default content (exit all frames)
        self.driver.switch_to.default_content()

