"""
TAC Notifications page object model.
"""
import logging

from playwright.sync_api import Page

from hpe_glcp_automation_lib.libs.ccs_manager.ui.tac_menu_navigable_page import TacMenuNavigablePage
from hpe_glcp_automation_lib.libs.commons.ui.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import TableUtils

log = logging.getLogger(__name__)


class TacNotificationsPage(HeaderedPage, TacMenuNavigablePage):
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
