"""
Roles page object model.
"""
import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.authz.ui.locators import RolesSelectors
from hpe_glcp_automation_lib.libs.commons.ui.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import TableUtils

log = logging.getLogger(__name__)


class Roles(HeaderedPage):
    """
    Roles page object model class.
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize Roles page object.
        :param page: page.
        :param cluster: cluster url.
        """
        log.info("Initialize Roles page object")
        super().__init__(page, cluster)
        self.table_utils = TableUtils(page)
        self.url = f"{cluster}/manage-account/identity/roles"

    def wait_for_loaded_table(self):
        """
        Wait for table rows are not empty and loader spinner is not present on the page.
        :return: current instance of roles page object.
        """
        log.info("Playwright: wait for table is loaded.")
        self.wait_for_loaded_state()
        self.page.wait_for_selector(RolesSelectors.TABLE_ROWS, state="visible", strict=False)
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def search_for_text(self, search_text):
        """
        Enter text to search field.
        :param search_text: search_text.
        :return: current instance of roles page object.
        """
        log.info(f"Playwright: search for text: '{search_text}' in roles.")
        self.pw_utils.enter_text_into_element(RolesSelectors.SEARCH_FIELD, search_text)
        self.wait_for_loaded_table()
        return self

    def navigate_to_identity_and_access(self):
        """
        Return to the previous page.
        """
        log.info(f"Playwright: navigate back to identity and access page from roles.")
        self.page.locator(RolesSelectors.BACK_BUTTON).click()
        # Note: page object cannot be returned when navigating to the previous pages due to the circular import

    def should_have_search_field(self):
        """
        Check that search field with expected placeholder is present on the page.
        :return: current instance of roles page object.
        """
        log.info(f"Playwright: check search field is present at roles.")
        search_field_locator = self.page.locator(RolesSelectors.SEARCH_FIELD)
        self.pw_utils.save_screenshot(self.test_name)
        expect(search_field_locator).to_be_visible()
        expect(search_field_locator).to_have_attribute("placeholder", "Search roles")
        return self

    def should_contain_text_in_table(self, text):
        """
        Check table has row containing expected text.
        :param text: the text to be displayed in table.
        :return: current instance of roles page object.
        """
        log.info(f"Playwright: check that row with text '{text}' is present in table.")
        self.pw_utils.save_screenshot(self.test_name)
        expect(self.page.locator(RolesSelectors.TABLE_ROWS, has_text=text).first).to_be_visible()
        return self

    def should_have_row_with_text_in_column(self, column_name, value):
        """Check that row with matched text in specified column is present and visible in table.

        :param column_name: column name where matching text should be looked at.
        :param value: text to be matched.
        :return: current instance of roles page object.
        """
        log.info(f"Playwright: check that row with text '{value}' in column '{column_name}' is present in table.")
        matching_rows_indices = self.table_utils.get_rows_indices_by_text_in_column(column_name, value)
        if not matching_rows_indices:
            raise ValueError(f"Not found rows with '{value}' value at '{column_name}' column.")
        expect(self.page.locator(RolesSelectors.TABLE_ROW_TEMPLATE.format(matching_rows_indices[0]))).to_be_visible()
        return self

    def should_have_rows_count(self, count):
        """Check that displayed rows count in table is matched to expected.

        :param count: expected count of rows.
        :return: current instance of roles page object.
        """
        log.info("Playwright: wait for expected rows count in table.")
        expect(self.page.locator(RolesSelectors.TABLE_ROWS)).to_have_count(count)
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def should_contain_text_in_title(self, text):
        """
        Check that expected text is present as part of the heading page title.
        :param text: expected text to be contained in title.
        :return: current instance of roles page object.
        """
        log.info(f"Playwright: check that title contains text '{text}' in roles page.")
        self.pw_utils.save_screenshot(self.test_name)
        expect(self.page.locator(RolesSelectors.HEADING_PAGE_TITLE)).to_contain_text(text)
        return self

    def should_have_text_in_title(self, text):
        """
        Check that expected text matches with the heading page title.
        :param text: expected text to match with the text in title.
        :return: current instance of My Applications page object.
        """
        log.info(f"Playwright: check that title has matched text '{text}' in roles page.")
        self.pw_utils.save_screenshot(self.test_name)
        expect(self.page.locator(RolesSelectors.HEADING_PAGE_TITLE)).to_have_text(text)
        return self
