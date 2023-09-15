"""
This file holds functions for Check Eligibility page
"""
import logging

from playwright.sync_api import Page

from hpe_glcp_automation_lib.libs.acct_mgmt.ui.create_user_data import \
    CheckEligibilityData
from hpe_glcp_automation_lib.libs.acct_mgmt.ui.locators import \
    CheckEligibilitySelectors
from hpe_glcp_automation_lib.libs.commons.ui.base_page import BasePage

log = logging.getLogger(__name__)


class CheckEligibility(BasePage):
    """
    Class for checking eligibility for Standard to MSP conversion
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize with page and cluster
        :param page: Page
        :param cluster: cluster under test url
        """
        log.info("Initialize Check Eligibility page object")
        super().__init__(page, cluster)
        self.url = f"{cluster}/manage-account/account-type-overview/check-eligibility"

    def perform(self, eligibility_check_data: CheckEligibilityData = CheckEligibilityData):
        """
        Performs eligibility check for the customer to be converted to MSP mode
        :return: None
        """
        log.info("Checking for eligibiligty of the account to be converted to MSP")

        # Provide Account Details
        self.page.locator(
            CheckEligibilitySelectors.NM_SERVICE_OPTION.format(
                eligibility_check_data.nmservice)
        ).click()

        self.pw_utils.select_drop_down_element(CheckEligibilitySelectors.DEVICE_DROP_DOWN,
                                               eligibility_check_data.device,
                                               CheckEligibilitySelectors.DEVICE_OPTION_ROLE,
                                               exact_match=True
                                               )

        self.pw_utils.select_drop_down_element(CheckEligibilitySelectors.SELECT_COUNTRY_DROP_DOWN,
                                               eligibility_check_data.country,
                                               CheckEligibilitySelectors.COUNTRY_OPTION_ROLE,
                                               exact_match=True
                                               )

        self.pw_utils.select_drop_down_element(
            CheckEligibilitySelectors.CUSTOMER_LOCATION_DROP_DOWN,
            eligibility_check_data.location,
            CheckEligibilitySelectors.CUSTOMER_LOCATION_OPTION_ROLE,
            exact_match=True
        )

        self.page.locator(CheckEligibilitySelectors.NETWORK_COUNT_INPUT).fill(
            eligibility_check_data.network_count
        )
        self.page.locator(CheckEligibilitySelectors.MAIL_ID).fill(
            eligibility_check_data.mail_id)
        self.page.locator(CheckEligibilitySelectors.SALES_REP_MAIL_ID).fill(
            eligibility_check_data.mail_id
        )
        self.pw_utils.save_screenshot(self.test_name)
        self.page.locator(CheckEligibilitySelectors.SUBMIT_BUTTON).click()
        self.page.locator(CheckEligibilitySelectors.CONTINUE_BUTTON).click()
