import logging

from playwright.sync_api import Page

from hpe_glcp_automation_lib.libs.acct_mgmt.ui.choose_account_page import ChooseAccount
from hpe_glcp_automation_lib.libs.authn.ui.locators import LoginPageSelectors
from hpe_glcp_automation_lib.libs.ccs_manager.ui.tac_home_page import TacHomePage
from hpe_glcp_automation_lib.libs.commons.ui.base_page import BasePage
from hpe_glcp_automation_lib.libs.commons.ui.home_page import HomePage

log = logging.getLogger(__name__)


class Login(BasePage):
    """
    Login Page object methods

    """

    def __init__(self, page: Page, cluster: str):
        log.info("Initialize Login page object")
        super().__init__(page, cluster)

    def login_acct(self, username, password, account_name=None):
        """ Method used for logging in based on credentials

        :param username: str - User's email
        :param password: str - User's password
        :param account_name: str - User's account name, if user has several accounts (optional)
        :return: Choose Account (if user has several accounts) or Home Page (if only one account available) object
        """
        log.info(f"Login by '{username}'.")
        self._login_account(username, password)
        if account_name:
            return ChooseAccount(self.page, self.cluster)
        else:
            return HomePage(self.page, self.cluster)

    def login_acct_tac(self, username, password, account_name=None):
        """Method used for logging in by TAC-user based on credentials.

        :param username: str - User's email.
        :param password: str - User's password.
        :param account_name: str - User's account name, if user has several accounts (optional).
        :return: ChooseAccount (if user has several accounts) or TacHomePage (if only one account available) object.
        """
        log.info(f"TAC: Login by '{username}'.")
        self._login_account(username, password)
        if account_name:
            return ChooseAccount(self.page, self.cluster)
        else:
            return TacHomePage(self.page, self.cluster)

    def open(self):
        """ Opens the Login page and verified it is opened

        :return: the instance of itself
        """
        self.page.goto(self.cluster)
        self.page.wait_for_selector(LoginPageSelectors.EMAIL_ID_PATH)
        return self

    def _login_account(self, username, password):
        """Log in by user with provided credentials.

        :param username: str - User's email.
        :param password: str - User's password.
        """
        self.page.fill(LoginPageSelectors.EMAIL_ID_PATH, username)
        self.page.locator(LoginPageSelectors.NEXT_BTN_PATH).click()
        self.page.fill(LoginPageSelectors.PASSWD_PATH, password)
        self.pw_utils.save_screenshot(self.test_name)
        self.page.locator(LoginPageSelectors.SUBMIT_PATH).click()
