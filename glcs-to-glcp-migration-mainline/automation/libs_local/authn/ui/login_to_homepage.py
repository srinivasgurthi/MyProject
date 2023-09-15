import logging
import time
import re

from playwright.sync_api import Page, expect

from automation.updated_libs_local.authn.ui.base import GlcBasePage

LOG = logging.getLogger(__name__)



log = logging.getLogger(__name__)


class LoginPagePaths:
    email_id_path = "id=idp-discovery-username"
    next_btn_path = "id=idp-discovery-submit"
    passwd_path = "id=okta-signin-password"
    submit_path = "id=okta-signin-submit"
    cop_passwd_path = "type='password"
    cop_sign_on = "data-testid='signin"
    choose_acct = "data-testid=text-tile-title-account-"
    featured_applications = "data-testid=heading-featured_applications"
    account_search_box_xpath = 'data-testid=accounts-search-box'
    user_button = "button[aria-label='User']"
    unable_signin_xpath = "//p[text()='Unable to sign in']"
    powered_by_okta = "Powered by Okta"



class Login(object):
    def __init__(self, username, password):
        self.selectors = LoginPagePaths()
        self.username = username
        self.password = password
        log.info(f"Initialize {__name__}")

    def login_acct(self, page, account_name=None,):
        try:
            log.info(f"Logging into 1")
            page.wait_for_selector(self.selectors.email_id_path, timeout=0)
            log.info(f"Logging into 2")
            
            page.fill(self.selectors.email_id_path, self.username)
            page.locator(self.selectors.next_btn_path).click()
            page.wait_for_load_state()
            exits = False
            try:
                expect(page.get_by_text(self.selectors.powered_by_okta)).to_be_visible()
                log.info(f"With Okta Case")
                exits = True
            except Exception as e:
                log.info(f"Without Okta Case")
            if exits:
                page.locator(self.selectors.next_btn_path).click()
                page.wait_for_load_state()
            page.fill(self.selectors.passwd_path, self.password)
            page.locator(self.selectors.submit_path).first.click()
            if account_name:
                page.wait_for_selector(self.selectors.account_search_box_xpath)
                page.locator(self.selectors.account_search_box_xpath
                             ).fill(account_name, force=True)
                page.locator(f'text={account_name}').first.click()
                page.locator(f'text={self.selectors.featured_applications}')
            return True
        except Exception as e:
            log.error("not able to login_acct {}".format(e))
            return False

    def select_acct(self, page, account_name):
        try:
            page.wait_for_selector(self.selectors.account_search_box_xpath)
            page.locator(self.selectors.account_search_box_xpath
                         ).fill(account_name, force=True)
            page.locator(f'text={account_name}').first.click()
            time.sleep(1)
            page.locator(f'text={self.selectors.featured_applications}')
            return True
        except Exception as e:
            log.error("not able to login_acct {}".format(e))
            return False

    def go_to_home(self, page, login_url, account_name):
        try:
            page.goto(login_url, timeout=0)
            log.info(f"Logging into :: {login_url} with Acc {account_name}")
            do_login = self.login_acct(page, account_name)
            if not do_login:
                self.select_acct(page, account_name)
        except Exception as e:
            log.error(e)

    def wrong_password(self, page, login_url):
        page.goto(login_url, timeout=0)
        log.info(f"Opening :: {login_url}")
        page.wait_for_selector(self.selectors.email_id_path, timeout=0)
        page.fill(self.selectors.email_id_path, self.username)
        page.locator(self.selectors.next_btn_path).click()
        page.wait_for_load_state('networkidle')
        exits = False
        try:
            expect(page.get_by_text(self.selectors.powered_by_okta)).to_be_visible()
            log.info(f"With Okta Case")
            exits = True
        except Exception as e:
            log.info(f"Without Okta Case")
        if exits:
            page.locator(self.selectors.next_btn_path).click()
            page.wait_for_load_state()
        page.fill(self.selectors.passwd_path, self.password)
        page.locator(self.selectors.submit_path).first.click()
        page.wait_for_load_state()
        status = page.locator(self.selectors.unable_signin_xpath)
        expect(status).to_be_visible()

    def wrong_user(self, page, login_url):
        page.goto(login_url, timeout=0)
        log.info(f"Opening :: {login_url}")
        page.wait_for_selector(self.selectors.email_id_path, timeout=0)
        page.fill(self.selectors.email_id_path, self.username)
        page.locator(self.selectors.next_btn_path).click()
        page.fill(self.selectors.passwd_path, self.password)
        page.locator(self.selectors.submit_path).first.click()
        status = page.locator(self.selectors.unable_signin_xpath)
        expect(status).to_be_visible()
    

class GLCAuthnPage(GlcBasePage, LoginPagePaths):
    """GLC authn page"""

    def __init__(self, page: Page) -> None:
        GlcBasePage.__init__(self, page)
        self.glc_signin_banner = page.get_by_text(
        "Sign-in with your HPE account to access hpe-greenlake-central"
        )

    def login(
        self,
        username: str,
        password: str,
    ) -> None:
        LOG.info("Login with username %s", username)
        expect(self.glc_signin_banner).to_be_visible(timeout=0)
        self.page.wait_for_selector(LoginPagePaths.email_id_path, timeout=0)
        self.page.fill(LoginPagePaths.email_id_path,username)
        self.page.locator(LoginPagePaths.next_btn_path).wait_for()
        self.page.locator(LoginPagePaths.next_btn_path).click()
        self.page.wait_for_load_state('networkidle')
        signin_button_status = self.page.locator(LoginPagePaths.submit_path).is_visible()
        if signin_button_status:
            self.page.locator(LoginPagePaths.passwd_path).fill(password)
            self.page.locator(LoginPagePaths.submit_path).click()
            self.page.wait_for_load_state()
        else:
            self.page.locator(LoginPagePaths.next_btn_path).wait_for()
            self.page.locator(LoginPagePaths.next_btn_path).click()
            self.page.locator(LoginPagePaths.passwd_path).wait_for()
            self.page.locator(LoginPagePaths.passwd_path).fill(password)
            self.page.locator(LoginPagePaths.submit_path).click()
            self.page.wait_for_load_state()


