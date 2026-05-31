"""
Pytest configuration and fixtures for UI automation
"""
import os
import pytest
import allure
from pathlib import Path

from UIAutoFramework.config.settings import settings
from UIAutoFramework.base.web_driver import WebDriverManager
from UIAutoFramework.base.mobile_driver import MobileDriverManager
from UIAutoFramework.utils.logger import get_logger

logger = get_logger("conftest")


# ===== Web Fixtures =====

@pytest.fixture(scope="session")
def web_browser():
    """Session-level browser fixture"""
    return os.getenv("WEB_BROWSER", settings.WEB_BROWSER)


@pytest.fixture(scope="function")
def web_driver(request, web_browser):
    """Function-level WebDriver fixture with auto-cleanup and screenshot on failure"""
    manager = WebDriverManager(
        browser=web_browser,
        headless=settings.WEB_HEADLESS,
        screenshot_dir=str(settings.SCREENSHOT_DIR),
        implicit_wait=settings.WEB_IMPLICIT_WAIT,
        page_load_timeout=settings.WEB_TIMEOUT
    )

    driver = None
    with manager as d:
        driver = d
        yield driver

    # Screenshot on failure
    if request.node.rep_call.failed:
        screenshot_path = os.path.join(settings.SCREENSHOT_DIR, f"FAIL_{request.node.name}")
        try:
            driver.save_screenshot(f"{screenshot_path}.png")
            logger.info(f"Failure screenshot: {screenshot_path}.png")
            with open(f"{screenshot_path}.png", "rb") as f:
                allure.attach(f.read(), name="Failure Screenshot", attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {e}")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Store test result for screenshot fixture"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


# ===== App Fixtures =====

@pytest.fixture(scope="session")
def app_platform():
    """Session-level app platform fixture"""
    return os.getenv("APPIUM_PLATFORM", settings.APPIUM_PLATFORM)


@pytest.fixture(scope="session")
def appium_url():
    """Appium server URL"""
    return os.getenv("APPIUM_URL", settings.APPIUM_URL)


@pytest.fixture(scope="function")
def app_driver(request, app_platform, appium_url):
    """Function-level Appium driver fixture with auto-cleanup and screenshot on failure"""
    manager = MobileDriverManager(
        platform=app_platform,
        platform_version=settings.APPIUM_VERSION,
        device_name=settings.APPIUM_DEVICE_NAME,
        remote_url=appium_url,
        screenshot_dir=str(settings.SCREENSHOT_DIR)
    )

    driver = None
    with manager as d:
        driver = d
        yield driver

    # Screenshot on failure
    if request.node.rep_call.failed:
        screenshot_path = os.path.join(settings.SCREENSHOT_DIR, f"FAIL_{request.node.name}")
        try:
            driver.save_screenshot(f"{screenshot_path}.png")
            logger.info(f"Failure screenshot: {screenshot_path}.png")
            with open(f"{screenshot_path}.png", "rb") as f:
                allure.attach(f.read(), name="Failure Screenshot", attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            logger.error(f"Failed to capture screenshot: {e}")


# ===== Allure Hooks =====

def pytest_configure(config):
    """Configure Allure environment info"""
    config.addinivalue_line(
        "markers", "web: mark test as web UI test"
    )
    config.addinivalue_line(
        "markers", "app: mark test as mobile app test"
    )


def pytest_allure_add_listener():
    """Add custom Allure listener (placeholder for future extensions)"""
    pass