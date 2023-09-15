"""
This file holds methods to create new user

"""
import logging
import os
import time

import allure
from allure_commons.types import AttachmentType

from hpe_glcp_automation_lib.libs.utils.random_gens import RandomGenUtils

log = logging.getLogger(__name__)
RECORD_DIR = os.path.join('tmp', 'results')


class CreateUserPaths:
    """
    Class holding user creation locators

    """
    choose_acct_url = "/onboarding/choose-account"
    signup_txt = "id=custom-signup"
    input_email = "input[name=\"email\"]"
    input_password = "input[name=\"password\"]"
    first_name = "input[name=\"firstName\"]"
    last_name = "input[name=\"lastName\"]"
    business_name = "input[name=\"businessName\"]"
    street_address = "input[name=\"streetAddress\"]"
    street_address2 = "input[name=\"streetAddress2\"]"
    input_city = "input[name=\"city\"]"
    state_province = "input[name=\"stateOrProvince\"]"
    postal_code = "input[name=\"postalCode\"]"
    create_acct_btn = "[data-testid=\"create-account-button\"]"
    setup_acct_comp_name = "[data-testid=\"set-up-account-company-name-input\"]"
    setup_acct_page = "/onboarding/set-up-account"
    select_country = "[placeholder=\"Select Country\"]"
    country = "text=American Samoa"
    select_lang = "input[name=\"selectLanguage\"]"
    select_tz = "input[name=\"selectTimezone\"]"
    select_tz1 = "text=(GMT+02:00) Cairo"
    input_phone = "input[name=\"phoneNumber\"]"
    email_ctct_pref = "#emailContactPreference div"
    phone_ctct_pref = "#phoneContactPreference div"
    legal_check_box = ".StyledCheckBox__StyledCheckBoxContainer-sc-1dbk5ju-1 >" \
                      " div > .StyledBox-sc-13pk1d4-0"
    create_acct_txt = "text=Create Account"
    acct_street_address = "[data-testid=\"set-up-account-street-address-input\"]"
    acct_city_input = "[data-testid=\"set-up-account-city-input\"]"
    acct_state_input = "[data-testid=\"set-up-account-state-input\"]"
    acct_legal_terms = "[data-testid=\"set-up-account-legal-terms-form-field\"] div"
    acct_submit = "[data-testid=\"set-up-account-submit\"]"
    manage_nav_menu = "[data-testid=\"manage-nav-menu\"]"


class CreateUser:
    """
    Class holding methods for new user creation

    """

    def __init__(self):
        log.info("Initialize create user function")
        self.selectors = CreateUserPaths()

    def create_user_fn(self, url, browser, random_mail_id):
        """
        Creates new user

        :param url: target url
        :param browser: browser instance
        :param random_mail_id: e-mail id of the new user
        """
        test_name = os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]
        random_str = RandomGenUtils.random_string_of_chars(7)
        context = browser.new_context(record_video_dir=RECORD_DIR)
        page = context.new_page()
        try:
            context.tracing.start(screenshots=True, snapshots=True, sources=True)
            page.goto(url)
            page.locator(self.selectors.signup_txt).click()
            # page.locator("Sign up").nth(1).click()
            page.screenshot(path=RECORD_DIR + random_str + "CreateAcct" + ".png", full_page=True)
            allure.attach.file(source=RECORD_DIR + random_str + "CreateAcct" + ".png")
            page.locator(self.selectors.input_email).click()
            page.screenshot(path=RECORD_DIR + random_str + "CreateAcct" + ".png", full_page=True)
            allure.attach.file(source=RECORD_DIR + random_str + "CreateAcct" + ".png")
            rand = RandomGenUtils.random_string_of_chars(7)
            page.locator(self.selectors.input_email).fill(random_mail_id)
            page.screenshot(path=RECORD_DIR + random_str + "CreateAcct" + ".png", full_page=True)
            allure.attach.file(source=RECORD_DIR + random_str + "CreateAcct" + ".png")
            page.locator(self.selectors.input_password).click()
            page.locator(self.selectors.input_password).fill("Aruba@123456789")
            # Click input[name="firstName"]
            page.locator(self.selectors.first_name).click()
            # Fill input[name="firstName"]
            page.locator(self.selectors.first_name).fill(rand + "first")
            time.sleep(1)
            # Click input[name="lastName"]
            page.locator(self.selectors.last_name).click()
            time.sleep(1)
            # Fill input[name="lastName"]
            page.locator(self.selectors.last_name).fill(rand)
            # Click input[name="businessName"]
            time.sleep(3)
            page.locator(self.selectors.business_name).click()
            time.sleep(1)
            # Fill input[name="businessName"]
            page.locator(self.selectors.business_name).fill(rand + " company")
            # Click input[name="streetAddress"]
            page.locator(self.selectors.street_address).click()
            time.sleep(1)
            # Fill input[name="streetAddress"]
            page.locator(self.selectors.street_address).fill("3333 my address")
            # Click input[name="streetAddress2"]
            page.locator(self.selectors.street_address2).click()
            time.sleep(1)
            # Click input[name="city"]
            page.locator(self.selectors.input_city).click()
            time.sleep(1)
            # Fill input[name="city"]
            page.locator(self.selectors.input_city).fill("Santa Clara")
            # Click input[name="stateOrProvince"]
            page.locator(self.selectors.state_province).click()
            # Fill input[name="stateOrProvince"]
            page.locator(self.selectors.state_province).fill("ca")
            # Click input[name="postalCode"]
            page.locator(self.selectors.postal_code).click()
            # Fill input[name="postalCode"]
            page.locator(self.selectors.postal_code).fill("94568")
            # Click input[name="streetAddress"]
            page.locator("input[name=\"streetAddress\"]").click()
            # Click input[name="selectCountry"]
            page.locator(self.selectors.select_country).click()
            # Click text=Albania
            page.locator("text=Albania").click()
            # Click input[name="selectLanguage"]
            page.locator(self.selectors.select_lang).click()
            # Click text=English
            page.locator("text=English").click()
            # Click input[name="selectTimezone"]
            page.locator(self.selectors.select_tz).click()
            # Click text=(GMT+02:00) Cairo
            page.locator(self.selectors.select_tz1).click()
            # Click input[name="phoneNumber"]
            page.locator(self.selectors.input_phone).click()
            # Fill input[name="phoneNumber"]
            page.locator(self.selectors.input_phone).fill("408-223-3232")
            # Click #emailContactPreference div >> nth=3
            page.locator(self.selectors.email_ctct_pref).nth(3).click()
            # Click #phoneContactPreference div >> nth=3
            page.locator(self.selectors.phone_ctct_pref).nth(3).click()
            # Click .StyledCheckBox__StyledCheckBoxContainer-sc-1dbk5ju-1 >
            # div > .StyledBox-sc-13pk1d4-0
            page.locator(self.selectors.legal_check_box).click()
            # Click text=Create Account
            page.screenshot(path=RECORD_DIR + random_str + "CreateAcct" + ".png", full_page=True)
            allure.attach.file(source=RECORD_DIR + random_str + "CreateAcct" + ".png")
            page.locator(self.selectors.create_acct_txt).click()
            time.sleep(3)
            page.screenshot(path=RECORD_DIR + random_str + "CreateAcct" + ".png", full_page=True)
            allure.attach.file(source=RECORD_DIR + random_str + "CreateAcct" + ".png")
            page.screenshot(path=RECORD_DIR + random_str + "CreateAcct" + ".png", full_page=True)
            allure.attach.file(source=RECORD_DIR + random_str + "CreateAcct" + ".png")
            # ---------------------
            return random_mail_id, rand
        except Exception as e:
            log.warning("not able to signup the user {}".format(e))
        finally:
            page.close()
            context.tracing.stop(path=RECORD_DIR + random_str + test_name + ".zip")
            allure.attach.file(source=RECORD_DIR + random_str + test_name + ".zip")
            context.close()
            path = page.video.path()
            allure.attach.file(source=path, name="video", attachment_type=AttachmentType.WEBM)
