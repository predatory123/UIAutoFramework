"""
App element locators - centralized locator definitions for mobile
"""

# Login page locators (Android example)
LOGIN_PAGE = {
    "username_input": ("id", "com.example.app:id/username"),
    "password_input": ("id", "com.example.app:id/password"),
    "login_button": ("id", "com.example.app:id/login_btn"),
    "error_message": ("id", "com.example.app:id/error_text"),
    "remember_me": ("id", "com.example.app:id/remember_me"),
    "skip_button": ("id", "com.example.app:id/skip"),
    "logo": ("id", "com.example.app:id/logo"),
}

# Common app locators
COMMON = {
    "loading_indicator": ("id", "com.example.app:id/loading"),
    "back_button": ("description", "Navigate up"),
    "menu_button": ("description", "Open navigation menu"),
    "search_icon": ("description", "Search"),
    "dialog_confirm": ("id", "com.example.app:id/dialog_confirm"),
    "dialog_cancel": ("id", "com.example.app:id/dialog_cancel"),
    "toast": ("class", "android.widget.Toast"),
    "settings": ("xpath", "//*[@text='Settings']"),
}

# Swipe gestures
SWIPE = {
    "swipe_left": {"direction": "left", "distance": 0.9},
    "swipe_right": {"direction": "right", "distance": 0.9},
    "swipe_up": {"direction": "up", "distance": 0.9},
    "swipe_down": {"direction": "down", "distance": 0.9},
}