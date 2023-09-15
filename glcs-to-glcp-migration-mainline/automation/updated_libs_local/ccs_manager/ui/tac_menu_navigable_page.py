import logging

from playwright.sync_api import Page

from hpe_glcp_automation_lib.libs.ccs_manager.ui.elem_tac_side_menu import TacSideMenu
from hpe_glcp_automation_lib.libs.ccs_manager.ui.locators import TacSideMenuSelectors
from hpe_glcp_automation_lib.libs.commons.ui.base_page import BasePage

log = logging.getLogger(__name__)


class TacMenuNavigablePage(BasePage):
    """
    TAC Side Menu Navigable page object model class.
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize TAC Side Menu Navigable page object.
        :param page: page.
        :param cluster: cluster url.
        """
        log.info("Initialize TAC Side Menu Navigable page object.")
        super().__init__(page, cluster)
        self.side_menu = TacSideMenu(page)

    # TODO: Remove this method when related tests are refactored.
    def click_menu_link(self, menu_item_text):
        """DEPRECATED! CONSIDER USING OF METHODS UNDER 'TacMenuNavigablePage().side_menu' ATTRIBUTE INSTEAD.
        Click at menu item with specified text.

        :param menu_item_text: text of menu item to click.
        """
        log.warning(f"THIS METHOD IS DEPRECATED AND GOING TO BE REMOVED SOON."
                    f"CONSIDER USING OF METHODS UNDER 'TacMenuNavigablePage().side_menu' ATTRIBUTE INSTEAD.")
        log.info(f"Playwright: navigate to page by menu link with text '{menu_item_text}'.")
        self.page.locator(TacSideMenuSelectors.MENU_LINK_TEMPLATE.format(menu_item_text)).click()
