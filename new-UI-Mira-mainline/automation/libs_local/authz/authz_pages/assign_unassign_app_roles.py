"""
This file holds functions to assign, unassign CCS roles

"""
import time
import logging

log = logging.getLogger(__name__)


class AssignUnassignRolePaths:
    """
    Class holding selectors for assigning and unassigning CCS roles

    """
    app_btn = 'data-testid=apps-btn'
    manage_acct = 'data-testid=text-desc-header-apps-manage-account'
    id_access_btn = 'data-testid=text-identity-title'
    roles_perm_tile = 'data-testid=text-roles-title'
    manage_nav_menu = 'data-testid=manage-nav-menu'
    identity_and_access = "data-testid=card-identity"
    users = 'data-testid=card-users'
    users_table_action_btn = 'data-testid=users-table-action-btn'
    assign_action = 'data-testid=action-1'
    applications_drop_down = 'data-testid=applications-dropdown'
    applications_value = 'text=Mira nms scale app'
    roles_drop_down = 'data-testid=roles-dropdown'
    custom_role_option = 'data-testid=option-custom_app_role1'
    lra_toggle = 'data-testid=toggle-btn-box'
    rrp_drop_down = 'data-testid=rrp-dropdown'
    rrp_value = 'data-testid=option-app_rrp1'
    assign_role_btn = "data-testid=assign-role-btn"
    confirm_assign_btn = "data-testid=confirm-assignment-role-btn"
    view_details_action = "data-testid=action-0"
    edit_access_btn = "text=Mira nms scale appcustom_app_role1Limited " \
                      "Access >> [aria-label='Open Drop']"
    remove_role = 'data-testid=action-1'
    save_btn = "data-testid=save-btn"
    users_back_button = "data-testid=user-back-btn"
    user_account_btn = "data-testid=drop-btn-glcp-header-all-menu-item-user"
    sign_out_btn = "data-testid=sign-out-hpe-nav-menu"


class AssignUnassignAppRolePage:
    """
    Class for defining methods of Assign Unassign role page
    """
    def __init__(self):
        self.selectors = AssignUnassignRolePaths()
        log.info(f"Initialize {__name__}")

    def assign_unassign_app_role(self, page):
        """
        Assigns/unassigns app role

        :param page: page instance
        :return: boolean
        """
        try:
            page.locator(self.selectors.manage_nav_menu).click()
            page.locator(self.selectors.identity_and_access).click()

            page.locator(self.selectors.users).click()
            page.wait_for_selector(self.selectors.users_table_action_btn)
            page.locator(self.selectors.users_table_action_btn).click()

            page.wait_for_selector(self.selectors.assign_action)
            page.locator(self.selectors.assign_action).click()

            page.wait_for_selector(self.selectors.applications_drop_down)
            page.locator(self.selectors.applications_drop_down).click()

            page.wait_for_selector(self.selectors.applications_value)
            page.locator(self.selectors.applications_value).click()

            time.sleep(1)
            page.wait_for_selector(self.selectors.roles_drop_down)
            page.locator(self.selectors.roles_drop_down).click()

            page.locator(self.selectors.custom_role_option).click()
            time.sleep(1)

            page.wait_for_selector(self.selectors.lra_toggle)
            page.locator(self.selectors.lra_toggle).click()

            page.wait_for_selector(self.selectors.rrp_drop_down)
            page.locator(self.selectors.rrp_drop_down).click()

            page.locator(self.selectors.rrp_value).click()

            page.locator(self.selectors.assign_role_btn).click()

            if page.is_visible(self.selectors.confirm_assign_btn):
                page.locator(self.selectors.confirm_assign_btn).click()

            page.locator(self.selectors.users_table_action_btn).click()

            page.locator(self.selectors.view_details_action).click()

            page.locator(self.selectors.edit_access_btn).click()

            page.locator(self.selectors.remove_role).click()

            page.locator(self.selectors.save_btn).click()

            page.locator(self.selectors.users_back_button).click()

            page.locator(self.selectors.user_account_btn).click()

            with page.expect_navigation():
                page.locator(self.selectors.sign_out_btn).click()
            return True
        except Exception as e:
            log.error("not able to locate the role on the page {}".format(e))
            return False
