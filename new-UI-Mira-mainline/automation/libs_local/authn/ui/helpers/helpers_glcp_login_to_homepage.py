"""
#TODO:
TO be refactored with new framework.

"""
import logging
import time
from hpe_glcp_automation_lib.libs.authn.ui.login_page_objs import LoginPagePaths

log = logging.getLogger(__name__)

class Login(object):
    def __init__(self, page, username=None, password=None):
        self.selectors = LoginPagePaths()
        self.page = page
        if username:
            self.username = username
        if password:
            self.password = password
        log.info(f"Initialize {__name__}")
        
    def selector_fill(self, selector_path, selector_value):
        self.page.locator(selector_path)
        self.page.fill(selector_path, selector_value)

    def selector_click(self, selector_path):
        self.page.locator(selector_path)
        self.page.click(selector_path)

    def selector_wait(self, selector_path):
        self.page.wait_for_selector(selector_path)

    def login_acct(self, account_name=None):
        try:
            self.login_user()
            if account_name:
                self.select_acct(account_name)
            self.selector_wait(self.selectors.featured_applications)
            return True
        except Exception as e:
            log.error("not able to login_acct {}".format(e))
            return False

    def login_user(self):
        self.selector_fill(self.selectors.email_id_path, self.username)
        self.selector_click(self.selectors.next_btn_path)
        self.selector_fill(self.selectors.passwd_path, self.password)
        self.selector_click(self.selectors.submit_path)

    def select_acct(self, account_name):
        try:
            self.selector_wait(self.selectors.account_search_box_xpath)
            self.selector_fill(self.selectors.account_search_box_xpath, account_name)
            self.selector_click(f'text={account_name}')
            self.selector_wait(self.selectors.featured_applications)
            return True
        except Exception as e:
            log.error("not able to login_acct {}".format(e))
            return False

    def go_to_page_after_login(self, url):
        try:
            return self.page.goto(url)
        except Exception as e:
            log.error(e)
            
    def logout_from_glcp(self):
        self.selector_click(self.selectors.menu_item_user_button)
        self.selector_click(self.selectors.sign_out_button)
