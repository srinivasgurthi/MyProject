"""
TAC Dashboard page object model.
"""
import logging

from playwright.sync_api import Page

from hpe_glcp_automation_lib.libs.acct_mgmt.ui.switch_account_page import SwitchAccount
from hpe_glcp_automation_lib.libs.ccs_manager.ui.locators import TacHomePageSelectors
from hpe_glcp_automation_lib.libs.ccs_manager.ui.tac_notifications_page import TacNotificationsPage
from hpe_glcp_automation_lib.libs.commons.ui.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import TableUtils

log = logging.getLogger(__name__)


class TacHomePage(HeaderedPage):
    """
    TAC Dashboard page object model class.
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize TAC Dashboard page object.
        :param page: page.
        :param cluster: cluster url.
        """
        log.info("Initialize TAC Dashboard page object.")
        super().__init__(page, cluster)
        self.table_utils = TableUtils(page)
        self.url = f"{cluster}/manage-ccs/home"

    def open_workspace_details(self):
        """Click at Workspace Details card.

        :return: instance of TAC account-details page object.
        """
        log.info(f"Playwright: Click at Workspace Details card.")
        self.page.locator(TacHomePageSelectors.CARD_WORKSPACE_DETAILS).click()
        # TODO: add returning of TAC account-details page object class when it's implemented.

    def open_manage_ccs(self):
        """Click at Manage CCS card.

        :return: instance of TAC notifications page object.
        """
        log.info(f"Playwright: Click at Manage CCS card.")
        self.page.locator(TacHomePageSelectors.CARD_MANAGE_CCS).click()
        return TacNotificationsPage(self.page, self.cluster)

    def click_switch_workspace(self):
        """Click at Switch Workspace button.

        :return: instance of switch-account page object.
        """
        log.info(f"Playwright: Click at Manage CCS card.")
        self.page.locator(TacHomePageSelectors.SWITCH_ACCOUNT_BTN).click()
        return SwitchAccount(self.page, self.cluster)
