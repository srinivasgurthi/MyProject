"""
TAC Notifications page object model.
"""
import logging

from playwright.sync_api import Page

from hpe_glcp_automation_lib.libs.ccs_manager.ui.locators import TacNotificationsSelectors
from hpe_glcp_automation_lib.libs.commons.ui.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import TableUtils

log = logging.getLogger(__name__)


class TacNotificationsPage(HeaderedPage):
    """
    TAC Notifications page object model class.
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize TAC Notifications page object.
        :param page: page.
        :param cluster: cluster url.
        """
        log.info("Initialize TAC Notifications page object.")
        super().__init__(page, cluster)
        self.table_utils = TableUtils(page)
        self.url = f"{cluster}/manage-ccs/notifications"

    def click_menu_link(self, menu_item_text):
        """Click at menu item with specified text.

        :param menu_item_text: text of menu item to click.
        """
        log.info(f"Playwright: navigate to page by menu link with text '{menu_item_text}'.")
        self.page.locator(TacNotificationsSelectors.MENU_LINK_TEMPLATE.format(menu_item_text)).click()
