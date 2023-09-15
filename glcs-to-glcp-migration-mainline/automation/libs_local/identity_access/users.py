
import logging
import re

from playwright.sync_api import Page,expect

from automation.updated_libs_local.identity_access.base import IdentityAccessPage

LOG = logging.getLogger(__name__)


class UserManagementPaths:
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
    delete_user_button_xpath: str = "data-testid=delete-user-btn"
    confirm_delete_user_button_xpath: str = "data-testid=confirm-delete-user-btn"
    new_user_row_xpath: str = "//*[contains(text(),'{}')]"




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
        Checks for visibility of user cards

        :param page: page instance
        :param test_name: name of the test case
        :return: boolean
        """
        self.page.click(self.selectors.apps_btn_xpath)
        self.page.click(self.selectors.mng_acct_btn_xpath)
        self.page.click(self.selectors.identity_and_access_tab_xpath)
        self.page.click(self.selectors.users_tab_xpath)

    def navigate_to_manage_users_page(self):
        LOG.info("Navigate to manage users page ")
        self.navigate_to_manage_identity_and_access_page()
        self.page.get_by_test_id("text-users-title").click()
        self.page.wait_for_url(url=re.compile(r"users"))

    def search_user(self, email_address) -> None:
        LOG.info(f"Search user: {email_address}")
        self.page.get_by_test_id("search-field").fill(email_address.split("@")[0])
        self.page.get_by_text(email_address).click()

    def check_role(
        self,
        email_address: str,
        role: str = "Account Administrator Built-in",
    ):
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
        LOG.info(
            f"Assign role {role} to user {email_address} in appliance {appliance_name}"
        )
        self.search_user(email_address)
        self.page.get_by_test_id("user-details-action-btn").get_by_role(
            "button", name="Open Drop"
        ).click()
        self.page.get_by_test_id("assign-role-btn").click()
        self.page.get_by_role("button", name="Select Application").click()
        self.page.get_by_role("option", name=f"{appliance_name}").click(delay=1000)
        self.page.get_by_role("button", name="Select Role").click()
        self.page.get_by_role("option", name=f"{role}", exact=True).click(delay=1000)
        self.page.get_by_test_id("two-buttons").get_by_test_id(
            "assign-role-btn"
        ).click(delay=1000)
        self.page.get_by_test_id("confirm-assignment-role-btn").click(delay=1000)
        self.page.wait_for_load_state()
        self.page.wait_for_load_state()
        self.page.reload()
        self.page.wait_for_load_state()

    

    def delete_user(self, email_address: str) -> None:
        LOG.info(f"Delete user: {email_address}")
        self.search_user(email_address)
        self.page.get_by_test_id("user-details-action-btn").get_by_role(
            "button", name="Open Drop"
        ).click()
        self.page.get_by_test_id("action-0").click()
        self.page.get_by_test_id("delete-user-btn").click()
        self.page.wait_for_load_state()
        self.page.get_by_test_id("confirm-delete-user-btn").click()
        self.page.wait_for_load_state()
        self.page.wait_for_url(url=re.compile(r"users"))
        self.page.wait_for_selector(
            self.selectors.new_user_row_xpath.format(email_address), state="hidden"
        )

    def delete_role(self, email_address: str, role: str) -> None:
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