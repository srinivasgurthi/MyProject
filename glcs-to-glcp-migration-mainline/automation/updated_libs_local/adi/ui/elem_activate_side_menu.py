"""
Side Menu page element
"""
import logging

from playwright.sync_api import Page

from hpe_glcp_automation_lib.libs.adi.ui.locators import ActivateSideMenuSelectors
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import PwrightUtils
from hpe_glcp_automation_lib.libs.commons.ui.headered_page import HeaderedPage

log = logging.getLogger(__name__)


class ActivateSideMenu(HeaderedPage):
    """
    Activate Side Menu page element class
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize instance of Activate Side Menu page element
        :param page: page
        """
        log.info("Initialize Activate Side Menu page object")
        super().__init__(page, cluster)
        self.page = page
        self.pw_utils = PwrightUtils(page)

    def navigate_to_devices(self):
        """Click at 'Devices' menu item at activate side-menu.
        """
        log.info(f"Playwright: navigate to 'Devices' page via activate side-menu link.")
        self.pw_utils.click_selector(ActivateSideMenuSelectors.DEVICES_TAB_BUTTON)

    def navigate_to_folders(self):
        """Click at 'Folders' menu item at activate side-menu.
        """
        log.info(f"Playwright: navigate to 'Folders' page via activate side-menu link.")
        self.pw_utils.click_selector(ActivateSideMenuSelectors.FOLDERS_TAB_BUTTON)

    def navigate_to_activate_documentation(self):
        """Click at 'Activate Documentation' menu item at activate side-menu.
        """
        log.info(f"Playwright: navigate to 'Activate Documentation' page via activate side-menu link.")
        self.pw_utils.click_selector(ActivateSideMenuSelectors.DOCUMENTATION_TAB_BUTTON)
