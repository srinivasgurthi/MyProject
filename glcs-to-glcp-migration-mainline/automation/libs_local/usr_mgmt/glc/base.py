# Copyright 2022 - Hewlett Packard Enterprise Company
""" CCS base page"""

import logging

from playwright.sync_api import Page, expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

LOG = logging.getLogger(__name__)


class GlcBasePage:
    """GLC base page"""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.glc_home_btn = self.page.get_by_role(
            "button", name="Cloud Services HPE GreenLake Central"
        )
        self.dashboard_menu = self.page.get_by_role("button", name="Dashboard")
        self.configure_btn = self.page.get_by_role("button", name="Configure")
        self.logout_menu = self.page.get_by_role("menuitem", name="Log Out")
        self.user_btn = self.page.get_by_role("button", name="User")

    def navigate_glc_home_page(self):
        self.page.wait_for_load_state()
        self.glc_home_btn.click()

    def select_tenant(self, tenant):
        self.page.get_by_text(tenant).click()
        self.page.wait_for_load_state()

    def current_tenant(self) -> str:
        try:
            self.page.get_by_role("button", name="User").click()
            return self.page.locator("saturn-text").filter(has_text="Tenant:").inner_text()
        except PlaywrightTimeoutError:
            return None

    def signout(self):
        self.user_btn.click()
        expect(self.logout_menu).to_be_visible()
        LOG.info("Signing out ...")
        self.logout_btn.click()
