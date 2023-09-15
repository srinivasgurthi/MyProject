import logging

from playwright.sync_api import Page

from hpe_glcp_automation_lib.libs.adi.ui.elem_activate_side_menu import ActivateSideMenu
from hpe_glcp_automation_lib.libs.adi.ui.locators import ActivateSideMenuSelectors
from hpe_glcp_automation_lib.libs.commons.ui.base_page import BasePage

log = logging.getLogger(__name__)


class SideMenuNavigablePage(BasePage):
    """
    Activate Side Menu Navigable page object model class.
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize Activate Side Menu Navigable page object.
        :param page: page.
        :param cluster: cluster url.
        """
        log.info("Initialize TAC Side Menu Navigable page object.")
        super().__init__(page, cluster)
        self.page = page
        self.side_menu = ActivateSideMenu(page, cluster)

    # TODO: Remove this method when related tests are refactored.
    def navigate_to_folders(self):
        """DEPRECATED! CONSIDER USING OF METHODS UNDER 'SideMenuNavigablePage().side_menu' ATTRIBUTE INSTEAD.
        Open Activate Folders page.
        :return: instance of Activate Folders page object.
        """
        log.info("Playwright: Navigate to Activate Folders page.")
        self.page.locator(ActivateSideMenuSelectors.FOLDERS_TAB_BUTTON).click()
