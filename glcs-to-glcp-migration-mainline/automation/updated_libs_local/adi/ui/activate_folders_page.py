"""
Activate Folders page object model.
"""
import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.adi.ui.activate_folder_details_page import ActivateFolderDetails
from hpe_glcp_automation_lib.libs.adi.ui.locators import ActivateFoldersSelectors
from hpe_glcp_automation_lib.libs.commons.ui.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import TableUtils
from hpe_glcp_automation_lib.libs.adi.ui.side_menu_navigable_page import SideMenuNavigablePage

log = logging.getLogger(__name__)


class ActivateFolders(HeaderedPage, SideMenuNavigablePage):
    """
    Activate Folders page object model class.
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize Activate Folders page object.
        :param page: page.
        :param cluster: cluster url.
        """
        log.info("Initialize Activate Folders page object")
        super().__init__(page, cluster)
        self.table_utils = TableUtils(page)
        self.url = f"{cluster}/manage-account/activate/folders"

    def wait_for_loaded_table(self):
        """Wait for table rows are not empty and loader spinner is not present on the page.

        :return: current instance of Activate Folders page object.
        """
        log.info("Playwright: wait for table is loaded.")
        self.wait_for_loaded_state()
        self.page.wait_for_selector(ActivateFoldersSelectors.TABLE_ROWS, state="visible", strict=False)
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def search_for_text(self, search_text, ensure_not_empty=True):
        """Enter text to search field.

        :param search_text: search_text.
        :param ensure_not_empty: defines either it's required to wait for non-empty table or not.
        :return: current instance of Activate Folders page object.
        """
        log.info(f"Playwright: search for text: '{search_text}' at folders page.")
        self.pw_utils.enter_text_into_element(ActivateFoldersSelectors.SEARCH_FIELD, search_text)
        if ensure_not_empty:
            self.wait_for_loaded_table()
        else:
            self.wait_for_loaded_state()
        return self

    def create_new_folder(self, folder_name, parent_folder="default", description=""):
        """Create new folder with specified name and parent.

        :param folder_name: name of the folder to create.
        :param parent_folder: parent folder's name.
        :param description: text value for description field of new folder.
        :return: current instance of Activate Folders page object.
        """
        log.info(f"Playwright: Create new folder '{folder_name}'.")
        self.page.locator(ActivateFoldersSelectors.CREATE_FOLDER_BTN).click()
        self.page.locator(ActivateFoldersSelectors.FOLDER_NAME_INPUT).fill(folder_name)
        self.pw_utils.select_drop_down_element(ActivateFoldersSelectors.PARENT_NAME_DROPDOWN, parent_folder, "option")
        self.page.locator(ActivateFoldersSelectors.DESCRIPTION_INPUT).fill(description)
        self.page.locator(ActivateFoldersSelectors.POPUP_CREATE_BTN).click()
        return self

    def open_folder_details(self, folder_name):
        """
        Open details page for particular folder

        :param folder_name: Name of the folder
        :return: current instance of Activate Folder Details page object.
        """
        self.search_for_text(folder_name)
        self.page.locator(ActivateFoldersSelectors.TABLE_ROWS).first.click()
        return ActivateFolderDetails(self.page, self.cluster)

    def should_have_row_with_text_in_column(self, column_name, value):
        """Check that row with matched text in specified column is present and visible in table.

        :param column_name: column name where matching text should be looked at.
        :param value: text to be matched.
        :return: current instance of Activate Folders page object.
        """
        log.info(f"Playwright: check that row with text '{value}' in column '{column_name}' is present in table.")
        matching_rows_indices = self.table_utils.get_rows_indices_by_text_in_column(column_name, value)
        if not matching_rows_indices:
            raise ValueError(f"Not found rows with '{value}' value at '{column_name}' column.")
        self.pw_utils.save_screenshot(self.test_name)
        expect(self.page.locator(
            ActivateFoldersSelectors.TABLE_ROW_TEMPLATE.format(matching_rows_indices[0]))).to_be_visible()
        return self

    def should_have_row_with_values_in_columns(self, column_to_text_dict):
        """Check that table has row with expected text-values in corresponding specified columns.

        :param column_to_text_dict: dictionary with key-value pairs, where 'key' is column name and 'value' is text
        to be in that column.
        :return: current instance of Activate Folders page object.
        """
        log.info("Playwright: check that row with expected text values in related columns is present in table.")
        matching_rows_indices = self.table_utils.get_rows_indices_by_values_in_columns(column_to_text_dict)
        if not matching_rows_indices:
            raise ValueError(f"Not found rows with expected text values at related columns.")
        self.pw_utils.save_screenshot(self.test_name)
        expect(self.page.locator(
            ActivateFoldersSelectors.TABLE_ROW_TEMPLATE.format(matching_rows_indices[0]))).to_be_visible()
        return self

    def should_have_rows_count(self, count):
        """Check that displayed rows count in table is matched to expected.

        :param count: expected count of rows.
        :return: current instance of Activate Folders page object.
        """
        log.info("Playwright: wait for expected rows count in table.")
        self.pw_utils.save_screenshot(self.test_name)
        expect(self.page.locator(ActivateFoldersSelectors.TABLE_ROWS)).to_have_count(count)
        self.page.wait_for_load_state("domcontentloaded")
        return self

    # TODO: Refactor for not taking unused arguments (or remove since it just wraps existing 'should_have_rows_count()')
    def should_not_have_folder_in_the_table(self, folder_name):
        """Check that folder is not in the table. Empty table expected.

        :param folder_name: folders' name.
        :return: current instance of Activate Folders page object.
        """
        log.info("Playwright: check that folder is not in the table.")
        self.should_have_rows_count(0)
        return self
