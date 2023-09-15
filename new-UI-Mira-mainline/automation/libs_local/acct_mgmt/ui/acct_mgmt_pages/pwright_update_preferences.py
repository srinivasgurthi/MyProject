import logging
import random
log = logging.getLogger(__name__)


class AcctUpdatePrefPagePaths:
    user_menu = 'data-testid=drop-btn-glcp-header-all-menu-item-user'
    user_menu_pref = 'data-testid=text-desc-hpe-gl-pref-nav-menu'
    session_timeout = 'data-testid=timeout-number-form-field-input'
    save_changes = 'data-testid=profile-button-submit'


class AcctUpdatePrefPage(object):
    def __init__(self):
        self.selectors = AcctUpdatePrefPagePaths()
        log.info(f"Initialize {__name__}")

    def acct_update_pref_page(self, page):
        try:
            random_number = str(random.randint(20, 30))
            page.click(self.selectors.user_menu)
            page.click(self.selectors.user_menu_pref)
            page.fill(self.selectors.session_timeout, random_number)
            page.click(self.selectors.save_changes)
            return True
        except Exception as e:
            log.error("not able to locate the role on the page {}".format(e))
            return False
