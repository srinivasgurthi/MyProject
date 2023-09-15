"""
Navigation bar page element
"""
import logging

from playwright.sync_api import Page

from hpe_glcp_automation_lib.libs.commons.ui.locators import NavBarSelectors
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import PwrightUtils

log = logging.getLogger(__name__)


class NavigationBar:
    """
    Navigation bar page element class
    """

    def __init__(self, page: Page):
        """
        Initialize instance of page navigation
        :param page: page
        """
        self.pw_utils = PwrightUtils(page)
        self.page = page

    def navigate_to_dashboard(self):
        """
        Navigate to dashboard home page.
        """
        log.info("Navigate to dashboard home page.")
        self.pw_utils.click_selector(NavBarSelectors.DASHBOARD_NAV_MENU)

    def navigate_to_applications(self):
        """
        Navigate to application page.
        """
        log.info("Navigate to application page.")
        self.pw_utils.click_selector(NavBarSelectors.APPLICATION_NAV_MENU)

    def navigate_to_devices(self):
        """
        Navigate to devices page.
        """
        log.info("Navigate to devices page.")
        self.pw_utils.click_selector(NavBarSelectors.DEVICES_NAV_MENU)

    def navigate_to_manage(self):
        """
        Navigate to manage page.
        """
        log.info("Navigate to manage page.")
        self.pw_utils.click_selector(NavBarSelectors.MANAGE_NAV_MENU)

    def navigate_to_customers(self):
        """
        Navigate to customers page
        """
        self.pw_utils.click_selector(NavBarSelectors.CUSTOMERS_NAV_MENU)

    def _open_user_menu(self):
        """
        Open the usermenu page
        """
        self.pw_utils.click_selector(NavBarSelectors.MENU_ITEM_USER_BUTTON)
        self.page.wait_for_selector(NavBarSelectors.USER_MENU_POPUP)

    def logout(self):
        """
        Logout of the account via header's user menu.
        """
        log.info("Logout from current page.")
        self._open_user_menu()
        self.page.locator(NavBarSelectors.SIGNOUT_MENU).click()
        self.page.wait_for_load_state("domcontentloaded")

    def navigate_user_profile(self):
        """
        Navigates to user profile page
        """
        log.info("Navigating to User Profile page")
        self._open_user_menu()
        self.page.locator(NavBarSelectors.ACCOUNT_DETAILS_NAV_MENU).click()

    def navigate_preferences(self):
        """
        Navigates to user preferences page
        """
        log.info("Navigating to User Preferences page")
        self._open_user_menu()
        self.page.locator(NavBarSelectors.PREFERENCES_NAV_MENU).click()
