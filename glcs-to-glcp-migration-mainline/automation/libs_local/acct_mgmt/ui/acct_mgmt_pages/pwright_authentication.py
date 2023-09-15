"""
This file holds library functions for Authentication test functions

"""
import logging
import os

from hpe_glcp_automation_lib.libs.authn.ui.login_to_homepage import Login
from hpe_glcp_automation_lib.libs.utils.pwright.pwright_utils import PwrightUtils
from hpe_glcp_automation_lib.libs.utils.random_gens import RandomGenUtils

log = logging.getLogger(__name__)

RECORD_DIR = os.path.join('tmp', 'results')


class AuthenticationPaths:
    """
    Class holding authentication locators

    """
    apps_btn_xpath: str = 'data-testid=apps-btn'
    mng_acct_btn_xpath: str = 'data-testid=desc-header-apps-manage-account'
    authentication_tile_xpath: str = 'data-testid=authentication-summary'
    claim_domain_modal_xpath: str = 'data-testid=claim-domain-modal'
    set_saml_connection_button_xpath: str = 'data-testid=set-saml-connection'
    domain_name_input_xpath: str = "//input[@data-testid='domain-name-input']"
    continue_button_xpath: str = 'data-testid=continue-btn'
    metadata_url_xpath: str = "//label[@for='Metadata URL']"
    metadata_url_input_xpath: str = 'data-testid=metadata-url-input'
    validate_url_button_xpath: str = 'data-testid=validate-url-button'
    next_button_xpath: str = 'data-testid=button-next'
    field_name_dropdown_xpath: str = 'data-testid=field-name-dropdown'
    nameid_dropdown_option_xpath: str = "//button[contains(text(),'NameId')]"
    hpe_ccs_attribute_xpath: str = 'data-testid=hpe-ccs-attribute-input'
    recovery_password_xpath: str = "//input[@name='password']"
    emergency_email_input_xpath: str = "//input[@name='email']"
    review_domain_name_text_xpath: str = 'data-testid=text-obj-list-value'
    finish_button_xpath: str = 'data-testid=button-finish'
    sso_setup_complete_text_xpath: str = 'data-testid=heading-title'
    exit_button_xpath: str = 'data-testid=exit-modal-btn'
    manual_metadata_xpath: str = "//label[@for='Manual (Enter X.509 Certificate Details)']"
    entity_id_input_xpath: str = 'data-testid=entity-id-input'
    domain_logout_input_xpath: str = 'data-testid=logout-url-input'
    domain_login_url_input_xpath: str = 'data-testid=login-url-input'
    signing_cert_input_xpath: str = 'data-testid=signing-cert-input'
    add_domain_text_xpath: str = "//*[contains(text(),'Claim a Domain')]"
    saml_homepage_heading_text_xpath: str = 'data-testid=heading-selected-authmethod-title'
    popup_add_domain_form_global_error_xpath: str = 'data-testid=form-global-error-message'
    set_up_acct_path = "data-testid=create-account-button"
    company_name_input_xpath: str = "data-testid=set-up-account-company-name-input"
    company_country_select_xpath: str = "//body/div[@id='root']/div[1]/div[1]/div[1]" \
                                        "/div[1]/div[2]/div[1]/div[1]/form[1]/div[2]/div[1]" \
                                        "/button[1]/div[1]/div[1]/div[1]/input[1]"
    company_search_xpath: str = "//body/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/input[1]"
    us_company_xpath: str = "//button[contains(text(),'United States')]"
    street_address_input_xpath: str = "data-testid=set-up-account-street-address-input"
    city_state_input_xpath: str = "data-testid=set-up-account-city-state-address-input"
    zipcode_input_xpath: str = "data-testid=set-up-account-zip-code-input"
    phone_input_xpath: str = "data-testid=set-up-account-phone-number-input"
    email_input_xpath: str = "data-testid=set-up-account-email-input"
    legal_terms_checkbox_xpath: str = "data-testid=text-setup-company-terms"
    create_acct_button_xpath: str = "data-testid=set-up-account-submit"
    switch_acct_button_xpath: str = "data-testid=switch-account-btn"
    create_new_acct_xpath: str = "data-testid=create-new-account-button"
    skip_for_now_xpath: str = "data-testid=skip-btn"
    recovery_user_email_input_xpath: str = 'data-testid=user-recovery-email'
    glcp_header_all_menu_button_xpath: str = 'data-testid=drop-btn-glcp-header-all-menu-item-user'
    sign_out_nav_xpath: str = 'data-testid=text-desc-sign-out-hpe-nav-menu'
    dashboard_nav_menu_xpath: str = 'data-testid=text-desc-dashboard-nav-menu'
    launch_btn_xpath: str = "(//*[contains(@data-testid, 'launch-btn')])[1]"
    account_search_input_xpath: str = 'data-testid=search-field'
    domain_actions_btn_xpath: str = 'data-testid=multipleactions-action-btn'
    account_count_xpath: str = "//span[@data-testid='text-total-accounts']/b"
    domain_delete_action_xpath: str = 'data-testid=action-4'
    domain_delete_btn_xpath: str = 'data-testid=delete-btn'
    domain_delete_confirmation_xpath: str = "//span[contains(text(),'Domain Removed Successfully')]"


class AuthenticationPage:
    """
    Class for defining Authentication methods

    """

    def __init__(self, test_data, login_data, current_env, hostname, saml_data, acct_data):
        self.selectors = AuthenticationPaths()
        self.s_shot = PwrightUtils()
        self.test_login_data = test_data
        self.login_data = login_data
        self.current_env = current_env
        self.hostname = hostname
        self.saml_data = saml_data
        self.acct_data = acct_data
        log.info(f"Initialize {__name__}")

    def go_to_authentication_page(self, page, test_name):
        """
        Fetches the authentication page

        :param page: page instance
        :param test_name: name of the test function
        :return: boolean
        """
        try:
            page.click(self.selectors.apps_btn_xpath)
            self.s_shot.save_screenshot(page, test_name)
            page.click(self.selectors.mng_acct_btn_xpath)
            self.s_shot.save_screenshot(page, test_name)
            page.click(self.selectors.authentication_tile_xpath)
            self.s_shot.save_screenshot(page, test_name)
        except Exception as e:
            log.error("Error running testcase: {}".format(e))
            return False

    def set_up_acct(self, page, test_name, account_name):
        """
        Sets up the account

        :param page: page instance
        :param test_name: name of the test function
        :param account_name: account name
        :return: boolean
        """
        try:
            page.fill(self.selectors.company_name_input_xpath, account_name)
            page.click(self.selectors.company_country_select_xpath)
            page.fill(self.selectors.company_search_xpath, 'United States')
            page.click(self.selectors.us_company_xpath)
            page.fill(self.selectors.street_address_input_xpath, self.acct_data['street_addr'])
            page.fill(self.selectors.city_state_input_xpath, self.acct_data['city_state'])
            page.fill(self.selectors.zipcode_input_xpath, self.acct_data['zip'])
            page.fill(self.selectors.phone_input_xpath, self.acct_data['phone'])
            page.fill(self.selectors.email_input_xpath, self.acct_data['email'])
            page.click(self.selectors.legal_terms_checkbox_xpath)
            self.s_shot.save_screenshot(page, test_name)
            page.click(self.selectors.create_acct_button_xpath)
            page.locator(f'text={account_name}')
        except Exception as e:
            log.error("not able to create account {}".format(e))
            return False

    def check_saml_homepage_text(self, page, test_name):
        """
        Checks SAML homepage text

        :param page: page instance
        :param test_name: name of the test function
        :return: boolean
        """
        try:
            self.go_to_authentication_page(page, test_name)
            saml_heading = \
                page.locator(self.selectors.saml_homepage_heading_text_xpath).is_visible()
            self.s_shot.save_screenshot(page, test_name)

            if saml_heading:
                self.s_shot.save_screenshot(page, test_name)
                return True
            else:
                raise Exception("SAML heading not found")
        except Exception as e:
            log.error("Error running testcase: {}".format(e))
            return False

    def check_saml_setup_popup(self, page, test_name):
        """
        Checks the SAML set up pop up

        :param page: page instance
        :param test_name: name of the test function
        :return: boolean
        """
        try:
            self.go_to_authentication_page(page, test_name)
            page.click(self.selectors.set_saml_connection_button_xpath)
            add_domain_popup = page.locator(self.selectors.claim_domain_modal_xpath).is_visible()
            if add_domain_popup:
                self.s_shot.save_screenshot(page, test_name)
                return True
            else:
                self.s_shot.save_screenshot(page, test_name)
                raise Exception("Popup not visible")
        except Exception as e:
            self.s_shot.save_screenshot(page, test_name)
            log.error("Error running testcase: {}".format(e))
            return False

    def check_input_domain_error(self, page, test_name):
        """
        Checks for domain input error

        :param page: page instance
        :param test_name: name of the test function
        :return: None
        """
        try:
            self.go_to_authentication_page(page, test_name)
            page.click(self.selectors.set_saml_connection_button_xpath)
            self.s_shot.save_screenshot(page, test_name)
            page.click(self.selectors.continue_button_xpath)
            page.wait_for_selector(self.selectors.popup_add_domain_form_global_error_xpath)
            error_msg = \
                page.locator(self.selectors.popup_add_domain_form_global_error_xpath).is_visible()
            if error_msg:
                self.s_shot.save_screenshot(page, test_name)
                return True
            else:
                self.s_shot.save_screenshot(page, test_name)
                raise Exception("Error fields not visible")
        except Exception as e:
            log.error("Error running testcase {}".format(e))
            return False

    def check_saml_addition(self, page, test_name, addition_type):
        try:
            account_name = self.saml_data['acct_name_1']
            login_creds = self.login_data[self.current_env]['users']
            self.go_to_authentication_page(page, test_name)
            page.click(self.selectors.set_saml_connection_button_xpath)
            self.s_shot.save_screenshot(page, test_name)
            page.fill(self.selectors.domain_name_input_xpath, self.saml_data["domain_name"])
            page.click(self.selectors.continue_button_xpath)
            self.s_shot.save_screenshot(page, test_name)
            if addition_type == 'url':
                page.click(self.selectors.metadata_url_xpath)
                page.fill(self.selectors.metadata_url_input_xpath, self.saml_data["metadata_url"])
                page.click(self.selectors.validate_url_button_xpath)
                self.s_shot.save_screenshot(page, test_name)
            elif addition_type == 'manual':
                account_name = self.saml_data['acct_name_2']
                page.click(self.selectors.manual_metadata_xpath)
                page.fill(self.selectors.entity_id_input_xpath,
                          self.saml_data["entity_id"])
                page.fill(self.selectors.domain_login_url_input_xpath,
                          self.saml_data["domain_login_url"])
                page.fill(self.selectors.domain_logout_input_xpath,
                          self.saml_data["domain_logout_url"])
                page.fill(self.selectors.signing_cert_input_xpath,
                          self.saml_data["signing_cert"])
                self.s_shot.save_screenshot(page, test_name)
            page.click(self.selectors.next_button_xpath)
            page.click(self.selectors.field_name_dropdown_xpath)
            page.click(self.selectors.nameid_dropdown_option_xpath)
            page.fill(self.selectors.hpe_ccs_attribute_xpath, self.saml_data["hpe_ccs_attr"])
            self.s_shot.save_screenshot(page, test_name)
            page.click(self.selectors.next_button_xpath)
            recovery_mail = page.input_value(self.selectors.recovery_user_email_input_xpath)
            page.fill(self.selectors.recovery_password_xpath, login_creds["saml_recovery_password"])
            page.fill(self.selectors.emergency_email_input_xpath, self.saml_data["emergency_email"])
            self.s_shot.save_screenshot(page, test_name)
            page.click(self.selectors.next_button_xpath)
            self.s_shot.save_screenshot(page, test_name)
            page.click(self.selectors.finish_button_xpath)
            page.locator('text=SSO Setup Complete')
            page.click(self.selectors.exit_button_xpath)
            page.click(self.selectors.skip_for_now_xpath)
            page.locator(f'text={self.saml_data["domain_name"]}')
            self.s_shot.save_screenshot(page, test_name)
            page.click(self.selectors.dashboard_nav_menu_xpath)
            self.s_shot.save_screenshot(page, test_name)
            page.click(self.selectors.switch_acct_button_xpath)
            self.s_shot.save_screenshot(page, test_name)
            page.click(self.selectors.launch_btn_xpath)
            self.s_shot.save_screenshot(page, test_name)
            page.click(self.selectors.switch_acct_button_xpath)
            page.fill(self.selectors.account_search_input_xpath, account_name)
            self.s_shot.save_screenshot(page, test_name)
            acct_count = page.locator(self.selectors.account_count_xpath).inner_text()
            if int(acct_count) > 0:
                raise Exception("Account claiming domain shouldn't be visible")
            page.click(self.selectors.glcp_header_all_menu_button_xpath)
            self.s_shot.save_screenshot(page, test_name)
            page.click(self.selectors.sign_out_nav_xpath)
            tc_login = Login(recovery_mail, login_creds['saml_recovery_password'])
            do_login = tc_login.login_acct(page)
            vts = PwrightUtils()
            vts.verify_test_step(do_login)
            self.go_to_authentication_page(page, test_name)
            self.s_shot.save_screenshot(page, test_name)
            page.click(self.selectors.domain_actions_btn_xpath)
            page.click(self.selectors.domain_delete_action_xpath)
            self.s_shot.save_screenshot(page, test_name)
            page.click(self.selectors.domain_delete_btn_xpath)
            self.s_shot.save_screenshot(page, test_name)
            page.locator(self.selectors.domain_delete_confirmation_xpath)
            self.s_shot.save_screenshot(page, test_name)
            page.click(self.selectors.glcp_header_all_menu_button_xpath)
            self.s_shot.save_screenshot(page, test_name)
            page.click(self.selectors.sign_out_nav_xpath)
            self.s_shot.save_screenshot(page, test_name)
            tc_login = Login(self.test_login_data['msp_username'],
                             login_creds[self.test_login_data['msp_username']])
            do_login = tc_login.login_acct(page)
            vts.verify_test_step(do_login)
            do_select_acct = tc_login.select_acct(page, account_name)
            self.s_shot.save_screenshot(page, test_name)
            vts.verify_test_step(do_select_acct)
            if recovery_mail:
                log.info("Recovery mail is {}".format(recovery_mail))
            return True
        except Exception as e:
            self.s_shot.save_screenshot(page, test_name)
            log.error("Error running testcase {}".format(e))
            return False

    def check_saml_addition_using_manual_metadata(self, page, test_name):
        try:
            account_name = "turidy{}".format(RandomGenUtils.random_string_of_chars(7))
            login_creds = self.login_data[self.current_env]['users']
            page.click(self.selectors.switch_acct_button_xpath)
            page.click(self.selectors.create_new_acct_xpath)
            self.set_up_acct(page, test_name, account_name)
            self.go_to_authentication_page(page, test_name)
            page.click(self.selectors.set_saml_connection_button_xpath)
            self.s_shot.save_screenshot(page, test_name)
            page.fill(self.selectors.domain_name_input_xpath, self.saml_data["domain_name"])
            page.click(self.selectors.continue_button_xpath)
            self.s_shot.save_screenshot(page, test_name)
            page.click(self.selectors.manual_metadata_xpath)
            page.fill(self.selectors.entity_id_input_xpath, self.saml_data["entity_id"])
            page.fill(self.selectors.domain_login_url_input_xpath,
                      self.saml_data["domain_login_url"])
            page.fill(self.selectors.domain_logout_input_xpath,
                      self.saml_data["domain_logout_url"])
            page.fill(self.selectors.signing_cert_input_xpath,
                      self.saml_data["signing_cert"])
            self.s_shot.save_screenshot(page, test_name)
            page.click(self.selectors.next_button_xpath)
            page.click(self.selectors.field_name_dropdown_xpath)
            page.click(self.selectors.nameid_dropdown_option_xpath)
            page.fill(self.selectors.hpe_ccs_attribute_xpath, self.saml_data["hpe_ccs_attr"])
            self.s_shot.save_screenshot(page, test_name)
            page.click(self.selectors.next_button_xpath)
            page.fill(self.selectors.recovery_password_xpath, login_creds["saml_recovery_password"])
            page.fill(self.selectors.emergency_email_input_xpath, self.saml_data["emergency_email"])
            self.s_shot.save_screenshot(page, test_name)
            page.click(self.selectors.next_button_xpath)
            self.s_shot.save_screenshot(page, test_name)
            page.click(self.selectors.finish_button_xpath)
            return True
        except Exception as e:
            self.s_shot.save_screenshot(page, test_name)
            log.error("Error running testcase {}".format(e))
            return False
