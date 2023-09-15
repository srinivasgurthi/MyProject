"""
Headered page base class for page object model.
"""
import logging

from playwright.sync_api import Page

from hpe_glcp_automation_lib.libs.commons.ui.base_page import BasePage
from hpe_glcp_automation_lib.libs.commons.ui.elem_nav_bar import NavigationBar

log = logging.getLogger(__name__)


class HeaderedPage(BasePage):
    """
    HeaderedPage page object model.
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize HeaderedPage page object.
        :param page: page.
        :param cluster: cluster url.
        """
        super().__init__(page, cluster)
        self.nav_bar = NavigationBar(page)
