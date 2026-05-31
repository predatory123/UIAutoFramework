"""
Web Login Page Object
"""
from ...base.base_page import BasePageWeb
from ...locators import web_locators as locators


class LoginPage(BasePageWeb):
    """Page Object for Web Login page"""

    def __init__(self, driver):
        super().__init__(driver)
        self.locators = locators.LOGIN_PAGE

    def open(self, url: str):
        """Open login page"""
        self.driver.get(url)

    def input_username(self, username: str):
        """Enter username"""
        self.input_text(self.locators["username_input"], username)

    def input_password(self, password: str):
        """Enter password"""
        self.input_text(self.locators["password_input"], password)

    def click_login(self):
        """Click login button"""
        self.click(self.locators["login_button"])

    def login(self, username: str, password: str):
        """Perform complete login flow"""
        self.input_username(username)
        self.input_password(password)
        self.click_login()

    def get_error_message(self) -> str:
        """Get error message text"""
        if self.is_visible(self.locators["error_message"]):
            return self.get_text(self.locators["error_message"])
        return ""

    def is_login_button_enabled(self) -> bool:
        """Check if login button is enabled"""
        return self.is_enabled(self.locators["login_button"])

    def is_login_page_loaded(self) -> bool:
        """Check if login page is loaded"""
        return self.is_visible(self.locators["username_input"]) or \
               self.is_visible(self.locators["login_button"])