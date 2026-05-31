"""
Base Page Object - common interface for Web and App automation
"""
import time
from typing import Optional, Union
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class BasePageWeb:
    """Base class for Web page objects using Selenium"""

    def __init__(self, driver):
        self.driver = driver
        self.timeout = 10
        self.poll_frequency = 0.5

    def find_element(self, locator: tuple, timeout: Optional[int] = None) -> Union:
        """Find element with explicit wait"""
        wait = WebDriverWait(
            self.driver,
            timeout or self.timeout,
            poll_frequency=self.poll_frequency
        )
        return wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator: tuple, timeout: Optional[int] = None) -> list:
        """Find multiple elements with explicit wait"""
        wait = WebDriverWait(
            self.driver,
            timeout or self.timeout,
            poll_frequency=self.poll_frequency
        )
        return wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator: tuple, timeout: Optional[int] = None):
        """Click element after it's clickable"""
        wait = WebDriverWait(
            self.driver,
            timeout or self.timeout,
            poll_frequency=self.poll_frequency
        )
        element = wait.until(EC.element_to_be_clickable(locator))
        element.click()
        return element

    def input_text(self, locator: tuple, text: str, clear_first: bool = True):
        """Input text into element"""
        element = self.find_element(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)
        return element

    def get_text(self, locator: tuple, timeout: Optional[int] = None) -> str:
        """Get element text"""
        element = self.find_element(locator, timeout)
        return element.text

    def get_attribute(self, locator: tuple, attr_name: str) -> Optional[str]:
        """Get element attribute value"""
        element = self.find_element(locator)
        return element.get_attribute(attr_name)

    def is_visible(self, locator: tuple, timeout: Optional[int] = None) -> bool:
        """Check if element is visible"""
        try:
            self.find_element(locator, timeout)
            return True
        except TimeoutException:
            return False

    def is_enabled(self, locator: tuple) -> bool:
        """Check if element is enabled"""
        element = self.find_element(locator)
        return element.is_enabled()

    def wait_for_url_contains(self, text: str, timeout: Optional[int] = None):
        """Wait for URL to contain specific text"""
        wait = WebDriverWait(
            self.driver,
            timeout or self.timeout,
            poll_frequency=self.poll_frequency
        )
        return wait.until(EC.url_contains(text))

    def wait_for_element_visible(self, locator: tuple, timeout: Optional[int] = None):
        """Wait until element is visible"""
        wait = WebDriverWait(
            self.driver,
            timeout or self.timeout,
            poll_frequency=self.poll_frequency
        )
        return wait.until(EC.visibility_of_element_located(locator))

    def submit(self, locator: tuple):
        """Submit form"""
        element = self.find_element(locator)
        element.submit()

    def take_screenshot(self, filepath: str):
        """Take screenshot"""
        self.driver.save_screenshot(filepath)


class BasePageApp:
    """Base class for App page objects using Appium"""

    def __init__(self, driver):
        self.driver = driver
        self.timeout = 10
        self.poll_frequency = 0.5

    def find_element(self, locator: tuple, timeout: Optional[int] = None):
        """Find element with explicit wait"""
        wait = WebDriverWait(
            self.driver,
            timeout or self.timeout,
            poll_frequency=self.poll_frequency
        )
        return wait.until(lambda d: d.find_element(*locator))

    def find_elements(self, locator: tuple, timeout: Optional[int] = None) -> list:
        """Find multiple elements"""
        wait = WebDriverWait(
            self.driver,
            timeout or self.timeout,
            poll_frequency=self.poll_frequency
        )
        return wait.until(lambda d: d.find_elements(*locator))

    def click(self, locator: tuple, timeout: Optional[int] = None):
        """Click element"""
        element = self.find_element(locator, timeout)
        element.click()
        return element

    def input_text(self, locator: tuple, text: str, clear_first: bool = True):
        """Input text into element"""
        element = self.find_element(locator)
        if clear_first:
            element.clear()
        element.set_value(text)
        return element

    def get_text(self, locator: tuple, timeout: Optional[int] = None) -> str:
        """Get element text"""
        element = self.find_element(locator, timeout)
        return element.text

    def is_visible(self, locator: tuple, timeout: Optional[int] = None) -> bool:
        """Check if element is visible"""
        try:
            self.find_element(locator, timeout)
            return True
        except Exception:
            return False

    def swipe(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: int = 500):
        """Swipe gesture"""
        action = TouchAction(self.driver)
        action.press(x=start_x, y=start_y).wait(duration).release().perform()

    def tap(self, x: int, y: int):
        """Tap gesture"""
        action = TouchAction(self.driver)
        action.tap(x=x, y=y).perform()

    def long_press(self, locator: tuple, duration: int = 1000):
        """Long press gesture"""
        element = self.find_element(locator)
        action = TouchAction(self.driver)
        action.long_press(element, duration=duration).release().perform()

    def hide_keyboard(self):
        """Hide keyboard if visible"""
        try:
            self.driver.hide_keyboard()
        except Exception:
            pass

    def take_screenshot(self, filepath: str):
        """Take screenshot"""
        self.driver.save_screenshot(filepath)


# Import TouchAction for Appium
try:
    from appium.webdriver.common.touch_action import TouchAction
except ImportError:
    TouchAction = None