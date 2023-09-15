"""
#TODO:
TO be refactored with new framework.

"""
import logging
import time

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


class Login(object):
    def __init__(self, username, password):
        self.selectors = LoginPagePaths()
        self.username = username
        self.password = password
        log.info(f"Initialize {__name__}")

    def login_acct(self, page, account_name=None):
        try:
            page.fill(self.selectors.email_id_path, self.username)
            page.click(self.selectors.next_btn_path)
            page.fill(self.selectors.passwd_path, self.password)
            page.click(self.selectors.submit_path)
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
            page.goto(login_url)
            do_login = self.login_acct(page, account_name)
            if not do_login:
                self.select_acct(page, account_name)
        except Exception as e:
            log.error(e)
