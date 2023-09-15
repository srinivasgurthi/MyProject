# Copyright 2023 - Hewlett Packard Enterprise Company
""" GLCP base page"""

import logging
from playwright.sync_api import Page, expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

LOG = logging.getLogger(__name__)


class GlcpBasePage:
    """GLC base page"""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.glcp_logo = self.page.get_by_test_id("glcp-header-all-brand")
        self.dashboard_menu = self.page.get_by_test_id("dashboard-nav-menu")
        self.application_menu = self.page.get_by_test_id("application-nav-menu")
        self.devices_menu = self.page.get_by_test_id("devices-nav-menu")
        self.manage_menu = self.page.get_by_test_id("manage-nav-menu")
        self.user_icon = self.page.get_by_test_id(
            "drop-btn-glcp-header-all-menu-item-user"
        )
        self.signout_menu = self.page.get_by_test_id("sign-out-hpe-nav-menu")
        self.account_search_box_xpath = "data-testid=accounts-search-box"
        self.switch_button = self.page.get_by_test_id("switch-account-btn")
        self.create_account_button = self.page.get_by_test_id("create-new-account-button")

    def navigate_glcp_home_page(self):
        self.page.wait_for_load_state()
        self.dashboard_menu.click()

    def signout(self):
        self.user_icon.click()
        expect(self.signout_menu).to_be_visible()
        LOG.info("Signing out ...")
        self.signout_menu.click()

    def current_account(self):
        try:
            self.page.get_by_test_id("switch-account-btn").is_visible()
            return self.page.get_by_test_id("heading-heading-home").inner_text()
        except PlaywrightTimeoutError:
            return None

    def select_acct(self, account_name: str) -> None:
        LOG.info(f"Select tenant {account_name}")
        self.page.wait_for_selector(self.account_search_box_xpath)
        self.page.locator(self.account_search_box_xpath).fill(
            account_name, force=True
        )
        self.page.locator(f"text={account_name}").first.click()

    def switch_account(self):
        self.switch_button.click()

    def create_account(self, company_name: str, country: str, address: str):
        self.create_account_button.click()
        self.page.wait_for_load_state()
        self.page.get_by_test_id("set-up-account-company-name-input").fill(company_name)
        self.page.get_by_test_id("set-up-account-street-address-input").fill(address)
        self.page.get_by_role("button", name="Select Country").click(delay=1000)
        self.page.wait_for_load_state()
        self.page.fill('[placeholder="Country"]', country[:len(country) - 1])
        self.page.get_by_role("option", name=f"{country}").first.click()
        # selector = '.StyledSelect__OptionsContainer-sc-znp66n-1 button:nth-child(247)'
        # united_states_button = self.page.query_selector(selector)
        # united_states_button.click()
        self.page.get_by_test_id("set-up-account-legal-terms-form-field").click()
        self.page.get_by_test_id("set-up-account-submit").click()
        self.page.wait_for_load_state()


# Copyright 2022 - Hewlett Packard Enterprise Company
""" CCS base page"""


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
