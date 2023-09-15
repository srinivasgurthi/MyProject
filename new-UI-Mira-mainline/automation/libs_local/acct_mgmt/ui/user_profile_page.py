"""
This file holds library methods for User Profile
"""
import logging

from playwright.sync_api import Page

from hpe_glcp_automation_lib.libs.commons.ui.base_page import BasePage
from hpe_glcp_automation_lib.libs.acct_mgmt.ui.locators import UserProfileSelectors
from hpe_glcp_automation_lib.libs.acct_mgmt.ui.create_user_data import CreateUserData

log = logging.getLogger(__name__)


class UserProfile(BasePage):
    """
    Class that holds the methods to access user profile page
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize with page and cluster
        :param page: Page
        :param cluster: cluster under test url
        """
        log.info("Initialize User Profile page object")
        super().__init__(page, cluster)
        self.url = f"{cluster}/profile/UserProfile"

    def update_password(self, user_data: CreateUserData = CreateUserData):
        """
        Update user password
        param user: password edit for existing customer
        e.g. current_password, new_password, etc.
        """
        log.info('Changing the password')
        self.pw_utils.click_selector(
            UserProfileSelectors.PASSWORD_EDIT_BTN)
        self.page.fill(UserProfileSelectors.CURRENT_PASSWORD,
                       user_data.current_password)
        self.page.fill(UserProfileSelectors.NEW_PASSWORD,
                       user_data.change_password)
        self.page.fill(UserProfileSelectors.CONFIRM_NEW_PASSWORD,
                       user_data.confirm_password)
        self.pw_utils.save_screenshot(self.test_name)
        self.page.click(UserProfileSelectors.CHANGE_PASSWORD_BTN)
        self.wait_for_loaded_state()
        return self

    def update_personal_information(self, user_data: CreateUserData = CreateUserData):
        """
        Updates the personal information

       :param data: e.g. email, password, address, phone etc.
        """
        log.info("Updating the user personal information")
        self.pw_utils.click_selector(
            UserProfileSelectors.PERSONAL_EDIT_INFO_BTN)
        self.page.fill(UserProfileSelectors.FIRST_NAME,
                       user_data.first_name)
        self.page.fill(UserProfileSelectors.LAST_NAME, user_data.last_name)
        self.page.fill(UserProfileSelectors.ORGANISATION_NAME,
                       user_data.business_name)
        self.page.fill(UserProfileSelectors.STREET_ADDRESS,
                       user_data.street_address)
        self.page.fill(UserProfileSelectors.STREET_ADDRESS2,
                       user_data.street_address2)
        self.page.fill(UserProfileSelectors.INPUT_CITY,
                       user_data.city_name)
        self.page.fill(UserProfileSelectors.STATE_PROVINCE,
                       user_data.state_or_province)
        self.page.fill(UserProfileSelectors.POSTAL_CODE,
                       user_data.postal_code)
        self.pw_utils.select_drop_down_element(UserProfileSelectors.COUNTRY_BTN,
                                               user_data.country,
                                               UserProfileSelectors.COUNTRY_ELEMENT_ROLE)
        self.pw_utils.select_drop_down_element(UserProfileSelectors.SELECT_LANG, user_data.language,
                                               UserProfileSelectors.SELECT_LANG_ROLE)
        self.page.locator(
            UserProfileSelectors.PRIMARY_PHONE).fill(user_data.phone_number)
        self.page.locator(
            UserProfileSelectors.MOBILE_PHONE).fill(user_data.phone_number)
        self.pw_utils.save_screenshot(self.test_name)
        self.page.click(UserProfileSelectors.SAVE_INFO_BTN)
        self.wait_for_loaded_state()
        return self
