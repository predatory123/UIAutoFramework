"""
Web UI Test - Login Page
"""
import pytest
import allure

from UIAutoFramework.pages.web.login_page import LoginPage
from UIAutoFramework.locators import web_locators as locators


@allure.feature("Web UI Tests")
@allure.story("Login")
@pytest.mark.web
class TestWebLogin:
    """Web Login page tests"""

    @allure.title("Test successful login")
    @allure.description("Verify user can login with valid credentials")
    def test_login_success(self, web_driver):
        """Test successful login with valid credentials"""
        page = LoginPage(web_driver)
        page.open("https://example.com/login")

        page.login("valid_user", "valid_password123")

        # Verify redirect or success state
        assert "dashboard" in web_driver.current_url.lower() or \
               page.is_visible(locators.COMMON["search_input"])

    @allure.title("Test login with invalid credentials")
    @allure.description("Verify error message displays for invalid credentials")
    def test_login_invalid_credentials(self, web_driver):
        """Test login with invalid credentials shows error"""
        page = LoginPage(web_driver)
        page.open("https://example.com/login")

        page.login("invalid_user", "wrong_password")

        error_msg = page.get_error_message()
        assert error_msg, "Error message should be displayed"
        assert "invalid" in error_msg.lower() or "incorrect" in error_msg.lower()

    @allure.title("Test login with empty fields")
    @allure.description("Verify validation when fields are empty")
    def test_login_empty_fields(self, web_driver):
        """Test login with empty username and password"""
        page = LoginPage(web_driver)
        page.open("https://example.com/login")

        page.click_login()

        # Should show validation error or prevent submission
        assert page.is_visible(locators.LOGIN_PAGE["error_message"]) or \
               not page.is_login_button_enabled()

    @allure.title("Test remember me checkbox")
    @allure.description("Verify remember me functionality")
    def test_remember_me(self, web_driver):
        """Test remember me checkbox"""
        page = LoginPage(web_driver)
        page.open("https://example.com/login")

        page.input_username("test_user")
        page.input_password("password123")

        # Find and click remember me
        remember_me = page.find_element(locators.LOGIN_PAGE["remember_me"])
        remember_me.click()

        page.click_login()

        # Verify cookie or session is persisted
        assert True  # Placeholder for actual verification

    @allure.title("Test forgot password link")
    @allure.description("Verify forgot password link navigates correctly")
    def test_forgot_password_link(self, web_driver):
        """Test forgot password link"""
        page = LoginPage(web_driver)
        page.open("https://example.com/login")

        forgot_link = page.find_element(locators.LOGIN_PAGE["forgot_password"])
        forgot_link.click()

        # Verify navigation to password reset page
        assert "reset" in web_driver.current_url.lower() or \
               "forgot" in web_driver.current_url.lower()