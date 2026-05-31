"""
Framework configuration settings
"""
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class Settings:
    """Global configuration for UI automation framework"""

    # Project paths
    BASE_DIR: Path = field(default_factory=lambda: Path(__file__).parent.parent.parent)
    SCREENSHOT_DIR: Path = field(default_factory=lambda: Path(__file__).parent.parent.parent / "screenshots")
    REPORT_DIR: Path = field(default_factory=lambda: Path(__file__).parent.parent.parent / "reports")
    LOG_DIR: Path = field(default_factory=lambda: Path(__file__).parent.parent.parent / "logs")

    # Environment
    ENV: str = os.getenv("TEST_ENV", "dev")

    # Web settings
    WEB_BROWSER: str = os.getenv("WEB_BROWSER", "chrome")
    WEB_HEADLESS: bool = os.getenv("WEB_HEADLESS", "false").lower() == "true"
    WEB_TIMEOUT: int = int(os.getenv("WEB_TIMEOUT", "30"))
    WEB_IMPLICIT_WAIT: int = int(os.getenv("WEB_IMPLICIT_WAIT", "10"))

    # Appium settings
    APPIUM_URL: str = os.getenv("APPIUM_URL", "http://localhost:4723")
    APPIUM_PLATFORM: str = os.getenv("APPIUM_PLATFORM", "android")
    APPIUM_VERSION: Optional[str] = os.getenv("APPIUM_VERSION", None)
    APPIUM_DEVICE_NAME: Optional[str] = os.getenv("APPIUM_DEVICE_NAME", None)

    # Report settings
    REPORT_TITLE: str = "UI 自动化测试报告"
    ENABLE_ALLURE: bool = True

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"

    # Screenshot on failure
    SCREENSHOT_ON_FAILURE: bool = True

    def __post_init__(self):
        """Ensure directories exist"""
        self.SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
        self.REPORT_DIR.mkdir(parents=True, exist_ok=True)
        self.LOG_DIR.mkdir(parents=True, exist_ok=True)


# Global config instance
settings = Settings()