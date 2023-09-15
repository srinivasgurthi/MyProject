"""
Activate Documentation page object model.
"""
import logging
import time
from pathlib import Path

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.adi.ui.locators import ActivateDocumentationSelectors
from hpe_glcp_automation_lib.libs.commons.ui.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import TableUtils
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import PwrightUtils
from hpe_glcp_automation_lib.libs.adi.ui.side_menu_navigable_page import SideMenuNavigablePage

log = logging.getLogger(__name__)


class ActivateDocumentation(HeaderedPage, SideMenuNavigablePage):
    """
    Activate Documentation page object model class.
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize Activate Documentation page object.
        :param page: page.
        :param cluster: cluster url.
        """
        log.info("Initialize Activate Documentation page object")
        super().__init__(page, cluster)
        self.page = page
        self.table_utils = TableUtils(page)
        self.pw_utils = PwrightUtils(page)
        self.url = f"{cluster}/manage-account/activate/activate-documentation"

    def activate_documentation(self):
        """ Click & Validate on Activate Documentation Link
        :param: None
        :return: current instance of Activate Documentation page object.
        """
        log.info("Playwright: Activate - Activate Documentation")
        self.pw_utils.click_selector(ActivateDocumentationSelectors.ACTIVATE_DOC_LINK)
        return self

    def should_have_document_content(self, text):
        """Check text at activate documentation content section.
        :param: message: text to be validated.
        :return: current instance of Activate Devices page object.
        """
        log.info("Playwright: Verify text at activate documentation content section")
        self.page.wait_for_load_state("domcontentloaded")
        expect(self.page.locator(ActivateDocumentationSelectors.ACTIVATE_DOC_CONTENT)).to_have_text(text)
        return self
