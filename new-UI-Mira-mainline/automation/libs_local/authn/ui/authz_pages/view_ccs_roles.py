"""
This file holds functions to view the CCS roles

"""
import logging

log = logging.getLogger(__name__)


class RolesPage:
    def __init__(self, hostname):
        self.hostname = hostname

    def view_roles_page(self, page):
        """
        Views the roles page

        :param page: page instance
        :return: None
        """
        try:
            # Click [data-testid="manage-nav-menu"]
            page.locator("[data-testid=\"manage-nav-menu\"]").click()

            # Click [data-testid="text-identity-title"] >> text=Identity & Access
            page.locator("[data-testid=\"text-identity-title\"] >> text=Identity & Access").click()
            page.wait_for_url(self.hostname + "/manage-account/identity")
            # page.wait_for_url("https://gemini.ccs.arubathena.com/manage-account/identity")

            # Click [data-testid="text-roles-title"]
            page.locator("[data-testid=\"text-roles-title\"]").click()
            page.wait_for_url(self.hostname + "/manage-account/identity/roles")
            # page.wait_for_url("https://gemini.ccs.arubathena.com/manage-account/identity/roles")

            # Click text=Account Administrator >> nth=0
            acct_admin_user = page.locator("text=Account Administrator")
            if "Account Administrator" not in acct_admin_user.all_text_contents():
                return False
            page.locator("text=Account Administrator").first.click()

            # Click button[role="tab"]:has-text("Assigned Users")
            page.locator("button[role=\"tab\"]:has-text(\"Assigned Users\")").click()

            # Click [data-testid="close-button"]
            page.locator("[data-testid=\"close-button\"]").click()

            # Click [data-testid="drop-btn-glcp-header-all-menu-item-user"]
            page.locator("[data-testid=\"drop-btn-glcp-header-all-menu-item-user\"]").click()

            # Click [data-testid="sign-out-hpe-nav-menu"]
            page.locator("[data-testid=\"sign-out-hpe-nav-menu\"]").click()
            page.wait_for_url("https://auth-itg.hpe.com/")
            return True
        except Exception as e:
            log.error("not able to locate the role on the page {}".format(e))
            return False
