"""
This file holds library functions for IP access rules

"""
import logging
import os

from hpe_glcp_automation_lib.libs.utils.pwright.pwright_utils import PwrightUtils
from hpe_glcp_automation_lib.libs.utils.random_gens import RandomGenUtils

log = logging.getLogger(__name__)

RECORD_DIR = os.path.join('tmp', 'results')


class IPAccessRulesPaths:
    """
    Class holding IP access rules locators

    """
    apps_btn_xpath: str = 'data-testid=apps-btn'
    mng_acct_btn_xpath: str = 'data-testid=desc-header-apps-manage-account'
    ip_access_rules_tile_xpath: str = 'data-testid=text-ip-access-rules-title'
    access_rules_heading_xpath: str = 'data-testid=heading-page-title'
    add_access_rule_xpath: str = 'data-testid=add-access-rule-btn'
    add_access_rule_modal_xpath: str = 'data-testid=add-access-rule-modal'
    single_ip_addr_input_xpath: str = 'data-testid=single_ip-form-field-input'
    description_textarea_xpath: str = 'data-testid=description-form-field-area'
    add_button_xpath: str = 'data-testid=add-btn'
    search_access_rule_input_xpath: str = 'data-testid=search-field'
    single_ip_row_text_xpath: str = "//span[contains(text(),'1.1.1.1')]"
    single_ip_row_action_xpath: str = "//tbody/tr[1]/td[4]/div[1]/div[1]/button[1]"
    delete_access_rule_action_xpath: str = 'data-testid=action-1'
    delete_access_rule_popup_xpath: str = 'data-testid=delete-access-modal-dialog'
    confirm_button_xpath: str = 'data-testid=confirm-btn'
    access_rule_deleted_notification: str = "//span[contains(text(),'Access Rule Deleted')]"


class IPAccessRulesPage:
    """
    Class holding methods for IP access rules
    """

    def __init__(self, access_rules_data):
        self.selectors = IPAccessRulesPaths()
        self.s_shot = PwrightUtils()
        self.access_rules_data = access_rules_data
        log.info(f"Initialize {__name__}")

    def check_access_rules_homepage(self, page, test_name):
        """
        Checks the access rules homepage

        :param page: page instance
        :param test_name: name of the test function
        :return: boolean
        """
        try:
            page.click(self.selectors.apps_btn_xpath)
            self.s_shot.save_screenshot(page, test_name)
            page.click(self.selectors.mng_acct_btn_xpath)
            self.s_shot.save_screenshot(page, test_name)
            page.click(self.selectors.ip_access_rules_tile_xpath)
            access_rules_heading = page.locator(self.selectors.access_rules_heading_xpath)
            if 'IP Access Rules' in access_rules_heading.inner_text():
                self.s_shot.save_screenshot(page, test_name)
                return True
            else:
                self.s_shot.save_screenshot(page, test_name)
                raise Exception("element not present")
        except Exception as e:
            log.error("testcase failed: {}".format(e))
            return False

    def check_add_delete_access_rules(self, page, test_name):
        """
        Validates add/delete IP access rules

        :param page: page instance
        :param test_name: name of the test function
        :return: boolean
        """
        try:
            random_str = RandomGenUtils.random_string_of_chars(5)
            page.click(self.selectors.apps_btn_xpath)
            self.s_shot.save_screenshot(page, test_name)
            page.click(self.selectors.mng_acct_btn_xpath)
            self.s_shot.save_screenshot(page, test_name)
            page.click(self.selectors.ip_access_rules_tile_xpath)
            self.s_shot.save_screenshot(page, test_name)
            page.click(self.selectors.add_access_rule_xpath)
            page.locator(self.selectors.add_access_rule_modal_xpath)
            self.s_shot.save_screenshot(page, test_name)
            page.fill(self.selectors.single_ip_addr_input_xpath,
                      self.access_rules_data['single_ip_addr_1'])
            page.fill(self.selectors.description_textarea_xpath, random_str)
            self.s_shot.save_screenshot(page, test_name)
            page.click(self.selectors.add_button_xpath)
            self.s_shot.save_screenshot(page, test_name)
            page.fill(self.selectors.search_access_rule_input_xpath,
                      self.access_rules_data['single_ip_addr_1'])
            page.locator(self.selectors.single_ip_row_text_xpath)
            self.s_shot.save_screenshot(page, test_name)
            page.click(self.selectors.single_ip_row_action_xpath)
            self.s_shot.save_screenshot(page, test_name)
            page.click(self.selectors.delete_access_rule_action_xpath)
            page.locator(self.selectors.delete_access_rule_popup_xpath)
            self.s_shot.save_screenshot(page, test_name)
            page.click(self.selectors.confirm_button_xpath)
            self.s_shot.save_screenshot(page, test_name)
            page.locator(self.selectors.access_rule_deleted_notification)
            self.s_shot.save_screenshot(page, test_name)
            return True
        except Exception as e:
            log.error("testcase failed: {}".format(e))
            return False
