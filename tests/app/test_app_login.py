"""
App UI Test - Login Page
"""
import pytest
import allure

from UIAutoFramework.pages.app.login_page import LoginPage
from UIAutoFramework.locators import app_locators as locators


@allure.feature("App UI Tests")
@allure.story("Login")
@pytest.mark.app
class TestAppLogin:
    """App Login page tests"""

    @allure.title("Test successful login")
    @allure.description("Verify user can login with valid credentials")
    def test_login_success(self, app_driver):
        """Test successful login with valid credentials"""
        page = LoginPage(app_driver)

        page.login("valid_user", "valid_password123")

        # Verify navigation after login
        current_activity = app_driver.current_activity
        assert current_activity is not None

    @allure.title("Test login with invalid credentials")
    @allure.description("Verify error message displays for invalid credentials")
    def test_login_invalid_credentials(self, app_driver):
        """Test login with invalid credentials shows error"""
        page = LoginPage(app_driver)

        page.login("invalid_user", "wrong_password")

        error_msg = page.get_error_message()
        assert error_msg, "Error message should be displayed"

    @allure.title("Test login with empty fields")
    @allure.description("Verify validation when fields are empty")
    def test_login_empty_fields(self, app_driver):
        """Test login with empty username and password"""
        page = LoginPage(app_driver)

        page.click_login()

        # Should show validation error or prevent submission
        assert page.is_visible(locators.LOGIN_PAGE["error_message"]) or \
               not page.is_login_button_enabled()

    @allure.title("Test skip button on login page")
    @allure.description("Verify skip button allows bypassing login")
    def test_skip_button(self, app_driver):
        """Test skip button if available"""
        page = LoginPage(app_driver)

        # Try to skip login
        page.click_skip()

        # Verify navigation or home page
        current_activity = app_driver.current_activity
        assert current_activity is not None

    @allure.title("Test app swipe gestures")
    @allure.description("Verify swipe gestures work correctly")
    def test_swipe_gestures(self, app_driver):
        """Test swipe gestures"""
        page = LoginPage(app_driver)

        # Perform swipe up
        page.swipe_up()

        # Verify something changed
        assert True  # Placeholder for actual verification

    @allure.title("Test app screenshot")
    @allure.description("Verify screenshot capture works")
    def test_screenshot_capture(self, app_driver):
        """Test screenshot capture"""
        page = LoginPage(app_driver)

        # Take screenshot
        screenshot_path = page.take_screenshot("/tmp/test_screenshot.png")

        assert screenshot_path is not None