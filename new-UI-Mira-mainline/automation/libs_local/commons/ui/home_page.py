"""
Homepage page object model.
"""
import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.commons.ui.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.commons.ui.locators import HomePageSelectors
from hpe_glcp_automation_lib.libs.acct_mgmt.ui.switch_account_page import SwitchAccount

log = logging.getLogger(__name__)


class HomePage(HeaderedPage):
    """
    Homepage page object model class.
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize homepage page object.
        :param page: page.
        :param cluster: cluster url.
        """
        log.info("Initialize HomePage page object")
        super().__init__(page, cluster)
        self.url = f"{cluster}/home"

    def wait_for_loaded_state(self):
        """
        Wait till page is loaded and loading spinner is not present.
        :return: current instance of Homepage page object.
        """
        log.info("Playwright: wait for home page is loaded.")
        super().wait_for_loaded_state()
        self.page.locator(HomePageSelectors.LOADER_SPINNER).wait_for(
            state="hidden")
        return self

    def should_have_displayed_account(self, account_name):
        """
        Verify that home page successfully loaded for particular account.
        :return: current instance of Homepage page object.
        """
        log.info("Playwright: check account name displayed at home page.")
        self.pw_utils.save_screenshot(self.test_name)
        expect(self.page.locator(HomePageSelectors.ACCT_NAME)
               ).to_have_text(account_name)
        return self

    def open_switch_acct(self):
        """
        Verify that switch account loaded successfully loaded for particular account.
        :return: SwitchAccount Page
        """
        self.page.locator(HomePageSelectors.SWITCH_ACCOUNT_BUTTON).click()
        return SwitchAccount(self.page, self.cluster)

    def open_return_msp_account(self):
        """
        Navigates to MSP Account homepage
        return:current instance of homepage object
        """
        self.page.locator(HomePageSelectors.RETURN_TO_MSP_ACCT_BTN).click()
        return self
