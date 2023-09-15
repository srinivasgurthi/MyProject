"""
This file holds methods to create a new account

"""
import logging
import os
import time

import allure
from allure_commons.types import AttachmentType

from hpe_glcp_automation_lib.libs.utils.random_gens import RandomGenUtils

log = logging.getLogger(__name__)
RECORD_DIR = os.path.join('tmp', 'results')


class CreateAcctPaths:
    """
    Class for account creation locators

    """
    choose_acct_url = "/onboarding/choose-account"
    create_acct_btn = "[data-testid=\"create-account-button\"]"
    setup_acct_comp_name = "[data-testid=\"set-up-account-company-name-input\"]"
    setup_acct_page = "/onboarding/set-up-account"
    select_country = "[placeholder=\"Select Country\"]"
    country = "text=American Samoa"
    acct_street_address = "[data-testid=\"set-up-account-street-address-input\"]"
    acct_city_input = "[data-testid=\"set-up-account-city-input\"]"
    acct_state_input = "[data-testid=\"set-up-account-state-input\"]"
    acct_legal_terms = "[data-testid=\"set-up-account-legal-terms-form-field\"] div"
    acct_submit = "[data-testid=\"set-up-account-submit\"]"
    manage_nav_menu = "[data-testid=\"manage-nav-menu\"]"
    pcid_value = "[data-testid=\"paragraph-account-id-val\"]"


class CreateAcct:
    """
    Class holding methods to create account
    """

    def __init__(self):
        log.info("Initialize create user function")
        self.selectors = CreateAcctPaths()

    def create_acct_fn(self, url, browser, verify_url, end_username, country="American Samoa"):
        """
        Creates account

        :param url: target url
        :param browser: browser instance
        :param verify_url: verification link
        :param end_username: end user name for the user
        :param country: country value
        """
        test_name = os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]
        random_str = RandomGenUtils.random_string_of_chars(7)
        context = browser.new_context(record_video_dir=RECORD_DIR)
        page = context.new_page()
        try:
            context.tracing.start(screenshots=True, snapshots=True, sources=True)
            page.goto(verify_url)
            time.sleep(5)
            page.goto(url + self.selectors.choose_acct_url)
            page.screenshot(path=RECORD_DIR + random_str + "CreateAcct" + ".png", full_page=True)
            allure.attach.file(source=RECORD_DIR + random_str + "CreateAcct" + ".png")
            time.sleep(15)
            page.locator(self.selectors.create_acct_btn).click()
            page.locator(self.selectors.setup_acct_comp_name).click()
            page.wait_for_url(url + self.selectors.setup_acct_page)
            page.locator(self.selectors.setup_acct_comp_name).click()
            page.locator(self.selectors.setup_acct_comp_name).fill(end_username + " Company")
            page.locator(self.selectors.select_country).click()
            page.locator("text=" + country).click()
            page.locator(self.selectors.acct_street_address).click()
            page.locator(self.selectors.acct_street_address).fill("3333 scott blvd")
            page.locator(self.selectors.acct_city_input).click()
            page.locator(self.selectors.acct_city_input).fill("Santa Clara")
            page.locator(self.selectors.acct_state_input).click()
            page.locator(self.selectors.acct_state_input).fill("ca")
            page.locator(self.selectors.acct_state_input).click()
            page.locator(self.selectors.acct_state_input).fill("94583")
            page.locator(self.selectors.acct_legal_terms).nth(2).click()
            page.screenshot(path=RECORD_DIR + random_str + "CreateAcct" + ".png", full_page=True)
            allure.attach.file(source=RECORD_DIR + random_str + "CreateAcct" + ".png")
            # Click [data-testid="set-up-account-submit"]
            page.locator(self.selectors.acct_submit).click()
            page.screenshot(path=RECORD_DIR + random_str + "CreateAcct" + ".png", full_page=True)
            allure.attach.file(source=RECORD_DIR + random_str + "CreateAcct" + ".png")
            page.wait_for_url(url + "/home")
            page.screenshot(path=RECORD_DIR + random_str + "CreateAcct" + ".png", full_page=True)
            allure.attach.file(source=RECORD_DIR + random_str + "CreateAcct" + ".png")
            page.locator(self.selectors.manage_nav_menu).click()
            page.wait_for_url(url + "/manage-account")
            page.screenshot(path=RECORD_DIR + random_str + "CreateAcct" + ".png", full_page=True)
            allure.attach.file(source=RECORD_DIR + random_str + "CreateAcct" + ".png")
            pcid = page.locator(self.selectors.pcid_value).text_content()
            return pcid
        except Exception as e:
            log.warning("not able to signup the account {}".format(e))
        finally:
            page.close()
            context.tracing.stop(path=RECORD_DIR + random_str + test_name + ".zip")
            allure.attach.file(source=RECORD_DIR + random_str + test_name + ".zip")
            context.close()
            path = page.video.path()
            allure.attach.file(source=path, name="video", attachment_type=AttachmentType.WEBM)
