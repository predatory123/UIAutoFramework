"""
Web element locators - centralized locator definitions
"""

# Login page locators
LOGIN_PAGE = {
    "username_input": ("id", "username"),
    "password_input": ("id", "password"),
    "login_button": ("id", "login-btn"),
    "error_message": ("css", ".error-message"),
    "remember_me": ("id", "remember-me"),
    "forgot_password": ("css", ".forgot-password"),
    "logo": ("css", ".logo"),
}

# Common web locators
COMMON = {
    "loading_spinner": ("css", ".loading, .spinner"),
    "modal_dialog": ("css", ".modal"),
    "toast_message": ("css", ".toast, .notification"),
    "confirm_button": ("xpath", "//button[contains(text(), 'Confirm')]"),
    "cancel_button": ("xpath", "//button[contains(text(), 'Cancel')]"),
    "close_button": ("css", ".close, .btn-close"),
    "search_input": ("css", "input[type='search'], input[placeholder*='Search']"),
    "submit_button": ("css", "button[type='submit'], input[type='submit']"),
}