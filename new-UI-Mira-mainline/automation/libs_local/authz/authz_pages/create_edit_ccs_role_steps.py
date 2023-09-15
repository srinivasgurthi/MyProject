"""
This file holds methods to create/edit CCS roles

"""
import time
import logging

log = logging.getLogger(__name__)


class CreateEditRolePaths:
    """
    Class holding selectors for create/edit CCS roles

    """
    app_btn = 'data-testid=apps-btn'
    manage_acct = 'data-testid=text-desc-header-apps-manage-account'
    card_identity = 'data-testid=card-identity'
    card_roles = 'data-testid=card-roles'
    roles_create = 'data-testid=roles-create-btn'
    app_dropdown = 'data-testid=application-dropdown'
    role_option = 'button[role=option]:has-text("HPE GreenLake platform")'
    role_input_button = 'data-testid=create-role-btn'
    role_name_input = 'data-testid=role-name-input'
    role_description_area = 'data-testid=role-description-input-area'
    next_button = 'data-testid=button-next'
    add_permissions = 'data-testid=add-permissions-btn'
    text_app_catalog = 'data-testid=text-Application Catalog'
    permissions_create_button = 'data-testid=permissions-create-btn'
    finish_button = 'data-testid=button-finish'
    custom_editing = 'text=ccs_custom_role1 for editing'
    edit_role = 'text=Edit Role'
    permissions_edit = 'data-testid=edit-permission-btn'
    permissions_edit_text = 'text=Add Permissions'
    listbox_audit_trial = 'ul[role="listbox"]:has-text("Audit Trail")'
    listbox_notification = 'ul[role="listbox"]:has-text("Notifications Service")'
    group_svg = 'div[role="group"] svg'
    group_div = 'div[role="group"] div'
    scope_edit_button = 'data-testid=permission-edit-save-btn'
    role_details_back = 'data-testid=role-details_back-btn'
    custom_role1 = 'text=ccs_custom_role1'
    actions_button = 'button:has-text("Actions")'
    delete_role = 'text=Delete Role'
    primary_button = 'data-testid=primary-btn'
    identity_title = 'data-testid=identity-title'
    glcp_header_all_menu = 'data-testid=drop-btn-glcp-header-all-menu-item-user'
    glcp_sign_out = 'data-testid=sign-out-hpe-nav-menu'


class CreateEditRolePage:
    """
    Class defining methods for create/edit CCS role page

    """
    def __init__(self):
        self.selectors = CreateEditRolePaths()
        log.info(f"Initialize {__name__}")

    def create_edit_ccs_role(self, page):
        """
        Creates/edits CCS roles

        :param page: page instance
        :return: boolean
        """
        try:
            page.locator(self.selectors.app_btn).click()

            page.locator(self.selectors.manage_acct).click()

            page.locator(self.selectors.card_identity).first.click()

            page.locator(self.selectors.card_roles).first.click()

            page.locator(self.selectors.roles_create).click()

            page.locator(self.selectors.app_dropdown).click()

            page.locator(self.selectors.role_option).click()

            page.locator(self.selectors.role_input_button).click()

            page.locator(self.selectors.role_name_input).fill("ccs_custom_role1")
            page.locator(self.selectors.role_description_area).fill("ccs_custom_role1 for editing")

            page.locator(self.selectors.next_button).click()

            page.locator(self.selectors.add_permissions).click()

            page.wait_for_selector(self.selectors.text_app_catalog)
            page.locator(self.selectors.text_app_catalog).click()

            page.locator(self.selectors.permissions_create_button).click()

            page.locator(self.selectors.next_button).click()

            with page.expect_navigation():
                page.locator(self.selectors.finish_button).click()

            time.sleep(9)

            page.locator(self.selectors.custom_editing).click()

            page.locator(self.selectors.edit_role).click()
            
            page.locator(self.selectors.permissions_edit).click()

            page.locator(self.selectors.add_permissions).click()

            page.locator(self.selectors.listbox_audit_trial).first.click()

            page.locator(self.selectors.group_svg).click()

            page.locator(self.selectors.listbox_notification).first.click()

            page.locator(self.selectors.group_div).nth(1).click()

            page.locator(self.selectors.permissions_create_button).click()

            page.locator(self.selectors.scope_edit_button).click()

            page.locator(self.selectors.role_details_back).click()

            if not page.locator(self.selectors.custom_role1):
                return False

            page.locator(self.selectors.custom_role1).first.click()

            time.sleep(9)

            page.locator(self.selectors.edit_role).click()

            page.locator(self.selectors.actions_button).click()

            page.locator(self.selectors.delete_role).click()

            page.locator(self.selectors.primary_button).click()

            with page.expect_navigation():
                page.locator(self.selectors.primary_button).click()
            page.goto("https://mira.ccs.arubathena.com/manage-account/identity/roles")

            time.sleep(3)

            page.locator(self.selectors.identity_title).click()

            page.locator(self.selectors.card_roles).click()

            page.locator(self.selectors.glcp_header_all_menu).click()

            with page.expect_navigation():
                page.locator(self.selectors.glcp_sign_out).click()
            return True
        except Exception as e:
            log.error("not able to locate the role on the page {}".format(e))
            return False
