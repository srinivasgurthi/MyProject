import json
import logging
import os
import time

from hpe_glcp_automation_lib.libs.authn.ui.login_to_homepage import Login
from hpe_glcp_automation_lib.libs.utils.pwright.pwright_utils import PwrightUtils

log = logging.getLogger(__name__)

record_dir = '/tmp/results/'

if os.getenv("POD_NAMESPACE") is None:
    with open(os.path.join(os.path.abspath(os.getcwd()), "test_pwright/web_commons_pwright/users_creds.json")) as fd:
        login_data = json.load(fd)

else:
    with open(os.path.join(os.path.dirname(__file__), "/opt/ccs/sol-auto/creds/acct_mgmt_login_info.json")) as fd:
        login_data = json.load(fd)


class MSPToStandardConversionPaths:
    apps_btn_xpath: str = 'data-testid=apps-btn'
    mng_acct_btn_xpath: str = 'data-testid=desc-header-apps-manage-account'
    manage_acct_type_button_xpath: str = 'data-testid=manage-account-type-btn'
    msp_account_heading_xpath: str = 'data-testid=msp-account-heading'
    standard_account_heading_xpath: str = 'data-testid=std-account-heading'
    current_acct_text_xpath: str = 'data-testid=text-current-account-btn'
    convert_account_button_xpath: str = 'data-testid=convert-account-button'
    convert_account_dialog_xpath: str = 'data-testid=convert-account-dialog'
    submit_btn_xpath: str = 'data-testid=submit-btn'
    company_name_input_xpath: str = "data-testid=set-up-account-company-name-input"
    company_country_select_xpath: str = "//body/div[@id='root']/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/form[1]/div[2]/div[1]/button[1]/div[1]/div[1]/div[1]/input[1]"
    company_search_xpath: str = "//body/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/input[1]"
    us_company_xpath: str = "//button[contains(text(),'Albania')]"
    street_address_input_xpath: str = "data-testid=set-up-account-street-address-input"
    city_state_input_xpath: str = "data-testid=set-up-account-city-state-address-input"
    zipcode_input_xpath: str = "data-testid=set-up-account-zip-code-input"
    phone_input_xpath: str = "data-testid=set-up-account-phone-number-input"
    email_input_xpath: str = "data-testid=set-up-account-email-input"
    legal_terms_checkbox_xpath: str = "data-testid=text-setup-company-terms"
    create_acct_button_xpath: str = "data-testid=set-up-account-submit"
    switch_acct_button_xpath: str = "data-testid=switch-account-btn"
    create_new_acct_xpath: str = "data-testid=create-new-account-button"
    check_eligibility_button_xpath: str = 'data-testid=check-eligibility-button'
    provide_acct_details_heading_xpath: str = "//[contains(text(),'Provide Account Details')]"
    radio_deliver_button_xpath: str = "//div[@data-testid='input-radio-deliver-nm']/label[1]"
    network_as_a_service_dropdown_xpath: str = 'data-testid=input-select-nw-as-a-svs'
    ntwrk_service_all_option_xpath: str = "//button[contains(text(),'All')]"
    operating_country_dropdown_xpath: str = 'data-testid=input-select-operating-country'
    operating_country_search_xpath: str = "//body/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/input[1]"
    operating_country_xpath: str = "//button[contains(text(),'Albania')]"
    customer_located_geo_dropdown_xpath: str = 'data-testid=input-select-customer-located'
    multi_geo_xpath: str = "//button[contains(text(),'Multi Geo')]"
    number_of_networks_input_xpath: str = 'data-testid=input-text-num-of-nw'
    text_email_input_xpath: str = 'data-testid=input-text-email'
    sales_rep_email_input_xpath: str = 'data-testid=input-text-sales-rep-email'
    submit_eligibility_check_button_xpath: str = 'data-testid=button-next'
    you_are_eligible_text_xpath: str = "//[contains(text(),'You Are Eligible')]"
    finish_eligibility_check_button_xpath: str = 'data-testid=button-finish'
    account_type_val_xpath: str = 'data-testid=paragraph-account-type-val'


class MSPToStandardConversionPage(object):
    def __init__(self, setting):
        self.pw_utils = PwrightUtils()
        self.selectors = MSPToStandardConversionPaths()
        self.test_login_data = setting.test_data
        self.curr_env = setting.current_env

        log.info(f"Initialize {__name__}")

    def __check_account_type(self, page, test_name) -> str:
        try:
            acct_type = page.locator(self.selectors.account_type_val_xpath)
            return acct_type.inner_text()
        except Exception as e:
            log.error(f"account type check failed in test {test_name}: {e}")
            return ""

    def check_standalone_to_msp_account_conversion(self, page, test_name):
        try:
            time.sleep(5)
            eligibility_button = page.query_selector(
                self.selectors.check_eligibility_button_xpath)
            if eligibility_button:
                page.click(self.selectors.check_eligibility_button_xpath)
                page.locator(self.selectors.provide_acct_details_heading_xpath)
                self.pw_utils.save_screenshot(page, test_name)
                page.click(self.selectors.radio_deliver_button_xpath)
                self.pw_utils.save_screenshot(page, test_name)
                page.click(self.selectors.network_as_a_service_dropdown_xpath)
                page.click(self.selectors.ntwrk_service_all_option_xpath)
                self.pw_utils.save_screenshot(page, test_name)
                page.click(self.selectors.operating_country_dropdown_xpath)
                self.pw_utils.save_screenshot(page, test_name)
                page.fill(
                    self.selectors.operating_country_search_xpath, 'Albania')
                page.click(self.selectors.operating_country_xpath)
                self.pw_utils.save_screenshot(page, test_name)
                page.click(self.selectors.customer_located_geo_dropdown_xpath)
                page.click(self.selectors.multi_geo_xpath)
                self.pw_utils.save_screenshot(page, test_name)
                page.fill(self.selectors.number_of_networks_input_xpath, '500')
                page.fill(self.selectors.text_email_input_xpath,
                          self.test_login_data['msp_username'])
                page.fill(self.selectors.sales_rep_email_input_xpath,
                          self.test_login_data['msp_username'])
                self.pw_utils.save_screenshot(page, test_name)
                page.click(
                    self.selectors.submit_eligibility_check_button_xpath)
                page.locator(self.selectors.you_are_eligible_text_xpath)
                self.pw_utils.save_screenshot(page, test_name)
                page.click(
                    self.selectors.finish_eligibility_check_button_xpath)
                time.sleep(5)
                self.pw_utils.save_screenshot(page, test_name)

            page.click(self.selectors.convert_account_button_xpath)
            self.pw_utils.save_screenshot(page, test_name)
            page.locator(self.selectors.convert_account_dialog_xpath)
            self.pw_utils.save_screenshot(page, test_name)
            page.click(self.selectors.submit_btn_xpath)
            time.sleep(10)
            self.pw_utils.save_screenshot(page, test_name)
            login_creds = login_data[self.curr_env]['users']
            tc_login = Login(
                self.test_login_data['msp_username'], login_creds[self.test_login_data['msp_username']])
            do_login = tc_login.login_acct(page)
            self.pw_utils.verify_test_step(do_login)
            time.sleep(10)
            do_select_acct = tc_login.select_acct(
                page, self.test_login_data['msp_acct_name_2'])
            self.pw_utils.verify_test_step(do_select_acct)
            self.pw_utils.save_screenshot(page, test_name)

            page.click(self.selectors.apps_btn_xpath)
            page.click(self.selectors.mng_acct_btn_xpath)
            self.pw_utils.save_screenshot(page, test_name)
        except Exception as e:
            log.error("testcase failed: {}".format(e))
            return False

    def check_msp_to_standalone_account_conversion(self, page, test_name):
        try:
            page.click(self.selectors.apps_btn_xpath)
            page.click(self.selectors.mng_acct_btn_xpath)
            self.pw_utils.save_screenshot(page, test_name)

            if self.__check_account_type(page, test_name) == 'Standard Enterprise Account':
                page.click(self.selectors.manage_acct_type_button_xpath)
                self.pw_utils.save_screenshot(page, test_name)
                self.check_standalone_to_msp_account_conversion(
                    page, test_name)

            if self.__check_account_type(page, test_name) == 'Managed Service Provider Account':
                page.click(self.selectors.manage_acct_type_button_xpath)
                self.pw_utils.save_screenshot(page, test_name)
                page.locator(self.selectors.msp_account_heading_xpath).locator(
                    self.selectors.current_acct_text_xpath)
                page.click(self.selectors.convert_account_button_xpath)
                self.pw_utils.save_screenshot(page, test_name)
                page.locator(self.selectors.convert_account_dialog_xpath)
                self.pw_utils.save_screenshot(page, test_name)
                page.click(self.selectors.submit_btn_xpath)
                time.sleep(10)
                self.pw_utils.save_screenshot(page, test_name)
                login_creds = login_data[self.curr_env]['users']
                tc_login = Login(
                    self.test_login_data['msp_username'], login_creds[self.test_login_data['msp_username']])
                do_login = tc_login.login_acct(page)
                self.pw_utils.verify_test_step(do_login)
                time.sleep(10)
                do_select_acct = tc_login.select_acct(
                    page, self.test_login_data['msp_acct_name_2'])
                self.pw_utils.verify_test_step(do_select_acct)
                self.pw_utils.save_screenshot(page, test_name)
                page.click(self.selectors.apps_btn_xpath)
                page.click(self.selectors.mng_acct_btn_xpath)
                self.pw_utils.save_screenshot(page, test_name)
                if self.__check_account_type(page, test_name) == 'Standard Enterprise Account':
                    return True
                else:
                    raise Exception(
                        "MSP to Standard Account Conversion unsuccessfull")
        except Exception as e:
            log.error("testcase failed: {}".format(e))
            return False
