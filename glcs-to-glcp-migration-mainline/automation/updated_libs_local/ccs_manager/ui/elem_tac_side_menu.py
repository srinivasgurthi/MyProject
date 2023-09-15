"""
TAC Side Menu page element
"""
import logging

from playwright.sync_api import Page

from hpe_glcp_automation_lib.libs.ccs_manager.ui.locators import TacSideMenuSelectors
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import PwrightUtils

log = logging.getLogger(__name__)


class TacSideMenu:
    """
    TAC Side Menu page element class
    """

    def __init__(self, page: Page):
        """
        Initialize instance of TAC Side Menu page element
        :param page: page
        """
        self.pw_utils = PwrightUtils(page)
        self.page = page

    def navigate_to_notifications(self):
        """Click at 'Notifications' menu item at TAC side-menu.

        """
        log.info(f"Playwright: navigate to 'Notifications' page via TAC side-menu link.")
        self.pw_utils.click_selector(TacSideMenuSelectors.NOTIFICATIONS_LINK)

    def navigate_to_customers(self):
        """Click at 'Customers' menu item at TAC side-menu.

        """
        log.info(f"Playwright: navigate to 'Customers' page via TAC side-menu link.")
        self.pw_utils.click_selector(TacSideMenuSelectors.CUSTOMERS_LINK)

    def navigate_to_users(self):
        """Click at 'Users' menu item at TAC side-menu.

        """
        log.info(f"Playwright: navigate to 'Users' page via TAC side-menu link.")
        self.pw_utils.click_selector(TacSideMenuSelectors.USERS_LINK)

    def navigate_to_devices(self):
        """Click at 'Devices' menu item at TAC side-menu.

        """
        log.info(f"Playwright: navigate to 'Devices' page via TAC side-menu link.")
        self.pw_utils.click_selector(TacSideMenuSelectors.DEVICES_LINK)

    def navigate_to_orders(self):
        """Click at 'Orders' menu item at TAC side-menu.

        """
        log.info(f"Playwright: navigate to 'Orders' page via TAC side-menu link.")
        self.pw_utils.click_selector(TacSideMenuSelectors.ORDERS_LINK)

    def navigate_to_subscriptions(self):
        """Click at 'Subscriptions' menu item at TAC side-menu.

        """
        log.info(f"Playwright: navigate to 'Subscriptions' page via TAC side-menu link.")
        self.pw_utils.click_selector(TacSideMenuSelectors.SUBSCRIPTIONS_LINK)

    def navigate_to_firmware(self):
        """Click at 'Firmware' menu item at TAC side-menu.

        """
        log.info(f"Playwright: navigate to 'Firmware' page via TAC side-menu link.")
        self.pw_utils.click_selector(TacSideMenuSelectors.FIRMWARE_LINK)

    def navigate_to_applications(self):
        """Click at 'Applications' menu item at TAC side-menu.

        """
        log.info(f"Playwright: navigate to 'Applications' page via TAC side-menu link.")
        self.pw_utils.click_selector(TacSideMenuSelectors.APPLICATIONS_LINK)

    def navigate_to_whats_new(self):
        """Click at 'What's New' menu item at TAC side-menu.

        """
        log.info(f"Playwright: navigate to 'What's New' page via TAC side-menu link.")
        self.pw_utils.click_selector(TacSideMenuSelectors.WHATS_NEW_LINK)
