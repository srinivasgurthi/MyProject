"""
customer details page object model
"""
import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.acct_mgmt.ui.create_user_data import CreateUserData
from hpe_glcp_automation_lib.libs.acct_mgmt.ui.locators import CustomerDetailSelectors
from hpe_glcp_automation_lib.libs.commons.ui.headered_page import HeaderedPage

log = logging.getLogger(__name__)


class CustomerDetails(HeaderedPage):
    """
    Customer details page object model class
    """

    def __init__(self, page: Page, cluster: str, customer_id: str):
        """
        Initialize with page and cluster
        :param page: Page
        :param cluster: cluster under test url
        """
        log.info("Initialize CustomerAccount page object")
        super().__init__(page, cluster)
        self.url = f"{cluster}/customer-account/{customer_id}"

    def edit_customer_details(self, customer_data: CreateUserData = CreateUserData):
        """
        Edits customer account details

        :param customer_data: account data for new customer account creation,
            e.g. company_name, address, etc.
        :return: current instance of Customer details page object.
        """
        log.info(f"Editing customer details")
        self.page.locator(CustomerDetailSelectors.EDIT_DETAILS_BTN).click()
        self.page.locator(CustomerDetailSelectors.DESCRIPTION).fill(
            customer_data.description
        )
        self.page.locator(CustomerDetailSelectors.COUNTRY).click()
        self.page.locator(CustomerDetailSelectors.INPUT_COUNTRY_SEARCH).type(
            customer_data.country, delay=100
        )
        self.page.get_by_text(customer_data.country, exact=True).click()
        self.page.locator(CustomerDetailSelectors.STREET_ADDRESS_1).fill(
            customer_data.street_address
        )
        self.page.locator(CustomerDetailSelectors.STREET_ADDRESS_2).fill(
            customer_data.street_address2
        )
        self.page.locator(CustomerDetailSelectors.CITY).fill(
            customer_data.city_name)
        self.page.locator(CustomerDetailSelectors.STATE_OR_REGION).fill(
            customer_data.state_or_province
        )
        self.page.locator(CustomerDetailSelectors.ZIP).fill(
            customer_data.postal_code)
        self.page.locator(CustomerDetailSelectors.EMAIL_DETAILS).fill(
            customer_data.email
        )
        self.page.locator(CustomerDetailSelectors.PHONE_DETAILS).fill(
            customer_data.phone_number
        )
        self.pw_utils.save_screenshot(self.test_name)
        self.page.locator(CustomerDetailSelectors.SAVE_CHANGES_BTN).click()
        self.pw_utils.save_screenshot(self.test_name)
        self.page.wait_for_selector(CustomerDetailSelectors.UPDATE_MSG_POPUP)
        expect(self.page.locator(
            CustomerDetailSelectors.UPDATE_MSG)).to_be_visible()
        self.page.locator(CustomerDetailSelectors.UPDATE_MSG_CLOSE_BTN).click()
        return self
