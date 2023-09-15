"""
This file holds methods to switch account

"""
import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.commons.ui.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.acct_mgmt.ui.locators import SwitchAccountSelectors


log = logging.getLogger(__name__)


class SwitchAccount(HeaderedPage):
    """
    SwitchAccount page object
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize with page and cluster
        :param page: Page
        :param cluster: cluster under test url
        """
        log.info("Initialize Switch Account page object")
        super().__init__(page, cluster)
        self.url = f"{cluster}/switch-account"

    def should_have_account_in_recent(self, account_name):
        """
        Check the account name listed in the recent first

        :param account_name: account_name
        :return: current instance
        """
        log.info(f"Playwright: check that account_name listed in the recent"
                 f"with '{account_name}'")
        self.pw_utils.save_screenshot(self.test_name)
        expect(self.page.locator(SwitchAccountSelectors.RECENT_ACCOUNT_NAME)
               ).to_have_text(account_name)
        return self

    def search_account(self, account: str):
        """
        Searches the specified account

        :param account: name of the account
        :return: self
        """
        log.info(
            f"Playwright: search for text: '{account}' in customer reecords")
        self.pw_utils.enter_text_into_element(
            SwitchAccountSelectors.SEARCH_ACCOUNT_FIELD, account)
        self.wait_for_loaded_state()
        return self

    def filterby(self, _type: str = 'All'):
        """
        Filter the account list for the given type

        :param by_type: "Standard", "MSP", "All"
        :return: self
        """
        log.info(
            f"Playwright: filter by account type: '{_type}' in customer reecords")
        log.info(self.page.locator(SwitchAccountSelectors.ACCOUNT_TYPE_DROPDOWN).input_value())
        if _type != self.page.locator(SwitchAccountSelectors.ACCOUNT_TYPE_DROPDOWN).input_value():
            self.page.locator(SwitchAccountSelectors.ACCOUNT_TYPE_DROPDOWN).click()
            self.page.locator(SwitchAccountSelectors.DROPDOWN_OPTS_TEMPLATE.format(_type)).click()
            self.wait_for_loaded_state()
        return self

    def sortby(self, _type: str = 'Recent'):
        """
        Sort the account list for the given type

        :param by_type: "Recent", "Alphabetical"
        :return: self
        """
        log.info(
            f"Playwright: sort by account type: '{_type}' in customer reecords")
        if _type != self.page.locator(SwitchAccountSelectors.SORT_BY_DROPDOWN).input_value():
            self.page.locator(SwitchAccountSelectors.SORT_BY_DROPDOWN).click()
            self.page.locator(SwitchAccountSelectors.DROPDOWN_OPTS_TEMPLATE.format(_type)).click()
            self.wait_for_loaded_state()
        return self
