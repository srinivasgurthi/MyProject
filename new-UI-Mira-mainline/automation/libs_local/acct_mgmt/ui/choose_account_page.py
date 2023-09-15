"""
Choose account page object model
"""
import logging

from playwright.sync_api import Page

from hpe_glcp_automation_lib.libs.acct_mgmt.ui.create_account_page import CreateAcctPage
from hpe_glcp_automation_lib.libs.acct_mgmt.ui.locators import ChooseAccountSelectors
from hpe_glcp_automation_lib.libs.ccs_manager.ui.tac_home_page import TacHomePage
from hpe_glcp_automation_lib.libs.commons.ui.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.commons.ui.home_page import HomePage

log = logging.getLogger(__name__)


class ChooseAccount(HeaderedPage):
    """
    Choose account page object model class
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize with page and cluster
        :param page: Page
        :param cluster: cluster under test url
        """
        log.info("Initialize ChooseAccount page object")
        super().__init__(page, cluster)
        self.url = f"{cluster}/onboarding/choose-account"

    def open(self):
        """
        Navigate to choose account by url
        :return: current instance of page object
        """
        log.info("Open Choose Account page by navigating to url.")
        self.page.goto(self.url)
        self.pw_utils.wait_for_selector(ChooseAccountSelectors.GO_TO_ACCOUNT,
                                        timeout_ignore=True,
                                        timeout=10000)
        if self.page.locator(ChooseAccountSelectors.GO_TO_ACCOUNT).count() < 2:
            self.pw_utils.wait_for_url(
                f"{self.cluster}/home", timeout_ignore=True, timeout=20000)
        current_url = self.page.url
        if not current_url == self.url:
            log.error("Unexpected URL")
            self.pw_utils.save_screenshot(self.test_name)
            raise Exception(
                f"Wrong page opened instead of expected 'choose-account': '{current_url}'")
        return self

    def go_to_account_by_index(self, num: int):
        """
        Select account by index.
        :param num: index (starting from 0) of account to choose.
        :return: instance of homepage object
        """
        log.info(f"Go to account with index '{num}'.")
        self.page.locator(
            ChooseAccountSelectors.GO_TO_ACCOUNT).nth(num).click()
        self.page.wait_for_load_state("domcontentloaded")
        return HomePage(self.page, self.cluster)

    def go_to_account_by_name(self, name: str):
        """
        Select account by name.
        :param name: name of account to choose.
        :return: instance of homepage object
        """
        log.info(f"Go to account with name '{name}'.")
        self._go_to_account_by_name(name)
        return HomePage(self.page, self.cluster)

    def go_to_account_by_name_tac(self, name: str):
        """Select account of TAC user by account name.

        :param name: name of account to choose.
        :return: instance of TAC homepage object.
        """
        log.info(f"TAC: Go to account with name '{name}'.")
        self._go_to_account_by_name(name)
        return TacHomePage(self.page, self.cluster)

    def open_create_account(self):
        """
        Navigate to create account page
        """
        self.page.locator(ChooseAccountSelectors.CREATE_ACCT_BTN).click()
        return CreateAcctPage(self.page, self.cluster)

    def _go_to_account_by_name(self, name: str):
        """Select account of user by account name.

        :param name: name of account to choose.
        """
        self.pw_utils.enter_text_into_element(ChooseAccountSelectors.SEARCH_BOX, name)
        try:
            self.page.wait_for_selector(ChooseAccountSelectors.COMPANY_NAME_TEMPLATE.format(name),
                                        state="visible", strict=True)
        except Exception as ex:
            log.error(f"Company name resolving error.")
            self.pw_utils.save_screenshot(self.test_name)
            raise Exception(f"Not resolved company name:\n{ex}")

        self.page.locator(
            ChooseAccountSelectors.GO_TO_ACCOUNT_TEMPLATE.format(name)).click()
        self.page.wait_for_load_state("domcontentloaded")
