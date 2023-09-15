import logging
import os

from playwright.sync_api import Page

from hpe_glcp_automation_lib.libs.utils.pwright.pwright_utils import PwrightUtils
from hpe_glcp_automation_lib.libs.utils.random_gens import RandomGenUtils

log = logging.getLogger(__name__)

RECORD_DIR = os.path.join('tmp', 'results')


class UserManagementPaths:
    apps_btn_xpath: str = 'data-testid=apps-btn'
    mng_acct_btn_xpath: str = 'data-testid=desc-header-apps-manage-account'
    users_tab_xpath: str = 'data-testid=text-users-title'
    identity_and_access_tab_xpath: str = 'data-testid=text-identity-title'
    total_users_card_xpath: str = 'data-testid=card-total-users-tab'
    active_users_card_xpath: str = 'data-testid=card-active-users-tab'
    inactive_users_card_xpath: str = 'data-testid=card-inactive-users-tab'
    unverified_users_card_xpath: str = 'data-testid=card-unverified-users-tab'
    users_page_heading_title_xpath: str = 'data-testid=heading-page-title'
    user_invite_button_xpath: str = 'data-testid=invite-users-btn'
    user_data_table_xpath: str = 'data-testid=user-data-table'
    user_table_rows: str = "[data-testid='user-data-table'] tbody > tr"
    invite_user_popup_xpath: str = 'data-testid=invite-user-layer'
    invite_user_modal: str = 'data-testid=invite-user-modal'
    invite_user_email_input_xpath: str = 'data-testid=email-form-field-input'
    invite_user_role_dropdown: str = 'data-testid=roles-dropdown'
    invite_user_role_dropdown_option: str = 'data-testid=role-id-1'
    send_invite_button_xpath: str = 'data-testid=send-invite-btn'
    cancel_invite_button_xpath: str = 'data-testid=cancel-invite-btn'
    search_user_input_xpath: str = 'data-testid=search-field'
    user_table_action_button: str = 'data-testid=users-table-action-btn'
    row_delete_action_xpath: str = 'data-testid=action-2'
    delete_user_button_xpath: str = 'data-testid=delete-user-btn'
    confirm_delete_user_button_xpath: str = 'data-testid=confirm-delete-user-btn'
    new_user_row_xpath: str = "//*[contains(text(),'{}')]"


class UserManagementPage(object):
    def __init__(self):
        self.selectors = UserManagementPaths()
        log.info(f"Initialize {__name__}")

    def open_users_tab(self, page, test_name):
        """
        Checks for visibility of user cards

        :param page: page instance
        :param test_name: name of the test case
        :return: boolean
        """
        s_shot = PwrightUtils()
        page.click(self.selectors.apps_btn_xpath)
        page.click(self.selectors.mng_acct_btn_xpath)
        s_shot.save_screenshot(page, test_name)
        page.click(self.selectors.identity_and_access_tab_xpath)
        page.click(self.selectors.users_tab_xpath)
        s_shot.save_screenshot(page, test_name)

    def check_user_cards_visibility(self, page, test_name):
        """
        Checks for visibility of user cards

        :param page: page instance
        :param test_name: name of the test case
        :return: boolean
        """
        try:
            s_shot = PwrightUtils()
            self.open_users_tab(page, test_name)
            total_users = page.locator(self.selectors.total_users_card_xpath)
            active_users = page.locator(self.selectors.active_users_card_xpath)
            inactive_users = page.locator(self.selectors.inactive_users_card_xpath)
            unverified_users = page.locator(self.selectors.unverified_users_card_xpath)

            if total_users and active_users and inactive_users and unverified_users:
                s_shot.save_screenshot(page, test_name)
                return True
            else:
                raise Exception("Elements are not present")
        except Exception as e:
            log.error("not able to locate the details of user management page {}".format(e))
            return False

    def check_user_invite_button(self, page, test_name):
        """
        Checks for visibility of user cards

        :param page: page instance
        :param test_name: name of the test case
        :return: boolean
        """
        try:
            s_shot = PwrightUtils()
            self.open_users_tab(page, test_name)
            invite_button = page.locator(self.selectors.user_invite_button_xpath)
            if invite_button:
                s_shot.save_screenshot(page, test_name)
                return True
            else:
                raise Exception("Invite user button not present")
        except Exception as e:
            log.error("Error running testcase {}".format(e))
            return False

    def check_user_data_table(self, page, test_name):
        """
        Checks for visibility of user cards

        :param page: page instance
        :param test_name: name of the test case
        :return: boolean
        """
        try:
            s_shot = PwrightUtils()
            self.open_users_tab(page, test_name)
            data_table = page.locator(self.selectors.user_data_table_xpath)
            if data_table:
                s_shot.save_screenshot(page, test_name)
                return True
            else:
                raise Exception("users table not present")
        except Exception as e:
            log.error("Error running testcase {}".format(e))
            return False

    def check_invite_user_popup(self, page, test_name):
        """
        Checks for visibility of user cards

        :param page: page instance
        :param test_name: name of the test case
        :return: boolean
        """
        try:
            s_shot = PwrightUtils()
            self.open_users_tab(page, test_name)
            page.click(self.selectors.user_invite_button_xpath)
            popup = page.locator(self.selectors.invite_user_popup_xpath)
            if popup:
                s_shot.save_screenshot(page, test_name)
                return True
            else:
                raise Exception("invite popup not visible")
        except Exception as e:
            log.error("Error running testcase {}".format(e))
            return False

    def check_invite_user_flow(self, page, test_name):
        try:
            random_str = RandomGenUtils.random_string_of_chars(2)
            page.click(self.selectors.apps_btn_xpath)
            page.click(self.selectors.mng_acct_btn_xpath)
            PwrightUtils.save_screenshot(self, page, test_name)
            page.click(self.selectors.identity_and_access_tab_xpath)
            page.click(self.selectors.users_tab_xpath)
            PwrightUtils.save_screenshot(self, page, test_name)
            page.click(self.selectors.user_invite_button_xpath)
            PwrightUtils.save_screenshot(self, page, test_name)
            new_user_email: str = "admin+{}@gmail.com".format(random_str)
            page.fill(self.selectors.invite_user_email_input_xpath, new_user_email)
            page.click(self.selectors.invite_user_role_dropdown)
            page.click(self.selectors.invite_user_role_dropdown_option)
            page.click(self.selectors.send_invite_button_xpath)
            PwrightUtils.save_screenshot(self, page, test_name)
            # time.sleep(5)
            page.fill(self.selectors.search_user_input_xpath, new_user_email)
            new_user_row_xpath: str = "//*[contains(text(),'{}')]".format(new_user_email)
            PwrightUtils.save_screenshot(self, page, test_name)
            new_user_row = page.locator(new_user_row_xpath)
            if new_user_row:
                PwrightUtils.save_screenshot(self, page, test_name)
                return True
            else:
                raise Exception("selected user doesn't exists")
            return True
        except Exception as e:
            log.error("Error running testcase {}".format(e))
            return False

    def check_delete_user_flow(self, page: Page, test_name: str):
        """
        Checks delete user flow

        :param page: page instance
        :param test_name: name of the test case
        :return: boolean
        """
        try:
            random_str = RandomGenUtils.random_string_of_chars(5)
            s_shot = PwrightUtils()
            self.open_users_tab(page, test_name)
            page.click(self.selectors.user_invite_button_xpath)
            new_user_email: str = "user" + random_str + "@gmail.com"
            page.fill(self.selectors.invite_user_email_input_xpath, new_user_email)
            page.click(self.selectors.invite_user_role_dropdown)
            page.click(self.selectors.invite_user_role_dropdown_option)
            s_shot.save_screenshot(page, test_name)
            page.click(self.selectors.send_invite_button_xpath)
            page.locator(self.selectors.invite_user_modal).wait_for(state="hidden")
            page.fill(self.selectors.search_user_input_xpath, new_user_email)
            s_shot.save_screenshot(page, test_name)
            user_table_row = page.locator(f"{self.selectors.user_table_rows}:has-text('{new_user_email}')").first
            user_table_row.wait_for(state="visible")
            user_table_row.locator(self.selectors.user_table_action_button).click()
            page.click(self.selectors.row_delete_action_xpath)
            page.click(self.selectors.delete_user_button_xpath)
            page.click(self.selectors.confirm_delete_user_button_xpath)
            page.wait_for_selector(self.selectors.new_user_row_xpath.format(new_user_email),
                                   state='hidden')
            if not page.locator(self.selectors.new_user_row_xpath.format(
                    new_user_email)).is_visible():
                s_shot.save_screenshot(page, test_name)
                return True
            else:
                raise Exception("error deleting user")
        except Exception as e:
            log.error("Error running testcase: {}".format(e))
            return False
