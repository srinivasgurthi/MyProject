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
    Devices Inventory page object model class.
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize Devices Inventory page object.
        :param page: page.
        :param cluster: cluster url.
        """
        log.info("Initialize Devices Inventory page object.")
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

    def add_filter_by_applications(self, applications: list):
        """Add devices table filtering by Applications list.

        :param applications: list of applications labels to be applied in filter.
        :return: current instance of Devices Inventory page object.
        """
        log.info("Playwright: adding devices table filtering by Applications list.")
        self.page.locator(DevicesInventorySelectors.FILTER_BUTTON).click()
        self._select_checkbox_items("Application", applications)
        self.page.locator(DevicesInventorySelectors.APPLY_FILTERS_BTN).click()
        return self

    def add_filter_by_device_types(self, device_types: list):
        """Add devices table filtering by Devices Types list.

        :param device_types: list of devices types labels to be applied in filter.
        :return: current instance of Devices Inventory page object.
        """
        log.info("Playwright: adding devices table filtering by Devices Types list.")
        self.page.locator(DevicesInventorySelectors.FILTER_BUTTON).click()
        self._select_checkbox_items("Device Type", device_types)
        self.page.locator(DevicesInventorySelectors.APPLY_FILTERS_BTN).click()
        return self

    def add_filter_by_subscription_tiers(self, tiers: list):
        """Add devices table filtering by Subscription Tiers list.

        :param tiers: list of subscription tiers labels to be applied in filter.
        :return: current instance of Devices Inventory page object.
        """
        log.info("Playwright: adding devices table filtering by Subscription Tiers list.")
        self.page.locator(DevicesInventorySelectors.FILTER_BUTTON).click()
        self._select_checkbox_items("Subscription Tier", tiers)
        self.page.locator(DevicesInventorySelectors.APPLY_FILTERS_BTN).click()
        return self

    def clear_filter(self):
        """Clear Devices Inventory filter.

        :return: current instance of Devices Inventory page object.
        """
        log.info(f"Playwright: clear value in search field of audit logs.")
        self.page.locator(DevicesInventorySelectors.CLEAR_FILTERS_BUTTON).click()
        return self

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

    def should_all_rows_have_text_in_column(self, column_name, allowed_values):
        """Check that current table page has only rows with values at 'column_name' column,
        which are present in specified 'allowed_values' list.

        :param column_name: column name where matching text should be looked at.
        :param allowed_values: list of allowed expected values in specified column.
        :return: current instance of Devices Inventory page object.
        """
        log.info(
            f"Playwright: check all rows at current table page have only allowed values in '{column_name}' column.")
        matching_rows_indices = set()
        for value in allowed_values:
            matching_indices = self.table_utils.get_rows_indices_by_text_in_column(column_name, value)
            matching_rows_indices.update(set(matching_indices))
        if not matching_rows_indices:
            raise ValueError(f"Not found rows with any of '{allowed_values}' values at '{column_name}' column.")
        expect(self.page.locator(
            DevicesInventorySelectors.TABLE_ROW_TEMPLATE.format(list(matching_rows_indices)[0]))).to_be_visible()
        rows_count = self.page.locator(DevicesInventorySelectors.TABLE_ROWS).count()
        expected_matching_rows_indices = set(range(1, rows_count + 1))
        assert expected_matching_rows_indices == matching_rows_indices, \
            f"Some table rows have unexpected value(s) at '{column_name}' column. " \
            f"Mismatched rows indexes: '{sorted(expected_matching_rows_indices ^ matching_rows_indices)}'."
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

    def _select_checkbox_items(self, field_label, item_labels):
        """Select all checkboxes with text, listed in 'item_labels' list and located at field labeled as 'field_label'.

        :param field_label: text label of the field, whose checkbox-items have to be checked.
        :param item_labels: list of checkbox-items (list of text labels), to be selected.
        """
        selector_qualifiers = {"field_label": field_label}
        for item in item_labels:
            selector_qualifiers.update({"item_label": item})
            item_locator = \
                self.page.locator(DevicesInventorySelectors.FILTER_ITEM_TEMPLATE.format(**selector_qualifiers))
            if item_locator.locator("svg[viewBox]").is_hidden():
                item_locator.click()
            else:
                log.warning(f"Filter checkbox '{item}' at '{field_label}' field was set already.")
