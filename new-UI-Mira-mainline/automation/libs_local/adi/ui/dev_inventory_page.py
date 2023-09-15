"""
Devices Inventory page object model.
"""
import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.adi.ui.add_devices_page import AddDevices
from hpe_glcp_automation_lib.libs.adi.ui.locators import DevicesInventorySelectors
from hpe_glcp_automation_lib.libs.commons.ui.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import TableUtils

log = logging.getLogger(__name__)


class DevicesInventory(HeaderedPage):
    """
    Homepage page object model class.
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize Devices Inventory page object.
        :param page: page.
        :param cluster: cluster url.
        """
        log.info("Initialize Devices Inventory page object")
        super().__init__(page, cluster)
        self.table_utils = TableUtils(page)
        self.url = f"{cluster}/devices/inventory"

    def wait_for_loaded_table(self):
        """
        Wait for table rows are not empty and loader spinner is not present on the page.
        :return: current instance of Devices Inventory page object.
        """
        log.info("Playwright: wait for table is loaded.")
        self.wait_for_loaded_state()
        self.page.wait_for_selector(DevicesInventorySelectors.TABLE_ROWS, state="visible", strict=False)
        self.page.locator(DevicesInventorySelectors.LOADER_SPINNER).wait_for(state="hidden")
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def search_for_text(self, search_text):
        """
        Enter text to search field.
        :param search_text: search_text.
        :return: current instance of Devices Inventory page object.
        """
        log.info(f"Playwright: search for text: '{search_text}' at devices inventory.")
        self.pw_utils.enter_text_into_element(DevicesInventorySelectors.SEARCH_FIELD, search_text)
        self.wait_for_loaded_table()
        return self

    def click_add_devices(self):
        """Open add devices page.

        :return: instance of AddDevices page object.
        """
        log.info("Playwright: click 'Add Devices' button.")
        (self.page.locator(DevicesInventorySelectors.ADD_DEVICE_BUTTON)).click()
        return AddDevices(self.page, self.cluster)

    def should_have_search_field(self):
        """Check that search field with correct placeholder is present on the page.

        :return: current instance of Devices Inventory page object.
        """
        log.info(f"Playwright: check search field is present at devices inventory.")
        search_field_locator = self.page.locator(DevicesInventorySelectors.SEARCH_FIELD)
        self.pw_utils.save_screenshot(self.test_name)
        expect(search_field_locator).to_be_visible()
        expect(search_field_locator).to_have_attribute("placeholder", "Search by Serial, Model, or MAC Address")
        return self

    def should_have_row_with_text_in_column(self, column_name, value):
        """Check that row with matched text in specified column is present and visible in table.

        :param column_name: column name where matching text should be looked at.
        :param value: text to be matched.
        :return: current instance of Devices Inventory page object.
        """
        log.info(f"Playwright: check that row with text '{value}' in column '{column_name}' is present in table.")
        matching_rows_indices = self.table_utils.get_rows_indices_by_text_in_column(column_name, value)
        if not matching_rows_indices:
            raise ValueError(f"Not found rows with '{value}' value at '{column_name}' column.")
        expect(self.page.locator(
            DevicesInventorySelectors.TABLE_ROW_TEMPLATE.format(matching_rows_indices[0]))).to_be_visible()
        return self

    def should_have_row_with_values_in_columns(self, column_to_text_dict):
        """Check that table has row with expected text-values in corresponding specified columns.

        :param column_to_text_dict: dictionary with key-value pairs, where 'key' is column name and 'value' is text to be in that column.
        :return: current instance of Devices Inventory page object.
        """
        log.info(f"Playwright: check that row with expected text values in related columns is present in table.")
        matching_rows_indices = self.table_utils.get_rows_indices_by_values_in_columns(column_to_text_dict)
        if not matching_rows_indices:
            raise ValueError(f"Not found rows with expected text values at related columns.")
        expect(self.page.locator(
            DevicesInventorySelectors.TABLE_ROW_TEMPLATE.format(matching_rows_indices[0]))).to_be_visible()
        return self

    def should_have_rows_count(self, count):
        """Check that displayed rows count in table is matched to expected.

        :param count: expected count of rows.
        :return: current instance of Devices Inventory page object.
        """
        log.info("Playwright: wait for expected rows count in table.")
        expect(self.page.locator(DevicesInventorySelectors.TABLE_ROWS)).to_have_count(count)
        self.page.wait_for_load_state("domcontentloaded")
        return self
