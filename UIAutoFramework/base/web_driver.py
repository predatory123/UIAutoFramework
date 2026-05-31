"""
Selenium WebDriver wrapper with enhanced capabilities
"""
import os
import time
from pathlib import Path
from typing import Optional, Dict
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.common.exceptions import WebDriverException

from ..utils.logger import get_logger

logger = get_logger("WebDriver")


class WebDriverFactory:
    """Factory for creating Selenium WebDriver instances"""

    BROWSER_MAP = {
        "chrome": (webdriver.Chrome, ChromeOptions, ChromeService),
        "firefox": (webdriver.Firefox, FirefoxOptions, FirefoxService),
        "edge": (webdriver.Edge, EdgeOptions, EdgeService),
    }

    @staticmethod
    def create(
        browser: str = "chrome",
        headless: bool = False,
        incognito: bool = False,
        window_size: Optional[tuple] = None,
        page_load_timeout: int = 30,
        implicit_wait: int = 10,
        remote_url: Optional[str] = None,
        options: Optional[Dict] = None
    ) -> webdriver:
        """Create a WebDriver instance"""
        browser = browser.lower()
        if browser not in WebDriverFactory.BROWSER_MAP:
            raise ValueError(f"Unsupported browser: {browser}. Choose from: {list(WebDriverFactory.BROWSER_MAP.keys())}")

        driver_class, options_class, service_class = WebDriverFactory.BROWSER_MAP[browser]
        opts = options_class()

        # Headless mode
        if headless:
            opts.add_argument("--headless")
            opts.add_argument("--disable-gpu")

        # Incognito mode
        if incognito:
            if browser == "chrome":
                opts.add_argument("--incognito")
            elif browser == "firefox":
                opts.add_argument("--private")
            elif browser == "edge":
                opts.add_argument("--inprivate")

        # Custom options
        if options:
            for key, value in options.items():
                opts.add_argument(f"--{key}={value}")

        # Window size
        if window_size:
            opts.add_argument(f"--window-size={window_size[0]},{window_size[1]}")

        # Remote execution (Selenium Grid)
        if remote_url:
            logger.info(f"Connecting to remote WebDriver at {remote_url}")
            return driver_class(remote_url, options=opts)

        # Local execution
        service = service_class()
        driver = driver_class(service=service, options=opts)

        # Timeouts
        driver.set_page_load_timeout(page_load_timeout)
        driver.implicitly_wait(implicit_wait)

        logger.info(f"WebDriver created for {browser} (headless={headless})")
        return driver


class WebDriverManager:
    """Context manager for WebDriver lifecycle"""

    def __init__(
        self,
        browser: str = "chrome",
        headless: bool = False,
        screenshot_dir: Optional[str] = None,
        **kwargs
    ):
        self.browser = browser
        self.headless = headless
        self.screenshot_dir = screenshot_dir or self._default_screenshot_dir()
        self.kwargs = kwargs
        self.driver = None

    @staticmethod
    def _default_screenshot_dir() -> str:
        """Get default screenshot directory"""
        base_dir = Path(__file__).parent.parent.parent
        screenshot_dir = base_dir / "screenshots"
        screenshot_dir.mkdir(exist_ok=True)
        return str(screenshot_dir)

    def __enter__(self):
        self.driver = WebDriverFactory.create(
            browser=self.browser,
            headless=self.headless,
            **self.kwargs
        )
        logger.info(f"WebDriver started for {self.browser}")
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            try:
                self.driver.quit()
                logger.info("WebDriver quit successfully")
            except WebDriverException as e:
                logger.warning(f"Error quitting WebDriver: {e}")

    def capture_screenshot(self, name: str) -> str:
        """Capture screenshot and return filepath"""
        if not self.driver:
            raise RuntimeError("WebDriver not initialized")

        filepath = os.path.join(self.screenshot_dir, f"{name}_{int(time.time())}.png")
        self.driver.save_screenshot(filepath)
        logger.info(f"Screenshot saved: {filepath}")
        return filepath

    @property
    def is_alive(self) -> bool:
        """Check if driver is alive"""
        try:
            if self.driver:
                self.driver.current_url
                return True
        except Exception:
            pass
        return False