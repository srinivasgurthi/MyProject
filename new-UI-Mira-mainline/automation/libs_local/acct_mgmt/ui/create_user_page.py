"""
Create user page object
"""
import logging

from playwright.sync_api import Page

from hpe_glcp_automation_lib.libs.acct_mgmt.ui.create_user_data import CreateUserData
from hpe_glcp_automation_lib.libs.acct_mgmt.ui.locators import CreateUserSelectors
from hpe_glcp_automation_lib.libs.commons.ui.base_page import BasePage

log = logging.getLogger(__name__)


class CreateUserPage(BasePage):
    """
    Class holding methods for new user creation

    """

    def __init__(self, page: Page, cluster: str):
        log.info("Initialize Create User page object")
        super().__init__(page, cluster)

    def create_user(self, user: CreateUserData = CreateUserData):
        """
        Creates new user

        :param user: user data for new user creation, e.g. email, password, address, phone etc.
        """
        log.info(f"Register new user: '{user.email}'.")
        user_data = user
        self.page.locator(CreateUserSelectors.INPUT_EMAIL).fill(user_data.email)
        self.page.locator(CreateUserSelectors.INPUT_PASSWORD, ).fill(user_data.password)
        self.page.locator(CreateUserSelectors.FIRST_NAME).fill(user_data.first_name)
        self.page.locator(CreateUserSelectors.LAST_NAME).fill(user_data.last_name)
        self.page.locator(CreateUserSelectors.BUSINESS_NAME).fill(user_data.business_name)
        self.page.locator(CreateUserSelectors.STREET_ADDRESS).fill(user_data.street_address)
        self.page.locator(CreateUserSelectors.STREET_ADDRESS2).click()
        self.page.locator(CreateUserSelectors.INPUT_CITY).fill(user_data.city_name)
        self.page.locator(CreateUserSelectors.STATE_PROVINCE).fill(user_data.state_or_province)
        self.page.locator(CreateUserSelectors.POSTAL_CODE).fill(user_data.postal_code)
        self.pw_utils.select_drop_down_element(CreateUserSelectors.SELECT_COUNTRY, user_data.country)
        self.page.locator(CreateUserSelectors.SELECT_LANG).click()
        self.page.locator(CreateUserSelectors.SELECT_LANG_DROP.format(user_data.language)).click()
        self.pw_utils.select_drop_down_element(CreateUserSelectors.SELECT_TZ, user_data.time_zone)
        self.pw_utils.enter_text_into_element(CreateUserSelectors.INPUT_PHONE, user_data.phone_number)
        self.page.locator(CreateUserSelectors.EMAIL_CTCT_PREF).nth(3).click()
        self.page.locator(CreateUserSelectors.PHONE_CTCT_PREF).nth(3).click()
        self.page.locator(CreateUserSelectors.LEGAL_CHECK_BOX).click()
        self.pw_utils.save_screenshot(self.test_name)
        self.page.locator(CreateUserSelectors.CREATE_ACCT_TXT).click()
        self.page.wait_for_selector(CreateUserSelectors.VERIFICATION_EMAIL_SENT_TEXT)
        return user_data

    def open(self):
        """
        Navigate to cluster url
        """
        self.page.goto(self.cluster)
        self.page.wait_for_selector(CreateUserSelectors.SIGNUP_TXT).click()
        return self
