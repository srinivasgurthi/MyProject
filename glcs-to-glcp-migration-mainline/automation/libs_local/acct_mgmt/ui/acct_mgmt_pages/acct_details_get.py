"""
This file holds functions to collect account details

"""
import logging
log = logging.getLogger(__name__)


class AcctDetailsGetPaths:
    """
    Class for Account Details locators

    """
    manage_menu = 'data-testid=manage-nav-menu'
    user_menu = 'data-testid=drop-btn-glcp-header-all-menu-item-user'
    user_menu_pref = 'data-testid=text-desc-hpe-gl-pref-nav-menu'
    session_timeout = 'data-testid=timeout-number-form-field-input'
    save_changes = 'data-testid=profile-button-submit'


class AcctDetailsGetPage:
    """
    Class for collecting account details
    """
    def __init__(self):
        self.selectors = AcctDetailsGetPaths()
        log.info(f"Initialize {__name__}")

    def acct_update_pref_page(self, page, acct_name):
        """
        Fetches the account details page

        :param page: page instance
        :param acct_name: account name
        """
        try:
            page.locator("data-testid=manage-nav-menu").click()
            # Click [data-testid="card-account_details"] div:has-text("Acco
            # unt DetailsEdit your account's general information.") >> nth=0
            page.locator("[data-testid=\"card-account_details\"] div:has-text"
                         "(\"Account DetailsEdit your account's general "
                         "information.\")").first.click()

            # expect(page).to_have_url(
            # "https://mira.ccs.arubathena.com/manage-account/account-details")
            if not page.wait_for_selector(f'text={acct_name}'):
                return False
            else:
                return True
        except Exception as e:
            log.error("not able to locate the role on the page {}".format(e))
            return False
