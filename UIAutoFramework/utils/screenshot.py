"""
Screenshot utility for test failure documentation
"""
import os
import time
from pathlib import Path
from typing import Optional

import allure

from .logger import get_logger

logger = get_logger("Screenshot")


class ScreenshotHelper:
    """Helper for capturing and attaching screenshots to Allure reports"""

    def __init__(self, driver, screenshot_dir: Optional[str] = None):
        self.driver = driver
        self.screenshot_dir = screenshot_dir or self._default_screenshot_dir()
        Path(self.screenshot_dir).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _default_screenshot_dir() -> str:
        base_dir = Path(__file__).parent.parent.parent
        screenshot_dir = base_dir / "screenshots"
        screenshot_dir.mkdir(exist_ok=True)
        return str(screenshot_dir)

    def capture(self, name: str, attach_to_allure: bool = True) -> str:
        """Capture screenshot and optionally attach to Allure report"""
        timestamp = int(time.time() * 1000)
        filename = f"{name}_{timestamp}.png"
        filepath = os.path.join(self.screenshot_dir, filename)

        try:
            self.driver.save_screenshot(filepath)
            logger.info(f"Screenshot captured: {filepath}")

            if attach_to_allure:
                with open(filepath, "rb") as f:
                    allure.attach(
                        f.read(),
                        name=name,
                        attachment_type=allure.attachment_type.PNG
                    )

            return filepath
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {e}")
            return ""

    def capture_element(self, element, name: str, attach_to_allure: bool = True) -> str:
        """Capture screenshot of specific element"""
        timestamp = int(time.time() * 1000)
        filename = f"{name}_{timestamp}.png"
        filepath = os.path.join(self.screenshot_dir, filename)

        try:
            element.screenshot(filepath)
            logger.info(f"Element screenshot captured: {filepath}")

            if attach_to_allure:
                with open(filepath, "rb") as f:
                    allure.attach(
                        f.read(),
                        name=name,
                        attachment_type=allure.attachment_type.PNG
                    )

            return filepath
        except Exception as e:
            logger.error(f"Failed to capture element screenshot: {e}")
            return ""