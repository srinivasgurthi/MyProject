"""
This file holds functions to view the CCS roles

"""
import logging

log = logging.getLogger(__name__)


class RolesPaths:
    """
    Class holding selectors to view Roles

    """
    manage_menu = 'data-testid=manage-nav-menu'
    identity_and_access = 'data-testid=text-identity-title'
    identity_page = "/manage-account/identity"
    roles = 'data-testid=text-roles-title'
    roles_page = "/manage-account/identity/roles"
    acct_admin = 'text=Account Administrator'
    acct_administrator = "Account Administrator"
    assigned_user = "button[role='tab']:has-text('Assigned Users')"
    close_btn = 'data-testid=close-button'
    drop_btn = 'data-testid=drop-btn-glcp-header-all-menu-item-user'
    sign_out_btn = 'data-testid=sign-out-hpe-nav-menu'
    authn_url = "https://auth-itg.hpe.com/"


class RolesPage:
    """
    Class for defining methods to view roles

    """
    def __init__(self, hostname):
        self.selectors = RolesPaths()
        self.hostname = hostname

    def view_roles_page(self, page):
        """
        Views the roles page

        :param page: page instance
        :return: None
        """
        try:
            page.locator(self.selectors.manage_menu).click()
            page.locator(self.selectors.identity_and_access).click()
            page.wait_for_url(self.hostname + self.selectors.identity_page)
            page.locator(self.selectors.roles).click()
            page.wait_for_url(self.hostname + self.selectors.roles_page)
            page.wait_for_selector(self.selectors.acct_admin)
            acct_admin_user = page.locator(self.selectors.acct_admin)
            if self.selectors.acct_administrator not in acct_admin_user.all_text_contents():
                return False
            page.locator(self.selectors.acct_admin).first.click()
            page.locator(self.selectors.assigned_user).click()
            page.locator(self.selectors.close_btn).click()
            page.locator(self.selectors.drop_btn).click()
            page.locator(self.selectors.sign_out_btn).click()
            page.wait_for_url(self.selectors.authn_url)
            return True
        except Exception as e:
            log.error("not able to locate the role on the page {}".format(e))
            return False
