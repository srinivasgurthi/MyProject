
import logging
import re

from playwright.sync_api import Page,expect

from hpe_glcp_automation_lib.libs.identity_access.base import IdentityAccessPage

LOG = logging.getLogger(__name__)


class DeleteUserPaths:
    delete_user_actn_btn1 :str = "action-1"
    delete_user_actn_btn0 :str = "action-0"
    delete_user_btn :str = "delete-user-btn"
    delete_user_button_xpath: str = "data-testid=delete-user-btn"
    confirm_delete_user_btn: str = "confirm-delete-user-btn"



class UserRolePaths:
    pass


class UserManagementPaths(DeleteUserPaths,UserRolePaths):
    apps_btn_xpath: str = "data-testid=apps-btn"
    mng_acct_btn_xpath: str = "data-testid=desc-header-apps-manage-account"
    users_tab_xpath: str = "data-testid=text-users-title"
    identity_and_access_tab_xpath: str = "data-testid=text-identity-title"
    total_users_card_xpath: str = "data-testid=card-total-users-tab"
    active_users_card_xpath: str = "data-testid=card-active-users-tab"
    inactive_users_card_xpath: str = "data-testid=card-inactive-users-tab"
    unverified_users_card_xpath: str = "data-testid=card-unverified-users-tab"
    users_page_heading_title_xpath: str = "data-testid=heading-page-title"
    user_invite_button_xpath: str = "data-testid=invite-users-btn"
    user_data_table_xpath: str = "data-testid=user-data-table"
    user_table_rows: str = "[data-testid='user-data-table'] tbody > tr"
    invite_user_popup_xpath: str = "data-testid=invite-user-layer"
    invite_user_modal: str = "data-testid=invite-user-modal"
    invite_user_email_input_xpath: str = "data-testid=email-form-field-input"
    invite_user_role_dropdown: str = "data-testid=roles-dropdown"
    invite_user_role_dropdown_option: str = "data-testid=role-id-{}"
    send_invite_button_xpath: str = "data-testid=send-invite-btn"
    cancel_invite_button_xpath: str = "data-testid=cancel-invite-btn"
    search_user_input_xpath: str = "data-testid=search-field"
    user_table_action_button: str = "data-testid=users-table-action-btn"
    row_delete_action_xpath: str = "data-testid=action-2"
    confirm_delete_user_button_xpath: str = "data-testid=confirm-delete-user-btn"
    new_user_row_xpath: str = "//*[contains(text(),'{}')]"
    text_user_title_locator: str = "text-users-title"
    user_details_actn_button:str = "user-details-action-btn"
    confirm_assignment_btn :str = "confirm-assignment-role-btn"
    assign_role_btn :str = "assign-role-btn"
    search_field :str = "search-field"



class UserManagmentRoles:
    pass




class UsersPage(IdentityAccessPage):
    def __init__(self, page: Page) -> None:
        IdentityAccessPage.__init__(self, page)
        self.selectors = UserManagementPaths()
        self.roles = {
            "Account Administrator Built-in": 0,
            "Observer Built-in": 1,
            "Operator Built-in": 2
        }
        LOG.info(f"Initialize {__name__}")

    def open_users_tab(self):
        """
            Navigate to users tab 
            
        """
        self.page.click(self.selectors.apps_btn_xpath)
        self.page.click(self.selectors.mng_acct_btn_xpath)
        self.page.click(self.selectors.identity_and_access_tab_xpath)
        self.page.click(self.selectors.users_tab_xpath)

    def navigate_to_manage_users_page(self):
        """
        Navigate to manage users section

        return: None
        """
        LOG.info("Navigate to manage users page ")
        self.navigate_to_manage_identity_and_access_page()
        self.page.get_by_test_id(self.selectors.text_user_title_locator).click()
        self.page.wait_for_url(url=re.compile(r"users"))

    def search_user(self, email_address) -> None:
        """
        Search user with arg: {password}
        
        :param: email_address: (required)
        :return: None
        """
        
        """ Search users for there {email address} """
        LOG.info(f"Search user: {email_address}")
        self.page.get_by_test_id(self.selectors.search_field).fill(email_address.split("@")[0])
        self.page.get_by_text(email_address).click()

    def check_role(
        self,
        email_address: str,
        role: str = "Account Administrator Built-in",
    ):
        """Check whether specified {role} for {email_address} is present or not."""
        role = role.replace("Built-in", "").strip()
        LOG.info(
            f"Check role {role} for user {email_address}."
        )
        self.page.wait_for_load_state()
        if role in  self.page.locator(":below(:text(\"Role\"))").locator("tbody").text_content():
            return True
        return False
    
    def assign_role(
        self,
        email_address: str,
        appliance_name: str = "HPE Greenlake",
        role: str = "Account Administrator Built-in",
    ):
        """Assign specific {role} to a user with {email_address} under {appliance_name}
        :param: email_address: (required)
        :param: appliance_name: (optional)
        :param: role: (optional)
        :return: None
        
        """
        LOG.info(
            f"Assign role {role} to user {email_address} in appliance {appliance_name}"
        )
        self.search_user(email_address)
        self.page.get_by_test_id(self.selectors.user_details_actn_button).get_by_role(
            "button", name="Open Drop"
        ).click()
        self.page.get_by_test_id(self.selectors.assign_role_btn).click()
        self.page.get_by_role("button", name="Select Application").click()
        self.page.get_by_role("option", name=f"{appliance_name}").click(delay=1000)
        self.page.get_by_role("button", name="Select Role").click()
        self.page.get_by_role("option", name=f"{role}", exact=True).click(delay=1000)
        self.page.get_by_test_id("two-buttons").get_by_test_id(self.selectors.assign_role_btn).click(delay=1000)
        self.page.get_by_test_id(self.selectors.confirm_assignment_btn).click(delay=1000)
        self.page.wait_for_load_state()
        self.page.wait_for_load_state()
        self.page.reload()
        self.page.wait_for_load_state()

    

    def delete_user(self, email_address: str) -> None:
        """Delete user with specified {email_address}
        :param: email_address: (required)
        :return: None
        """
        LOG.info(f"Delete user: {email_address}")
        self.search_user(email_address)
        self.page.get_by_test_id(self.selectors.user_details_actn_button).get_by_role(
            "button", name="Open Drop"
        ).click()
        self.page.get_by_test_id(self.selectors.delete_user_actn_btn0).click()
        self.page.get_by_test_id(self.selectors.delete_user_btn).click()
        self.page.wait_for_load_state()
        self.page.get_by_test_id(self.selectors.confirm_delete_user_btn).click()
        self.page.wait_for_load_state()
        self.page.wait_for_url(url=re.compile(r"users"))
        self.page.wait_for_selector(
            self.selectors.new_user_row_xpath.format(email_address), state="hidden"
        )

    def delete_role(self, email_address: str, role: str) -> None:
        """Delete a role with {email_address} under {appliance_name}
        :param: email_address: (required)
        :param: role: (required)
        :return: None
        
        """
        
        LOG.info(f"Delete role {role} from user {email_address}")
        role = role.replace("Built-in", "").strip()
        self.search_user(email_address)
        self.page.get_by_test_id("multipleactions-action-btn").get_by_role(
            "button", name="Open Drop"
        ).click()
        self.page.get_by_test_id("action-1").click()
        self.page.get_by_test_id("content").get_by_text(f"{role}").click()
        self.page.get_by_test_id("save-btn").click()
        self.page.wait_for_selector("[data-testid='notification-status-ok']")

    def delete_recursive_role(self, email_address: str, role: str) -> None:
        """Delete a recursive role with {email_address} for role {role}
        :param: email_address: (required)
        :param: role: (required)
        :return: None
        """
        LOG.info(f"Delete role {role} from user {email_address}")
        role = role.replace("Built-in", "").strip()
        self.search_user(email_address)
        self.page.wait_for_timeout(2000)
        roles_locator = self.page.locator('[data-testid="multipleactions-action-btn"]').all()
        no_of_roles = len(roles_locator)
        LOG.info(f"{no_of_roles} roles found!")
        for i in range(0, no_of_roles):
            roles_locator[0].click()
            self.page.get_by_test_id("action-1").click()
            self.page.get_by_test_id("save-btn").click()
            self.page.wait_for_selector("[data-testid='notification-status-ok']")
            LOG.info(f"Role removed")
        self.page.wait_for_timeout(2000)

    def invite_user(self, new_user_email: str, role: str) -> bool:
        """ Invite user with {email_address} for role {role}
        :param: email_address: (required)
        :param: role: (required)
        :return: None
        """
        role_id = self.roles[role]
        self.page.click(self.selectors.user_invite_button_xpath)
        self.page.fill(
            self.selectors.invite_user_email_input_xpath, new_user_email
        )
        self.page.click(self.selectors.invite_user_role_dropdown)
        self.page.click(self.selectors.invite_user_role_dropdown_option.format(role_id))
        self.page.click(self.selectors.send_invite_button_xpath)
        self.page.wait_for_load_state()

        try:
            expect(self.page.locator("div").locator("span",has_text='This email address is already being used.')).not_to_be_visible()
        except Exception as e:
            LOG.info(f"Email already exist!.")
            return False

        # expect(self.page.get_by_text("Unable to sign in")).to_be_visible()

        self.page.fill(self.selectors.search_user_input_xpath, new_user_email)
        self.page.wait_for_load_state()
        new_user_row_xpath: str = "//*[contains(text(),'{}')]".format(new_user_email)
        email = self.page.locator(new_user_row_xpath).inner_text()
        if email == new_user_email:
            LOG.info(f"{email} invited.")
            return True
        else:
            LOG.info(f"{email} failed to invite.")
            return False

    def check_role_assigned(self, email, role):
        """Check Role assigned for email {email} for {role
        
        
        
        }
        :param: email_address: (required)
        :param: appliance_name: (optional)
        :param: role: (optional)
        :return: None
        
        """
        self.search_user(email_address=email)
        self.page.wait_for_selector("[data-testid='assign-role-btn']")
        LOG.info(role)
        role_split = role.split(" ")
        if role == "Account Administrator Built-in":
            assigned_role_xpath: str = "//span[text()='Account Administrator']"
        else:
            assigned_role_xpath: str = "//span[text()='{}']".format(role_split[0])
        role_exist = self.page.locator(assigned_role_xpath).is_visible()
        LOG.info(role_exist)
        return role_exist

    def get_status(self):
        status = self.page.locator("[data-testid='text-user-status']").text_content()
        return status