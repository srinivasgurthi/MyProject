"""
Identity page object model
"""
import logging

from playwright.sync_api import Page

from hpe_glcp_automation_lib.libs.authz.ui.roles_page import Roles
from hpe_glcp_automation_lib.libs.authz.ui.users_page import Users
from hpe_glcp_automation_lib.libs.commons.ui.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.commons.ui.locators import IdentitySelectors

log = logging.getLogger(__name__)


class Identity(HeaderedPage):
    """
    Identity page object model class
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize identity page object
        :param page: page
        :param cluster: cluster url
        """
        log.info("Initialize Identity page object")
        super().__init__(page, cluster)
        self.url = f"{cluster}/manage-account/identity"

    def open_users(self):
        """
        Navigate to Users page by clicking on tile on identity page
        """
        log.info(f"Playwright: navigate to Users page")
        self.pw_utils.wait_for_selector(IdentitySelectors.CARD_USERS)
        self.page.locator(IdentitySelectors.CARD_USERS).click()
        self.page.wait_for_load_state("domcontentloaded")
        self.pw_utils.save_screenshot(self.test_name)
        return Users(self.page, self.cluster)

    def open_roles_and_permissions(self):
        """
        Navigate to Roles & Permissions page by clicking on tile on identity page
        """
        log.info(f"Playwright: navigate to Roles & Permissions page")
        self.pw_utils.wait_for_selector(IdentitySelectors.CARD_ROLES)
        self.page.locator(IdentitySelectors.CARD_ROLES).click()
        self.page.wait_for_load_state("domcontentloaded")
        self.pw_utils.save_screenshot(self.test_name)
        return Roles(self.page, self.cluster)
