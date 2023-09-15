"""
This file holds library methods for User Profile
"""
import logging


from playwright.sync_api import Page

from hpe_glcp_automation_lib.libs.commons.ui.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.acct_mgmt.ui.locators import UserPreferencesSelectors
from hpe_glcp_automation_lib.libs.acct_mgmt.ui.create_user_data import UserPreferencesData

log = logging.getLogger(__name__)


class UserPreferences(HeaderedPage):
    """
    Class that holds the methods to access User Preferences
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize with page and cluster
        :param page: Page
        :param cluster: cluster under test url
        """
        log.info("Initialize User Preferences object")
        super().__init__(page, cluster)
        self.url = f"{cluster}/preferences-only"

    def update_preferences(self, pref_data: UserPreferencesData = UserPreferencesData):
        """
        Updates the given user preferences

        :param UserPreferencesData
        :return: self
        """
        log.info('Updating the preferences')
        self.pw_utils.select_drop_down_element(
            UserPreferencesSelectors.LANGUAGE_DROPDOWN, pref_data.language,
            UserPreferencesSelectors.LANGUAGE_DROP_ROLE, exact_match=True)
        self.page.locator(
            UserPreferencesSelectors.SESSION_TIMEOUT).click()
        self.page.locator(
            UserPreferencesSelectors.SESSION_TIMEOUT).fill(pref_data.timeout)
        self.pw_utils.save_screenshot(self.test_name)
        self.page.locator(
            UserPreferencesSelectors.SAVE_CHANGES_BTN).click()
        return self
