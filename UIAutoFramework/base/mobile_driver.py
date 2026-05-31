"""
Appium Mobile Driver wrapper with enhanced capabilities
"""
import os
import time
from pathlib import Path
from typing import Optional, Dict

from appium import webdriver as appium_driver
from appium.webdriver.webdriver import WebDriver as AppiumWebDriver
from appium.common.exceptions import WebDriverException

from ..utils.logger import get_logger

logger = get_logger("MobileDriver")


class MobileDriverFactory:
    """Factory for creating Appium driver instances"""

    @staticmethod
    def create(
        platform: str = "android",
        platform_version: Optional[str] = None,
        device_name: Optional[str] = None,
        app_package: Optional[str] = None,
        app_activity: Optional[str] = None,
        app_path: Optional[str] = None,
        remote_url: str = "http://localhost:4723",
        timeout: int = 30,
        new_command_timeout: int = 300,
        auto_grant_permissions: bool = True,
        allow_delay: bool = True,
        capabilities: Optional[Dict] = None
    ) -> AppiumWebDriver:
        """Create an Appium driver instance"""
        platform = platform.lower()

        if capabilities:
            caps = capabilities
        else:
            caps = {
                "platformName": platform.capitalize(),
                "browserName": "",
                "autoGrantPermissions": auto_grant_permissions,
                "allowDelay": allow_delay,
                "newCommandTimeout": new_command_timeout,
            }

            if platform_version:
                caps["platformVersion"] = platform_version
            if device_name:
                caps["deviceName"] = device_name
            if app_package:
                caps["appPackage"] = app_package
            if app_activity:
                caps["appActivity"] = app_activity
            if app_path:
                caps["app"] = app_path

        logger.info(f"Creating Appium driver for {platform}")
        logger.info(f"Capabilities: {caps}")

        driver = appium_driver.Remote(remote_url, caps)
        driver.timeout = timeout

        logger.info("Appium driver created successfully")
        return driver


class MobileDriverManager:
    """Context manager for Appium driver lifecycle"""

    def __init__(
        self,
        platform: str = "android",
        platform_version: Optional[str] = None,
        device_name: Optional[str] = None,
        app_package: Optional[str] = None,
        app_activity: Optional[str] = None,
        app_path: Optional[str] = None,
        remote_url: str = "http://localhost:4723",
        screenshot_dir: Optional[str] = None,
        **kwargs
    ):
        self.platform = platform
        self.platform_version = platform_version
        self.device_name = device_name
        self.app_package = app_package
        self.app_activity = app_activity
        self.app_path = app_path
        self.remote_url = remote_url
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

    def __enter__(self) -> AppiumWebDriver:
        self.driver = MobileDriverFactory.create(
            platform=self.platform,
            platform_version=self.platform_version,
            device_name=self.device_name,
            app_package=self.app_package,
            app_activity=self.app_activity,
            app_path=self.app_path,
            remote_url=self.remote_url,
            **self.kwargs
        )
        logger.info(f"MobileDriver started for {self.platform}")
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            try:
                self.driver.quit()
                logger.info("MobileDriver quit successfully")
            except WebDriverException as e:
                logger.warning(f"Error quitting MobileDriver: {e}")

    def capture_screenshot(self, name: str) -> str:
        """Capture screenshot and return filepath"""
        if not self.driver:
            raise RuntimeError("MobileDriver not initialized")

        filepath = os.path.join(self.screenshot_dir, f"{name}_{int(time.time())}.png")
        self.driver.save_screenshot(filepath)
        logger.info(f"Screenshot saved: {filepath}")
        return filepath

    @property
    def is_alive(self) -> bool:
        """Check if driver is alive"""
        try:
            if self.driver:
                self.driver.current_activity
                return True
        except Exception:
            pass
        return False

    def install_app(self, app_path: str):
        """Install app on device"""
        if self.driver:
            self.driver.install_app(app_path)
            logger.info(f"App installed: {app_path}")

    def uninstall_app(self, app_package: str):
        """Uninstall app from device"""
        if self.driver:
            self.driver.remove_app(app_package)
            logger.info(f"App uninstalled: {app_package}")

    def reset_app(self):
        """Reset app (clear data)"""
        if self.driver:
            self.driver.reset()
            logger.info("App reset")

    def start_activity(self, app_package: str, app_activity: str):
        """Start specific activity"""
        if self.driver:
            self.driver.start_activity(app_package, app_activity)
            logger.info(f"Started activity: {app_package}/{app_activity}")

    def swipe(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: int = 500):
        """Perform swipe gesture"""
        if self.driver:
            action = self.driver.TouchAction(self.driver)
            action.press(x=start_x, y=start_y).wait(duration).release().perform()

    def swipe_left(self, duration: int = 500):
        """Swipe left"""
        if self.driver:
            size = self.driver.get_window_size()
            start_x = size["width"] * 0.9
            start_y = size["height"] * 0.5
            end_x = size["width"] * 0.1
            self.swipe(start_x, start_y, end_x, start_y, duration)

    def swipe_right(self, duration: int = 500):
        """Swipe right"""
        if self.driver:
            size = self.driver.get_window_size()
            start_x = size["width"] * 0.1
            start_y = size["height"] * 0.5
            end_x = size["width"] * 0.9
            self.swipe(start_x, start_y, end_x, start_y, duration)

    def swipe_up(self, duration: int = 500):
        """Swipe up"""
        if self.driver:
            size = self.driver.get_window_size()
            start_x = size["width"] * 0.5
            start_y = size["height"] * 0.9
            end_y = size["height"] * 0.1
            self.swipe(start_x, start_y, start_x, end_y, duration)

    def swipe_down(self, duration: int = 500):
        """Swipe down"""
        if self.driver:
            size = self.driver.get_window_size()
            start_x = size["width"] * 0.5
            start_y = size["height"] * 0.1
            end_y = size["height"] * 0.9
            self.swipe(start_x, start_y, start_x, end_y, duration)