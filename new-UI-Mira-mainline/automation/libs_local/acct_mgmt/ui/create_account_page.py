"""
This file holds methods to create a new account

"""
import logging

from playwright.sync_api import Page

from hpe_glcp_automation_lib.libs.acct_mgmt.ui.create_user_data import CreateUserData
from hpe_glcp_automation_lib.libs.acct_mgmt.ui.locators import CreateAcctSelectors
from hpe_glcp_automation_lib.libs.commons.ui.base_page import BasePage
from hpe_glcp_automation_lib.libs.commons.ui.home_page import HomePage

log = logging.getLogger(__name__)


class CreateAcctPage(BasePage):
    """
    Account creation page object
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize with page and cluster
        :param page: Page
        :param cluster: cluster under test url
        """
        log.info("Initialize Create Account page object")
        super().__init__(page, cluster)
        self.url = f"{cluster}/onboarding/set-up-account"

    def create_acct(self, account: CreateUserData = CreateUserData):
        """
        Creates new account

        :param account: account data for new account creation, e.g. email, password, address, phone etc.
        """
        log.info(f"Create new workspace for {account.email}.")
        
        account_data = account
        self.page.locator(CreateAcctSelectors.SETUP_ACCT_COMP_NAME).fill(
            account_data.business_name)
        self.page.locator(CreateAcctSelectors.SELECT_COUNTRY).click()
        self.page.locator(CreateAcctSelectors.INPUT_COUNTRY_SEARCH).type(
            account_data.country, delay=100)
        self.page.get_by_text(account_data.country, exact=True).click()
        self.page.locator(CreateAcctSelectors.ACCT_STREET_ADDRESS).fill(
            account_data.street_address)
        self.page.locator(CreateAcctSelectors.ACCT_CITY_INPUT).fill(
            account_data.city_name)
        self.page.locator(CreateAcctSelectors.ACCT_STATE_INPUT).fill(
            account_data.state_or_province)
        self.page.locator(CreateAcctSelectors.POSTAL_CODE).fill(
            account_data.postal_code)
        self.page.locator(CreateAcctSelectors.INPUT_PHONE).fill(
            account_data.phone_number)
        self.page.locator(CreateAcctSelectors.INPUT_EMAIL).fill(
            account_data.email)
        self.page.locator(CreateAcctSelectors.ACCT_LEGAL_TERMS).nth(2).click()
        self.pw_utils.save_screenshot(self.test_name)
        self.page.locator(CreateAcctSelectors.ACCT_SUBMIT).click()
        self.pw_utils.save_screenshot(self.test_name)
        return HomePage(self.page, self.cluster)

    def open(self):
        """Navigate to create workspace page (for logged-in user) by URL.

        :return: current instance of page object.
        """
        self.page.goto(self.url)
        self.page.locator(CreateAcctSelectors.CREATE_ACCT_BTN).click()
        self.page.wait_for_selector(CreateAcctSelectors.SETUP_ACCT_COMP_NAME)
        return self
