"""
customer account page object model
"""
import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.commons.ui.elem_nav_bar import NavigationBar
from hpe_glcp_automation_lib.libs.commons.ui.manage_account_page import ManageAccount
from hpe_glcp_automation_lib.libs.acct_mgmt.ui.create_user_data import CreateUserData
from hpe_glcp_automation_lib.libs.acct_mgmt.ui.customer_details_page import (
    CustomerDetails,
)
from hpe_glcp_automation_lib.libs.acct_mgmt.ui.locators import (
    AddCustomerSelectors,
    CustomerAccountSelectors,
    DeleteCustomerSelectors,
)
from hpe_glcp_automation_lib.libs.commons.ui.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.commons.ui.home_page import HomePage

log = logging.getLogger(__name__)


class CustomerAccount(HeaderedPage):
    """
    Customer account page object model class
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize with page and cluster
        :param page: Page
        :param cluster: cluster under test url
        """
        log.info("Initialize CustomerAccount page object")
        super().__init__(page, cluster)
        self.url = f"{cluster}/customer-account"

    def add_customer(self, account_data: CreateUserData = CreateUserData):
        """
        Creates new customer account

        :param account_data: account data for new customer account creation,
        e.g. company_name, address, etc.
        """

        log.info(f"Creating customer account '{account_data.business_name}'")
        self.page.locator(CustomerAccountSelectors.ADD_CUSTOMER_BTN).click()

        self.page.locator(AddCustomerSelectors.COMPANY_NAME).fill(
            account_data.business_name
        )
        self.page.locator(AddCustomerSelectors.COMPANY_DESCRIPTION).fill(
            account_data.description
        )
        # self.pw_utils.select_drop_down_element(AddCustomerSelectors.COUNTRY_INPUT,
        #                                        account_data.country,
        #                                        AddCustomerSelectors.COUNTRY_ITEM_ROLE,
        #                                        exact_match=True
        #                                        )
        self.page.locator(AddCustomerSelectors.COUNTRY_INPUT).click()
        self.pw_utils.enter_text_into_element(
            AddCustomerSelectors.SEARCH_COUNTRY, account_data.country
        )
        self.pw_utils.click_selector(
            AddCustomerSelectors.COUNTRY_OPTION.format(account_data.country)
        )
        self.page.locator(AddCustomerSelectors.STREET_ADDRESS).fill(
            account_data.street_address
        )
        self.page.locator(AddCustomerSelectors.STREET_ADDRESS2).fill(
            account_data.street_address2
        )
        self.page.locator(AddCustomerSelectors.CITY_INPUT).fill(account_data.city_name)
        self.page.locator(AddCustomerSelectors.REGION_INPUT).fill(
            account_data.state_or_province
        )
        self.page.locator(AddCustomerSelectors.POSTAL_CODE).fill(
            account_data.postal_code)
        self.pw_utils.save_screenshot(self.test_name)
        self.page.locator(AddCustomerSelectors.CREATE_BTN).click()
        self.pw_utils.save_screenshot(self.test_name)
        self.page.wait_for_selector(AddCustomerSelectors.CREATION_MSG_POPUP)
        expect(self.page.locator(AddCustomerSelectors.CREATION_MSG)).to_be_visible()
        self.page.locator(AddCustomerSelectors.CREATION_MSG_CLOSE_BTN).click()
        return self

    def should_customer_exists(self, customer_name: str):
        """
        Check for the given customer existence

        return: bool
        """
        self.search_customer(customer_name)
        expect(
            self.page.locator(CustomerAccountSelectors.CUSTOMER.format(customer_name))
        ).to_be_enabled()
        return self

    def wait_for_loaded_table(self):
        """
        Wait for table rows are not empty and loader spinner is not present on the page
        :return: current instance of customers page object
        """
        self.page.wait_for_selector(
            CustomerAccountSelectors.CUSTOMER_TABLE_ROWS, state="visible", strict=False
        )
        self.page.locator(CustomerAccountSelectors.LOADER_SPINNER).wait_for(
            state="hidden"
        )
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def search_customer(self, customer_name: str):
        """
        Searches the specified customer

        :param customer_name: name of the customer/tenant
        :return: self
        """
        log.info(f"Playwright: search for text: '{customer_name}' in customer records")
        self.pw_utils.enter_text_into_element(
            CustomerAccountSelectors.SEARCH_CUSTOMER, customer_name
        )
        self.wait_for_loaded_table()
        return self

    def load_customer(self, customer_name: str):
        """
        Loads the specified customer

        :param customer_name: name of the customer
        :return: Dashboard page of the loaded customer
        """
        log.info(f"Loading customer account '{customer_name}'")
        try:
            self.search_customer(customer_name)
            self.page.locator(
                CustomerAccountSelectors.CUSTOMER.format(customer_name)
            ).click()
        except Exception as ex:
            log.error("Unable to load the customer {}".format(customer_name))
            raise Exception(f"Unable to load the customer:\n{ex}")
        else:
            return HomePage(self.page, self.cluster)

    def delete_customer(self, customer_name: str):
        """
        Deletes the specified customer

        :param customer_name: name of the customer to be deleted
        """
        try:
            log.info(f"Deleting customer account '{customer_name}'")
            self.search_customer(customer_name)
            self.page.locator(
                CustomerAccountSelectors.CUSTOMER_ACTIONS.format(customer_name)
            ).click()
            self.page.locator(CustomerAccountSelectors.DELETE_CUSTOMER_BTN).click()
            self.page.wait_for_selector(DeleteCustomerSelectors.TERMS_CHECKBOX).click()
            self.page.locator(DeleteCustomerSelectors.DELETE_ACCOUNT_BTN).click()
        except Exception as ex:
            log.error("Unable to delete the customer {}".format(customer_name))
            raise Exception(f"Unable to delete the customer:\n{ex}")
        else:
            return self

    def open_customer_details(self, customer_name: str):
        """
        Load the details for the specified customer

        :param customer_name: name of the customer whose details to be opened.
        :return: instance of Customer details page object.
        """
        home = self.load_customer(customer_name).wait_for_loaded_state()
        home.nav_bar.navigate_to_manage()
        manage_account_page = ManageAccount(self.page, self.cluster)
        pcid = manage_account_page.get_pcid()
        manage_account_page.nav_bar.navigate_to_dashboard()
        home \
            .wait_for_loaded_state() \
            .open_return_msp_account() \
            .wait_for_loaded_state() \
            .nav_bar.navigate_to_customers()
        self.wait_for_loaded_state()
        self.search_customer(customer_name)
        self.page.locator(
            CustomerAccountSelectors.CUSTOMER_ACTIONS.format(customer_name)
        ).click()
        self.page.locator(CustomerAccountSelectors.VIEW_DETAILS_BTN).click()
        return CustomerDetails(self.page, self.cluster, pcid)
