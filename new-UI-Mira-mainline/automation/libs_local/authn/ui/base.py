# Copyright 2023 - Hewlett Packard Enterprise Company
""" GLCP base page"""

import logging
from playwright.sync_api import Page, expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

LOG = logging.getLogger(__name__)



class GlcpBaseSelectors:
    glcp_header = "glcp-header-all-brand"
    dashboard_menu = "dashboard-nav-menu"
    application_nav_menu = "application-nav-menu"
    devices_nav_menu = "devices-nav-menu"
    manage_nav_menu = "manage-nav-menu"
    sign_out_hpe_nav_menu = "sign-out-hpe-nav-menu"
    accounts_search_box = "data-testid=accounts-search-box"
    user_icon_drop_down = "drop-btn-glcp-header-all-menu-item-user"
    switch_acc_button = "switch-account-btn"
    create_new_button = "create-new-account-button"
    home_heading_memu = "heading-heading-home"
    account_company_name_textbox = "set-up-account-company-name-input"
    account_street_addr_textbox = "set-up-account-street-address-input"
    account_legalterms_textbox = "set-up-account-legal-terms-form-field"
    account_setup_submit_btn = "set-up-account-submit"




class GlcpBasePage:
    """GLC base page"""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.base_selectors = GlcpBaseSelectors()
        self.glcp_logo = self.page.get_by_test_id(self.base_selectors.glcp_header)
        self.dashboard_menu = self.page.get_by_test_id(self.base_selectors.dashboard_menu)
        self.application_menu = self.page.get_by_test_id(self.base_selectors.application_nav_menu)
        self.devices_menu = self.page.get_by_test_id(self.base_selectors.devices_nav_menu)
        self.manage_menu = self.page.get_by_test_id(self.base_selectors.manage_nav_menu)
        self.user_icon = self.page.get_by_test_id(self.base_selectors.user_icon_drop_down)
        self.signout_menu = self.page.get_by_test_id(self.base_selectors.sign_out_hpe_nav_menu)
        self.account_search_box_xpath = self.base_selectors.accounts_search_box
        self.switch_button = self.page.get_by_test_id(self.base_selectors.switch_acc_button)
        self.create_account_button = self.page.get_by_test_id(self.base_selectors.create_new_button)

    def navigate_glcp_home_page(self):
        """ Navigate to home page """
        self.page.wait_for_load_state()
        self.dashboard_menu.click()

    def signout(self):
        """ Sign out from Glcp """
        self.user_icon.click()
        expect(self.signout_menu).to_be_visible()
        LOG.info("Signing out ...")
        self.signout_menu.click()

    def current_account(self):
        """ Fetch Current Account name """
        try:
            self.page.get_by_test_id(self.base_selectors.switch_acc_button).is_visible()
            return self.page.get_by_test_id(self.base_selectors.home_heading_memu).inner_text()
        except PlaywrightTimeoutError:
            return None

    def select_acct(self, account_name: str) -> None:
        """ Fetch Current Account name """
        LOG.info(f"Select tenant {account_name}")
        self.page.wait_for_selector(self.account_search_box_xpath)
        self.page.locator(self.account_search_box_xpath).fill(
            account_name, force=True
        )
        self.page.locator(f"text={account_name}").first.click()

    def switch_account(self):
        """ Switch Account in GLCP """
        self.switch_button.click()

    def create_account(self, company_name: str, country: str, address: str):
        """ Create account in in GLCP for {company_name}, {country}, {address} """
        self.create_account_button.click()
        self.page.wait_for_load_state()
        self.page.get_by_test_id(self.base_selectors.account_company_name_textbox).fill(company_name)
        self.page.get_by_test_id(self.base_selectors.account_street_addr_textbox).fill(address)
        self.page.get_by_role("button", name="Select Country").click(delay=1000)
        self.page.wait_for_load_state()
        self.page.fill('[placeholder="Country"]', country[:len(country) - 1])
        self.page.get_by_role("option", name=f"{country}").first.click()
        # selector = '.StyledSelect__OptionsContainer-sc-znp66n-1 button:nth-child(247)'
        # united_states_button = self.page.query_selector(selector)
        # united_states_button.click()
        self.page.get_by_test_id(self.base_selectors.account_legalterms_textbox).click()
        self.page.get_by_test_id(self.base_selectors.account_setup_submit_btn).click()
        self.page.wait_for_load_state()


# Copyright 2022 - Hewlett Packard Enterprise Company
""" CCS base page"""


class GlcBasePage:
    """
    GLC base page
    
    
    
    """

    def __init__(self, page: Page) -> None:
        """
        :param Page: take page object
        
        :return: instance of itself
        """
        self.page = page
        self.glc_home_btn = self.page.get_by_role(
            "button", name="Cloud Services HPE GreenLake Central"
        )
        self.dashboard_menu = self.page.get_by_role("button", name="Dashboard")
        self.configure_btn = self.page.get_by_role("button", name="Configure")
        self.logout_menu = self.page.get_by_role("menuitem", name="Log Out")
        self.user_btn = self.page.get_by_role("button", name="User")

    def navigate_glc_home_page(self):
        """ Navigate to Home page of GLC  
        
        """
        self.page.wait_for_load_state()
        self.glc_home_btn.click()

    def select_tenant(self, tenant):
        """ Select Tenant of GLC 
        
        :param: tenant: (required)
        
        :return: None
        
        """
        self.page.get_by_text(tenant).click()
        self.page.wait_for_load_state()


    def current_tenant(self) -> str:
        """ Get Current Tenant of GLC 

        """
        try:
            self.page.get_by_role("button", name="User").click()
            return self.page.locator("saturn-text").filter(has_text="Tenant:").inner_text()
        except PlaywrightTimeoutError:
            return None

    def signout(self):
        """ Signout from GLC """
        self.user_btn.click()
        expect(self.logout_menu).to_be_visible()
        LOG.info("Signing out ...")
        self.logout_btn.click()
