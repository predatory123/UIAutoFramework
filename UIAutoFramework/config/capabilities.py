"""
Appium Desired Capabilities configurations
"""
from typing import Dict, Optional


class Capabilities:
    """Appium Desired Capabilities builder"""

    @staticmethod
    def android(
        platform_version: Optional[str] = None,
        device_name: Optional[str] = None,
        app_package: Optional[str] = None,
        app_activity: Optional[str] = None,
        app_path: Optional[str] = None,
        browser_name: str = "",
        auto_grant_permissions: bool = True,
        no_reset: bool = False,
        full_reset: bool = False,
        new_command_timeout: int = 300,
        automation_name: str = "UiAutomator2",
        **kwargs
    ) -> Dict:
        """Build Android capabilities"""
        caps = {
            "platformName": "Android",
            "browserName": browser_name,
            "autoGrantPermissions": auto_grant_permissions,
            "noReset": no_reset,
            "fullReset": full_reset,
            "newCommandTimeout": new_command_timeout,
            "automationName": automation_name,
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

        caps.update(kwargs)
        return caps

    @staticmethod
    def ios(
        platform_version: Optional[str] = None,
        device_name: Optional[str] = None,
        app_path: Optional[str] = None,
        browser_name: str = "",
        auto_grant_permissions: bool = True,
        no_reset: bool = False,
        full_reset: bool = False,
        new_command_timeout: int = 300,
        automation_name: str = "XCUITest",
        **kwargs
    ) -> Dict:
        """Build iOS capabilities"""
        caps = {
            "platformName": "iOS",
            "browserName": browser_name,
            "autoGrantPermissions": auto_grant_permissions,
            "noReset": no_reset,
            "fullReset": full_reset,
            "newCommandTimeout": new_command_timeout,
            "automationName": automation_name,
        }
        if platform_version:
            caps["platformVersion"] = platform_version
        if device_name:
            caps["deviceName"] = device_name
        if app_path:
            caps["app"] = app_path

        caps.update(kwargs)
        return caps

    @staticmethod
    def chrome_android(
        platform_version: Optional[str] = None,
        device_name: Optional[str] = None,
        chrome_package: str = "com.android.chrome",
        **kwargs
    ) -> Dict:
        """Build Chrome on Android capabilities"""
        caps = Capabilities.android(
            platform_version=platform_version,
            device_name=device_name,
            browser_name="Chrome",
            **kwargs
        )
        caps["chromePackage"] = chrome_package
        return caps


# Preset configurations for common apps
PRESETS = {
    "android_demo_app": Capabilities.android(
        platform_version="12",
        device_name="Android Emulator",
        app_package="com.example.app",
        app_activity=".MainActivity",
        app_path="apps/demo.apk"
    ),
    "android_chrome": Capabilities.chrome_android(
        platform_version="12",
        device_name="Android Emulator"
    ),
    "ios_demo_app": Capabilities.ios(
        platform_version="16",
        device_name="iPhone 14",
        app_path="apps/demo.ipa"
    ),
}