import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.authn.ui.base import GlcpBasePage

LOG = logging.getLogger(__name__)


class IdentityAccessPage(GlcpBasePage):
    def __init__(self, page: Page) -> None:
        GlcpBasePage.__init__(self, page)
        LOG.info(f"Initialize {__name__}")

    def navigate_to_manage_identity_and_access_page(self):
        LOG.info("Navigate to Identity and Access page")
        self.manage_menu.click()
        self.page.get_by_test_id("text-identity-title").get_by_text(
            "Identity & Access"
        ).click()
        expect(
            self.page.get_by_test_id("identity-access").get_by_text(
                "Manage", exact=True
            )
        ).to_be_visible()
