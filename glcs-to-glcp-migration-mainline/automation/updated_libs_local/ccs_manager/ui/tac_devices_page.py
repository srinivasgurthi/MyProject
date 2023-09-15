"""
TAC Devices page object model.
"""
import logging
from typing import List

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.ccs_manager.ui.locators import TacDevicesSelectors
from hpe_glcp_automation_lib.libs.ccs_manager.ui.tac_device_details_page import TacDeviceDetailsPage
from hpe_glcp_automation_lib.libs.ccs_manager.ui.tac_menu_navigable_page import TacMenuNavigablePage
from hpe_glcp_automation_lib.libs.commons.ui.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import TableUtils

log = logging.getLogger(__name__)


class TacDevicesPage(HeaderedPage, TacMenuNavigablePage):
    """
    TAC Devices page object model class.
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize TAC Devices page object.
        :param page: page.
        :param cluster: cluster url.
        """
        log.info("Initialize TAC Devices page object.")
        super().__init__(page, cluster)
        self.table_utils = TableUtils(page)
        self.url = f"{cluster}/manage-ccs/devices"

    def wait_for_loaded_table(self):
        """
        Wait for table rows are not empty and loader spinner is not present on the page.
        :return: current instance of TAC Devices page object.
        """
        log.info("Playwright: wait for table is loaded.")
        self.wait_for_loaded_state()
        self.page.wait_for_selector(TacDevicesSelectors.TABLE_ROWS, state="visible", strict=False)
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def search_for_text(self, search_text):
        """Enter text to search field.

        :param search_text: search_text.
        :return: current instance of TAC Devices page object.
        """
        log.info(f"Playwright: search for text: '{search_text}' at TAC Devices.")
        self.pw_utils.enter_text_into_element(TacDevicesSelectors.SEARCH_FIELD, search_text)
        self.wait_for_loaded_table()
        return self

    def move_devices_to_customer_folder(self, devices_ids_list: List, pcid, folder_name, expect_failure=False):
        """Move list of devices to the folder of customer with specified pcid.

        :param devices_ids_list: list of devices serials or mac-addresses.
        :param pcid: pcid of target customer.
        :param folder_name: target folder name.
        :param expect_failure: is failure (True) or success (False) of devices moving expected.
        :return: current instance of TAC Devices page object.
        """
        log.info(f"Playwright: move devices to '{folder_name}' folder of pcid '{pcid}'.")
        self.page.locator(TacDevicesSelectors.MOVE_DEVICE_BTN).click()
        devices_ids_text = ",".join(devices_ids_list)
        self.page.locator(TacDevicesSelectors.SERIALS_OR_MACS_FIELD).fill(devices_ids_text)
        self.page.locator(TacDevicesSelectors.PCID_INPUT_FIELD).fill(pcid)
        self.page.locator(TacDevicesSelectors.CUST_ID_SEARCH_BTN).click()
        self.pw_utils.select_drop_down_element(drop_menu_selector=TacDevicesSelectors.FOLDER_SELECT_DROPDOWN,
                                               element=folder_name,
                                               element_role="option",
                                               exact_match=True)
        self.page.locator(TacDevicesSelectors.MOVE_DEVICES_ACTION_BTN).click()
        if expect_failure:
            self.page.locator(TacDevicesSelectors.ERROR_MESSAGE_AREA).wait_for()
        else:
            self.page.locator(TacDevicesSelectors.MOVED_DEVICES_POPUP_TITLE).wait_for()
            self.page.locator(TacDevicesSelectors.CLOSE_BTN).click()
        return self

    def close_move_devices_dialog(self):
        """Close Move Devices dialog.

        :return: current instance of TAC Devices page object.
        """
        log.info(f"Playwright: close Move Devices popup dialog.")
        self.page.locator(TacDevicesSelectors.CANCEL_BTN).click()
        return self

    def open_device_details_page(self, column_name, value):
        """Click at row, containing expected text in specified column.

        :param column_name: column name where matching text should be looked at.
        :param value: text to be matched.
        :return: instance of Folder Details page object.
        """
        log.info(f"Playwright: click row with text '{value}' in column '{column_name}'.")
        self.wait_for_loaded_table()
        matching_rows_indices = self.table_utils.get_rows_indices_by_text_in_column(column_name, value)
        if not matching_rows_indices:
            raise ValueError(f"Not found rows with '{value}' value at '{column_name}' column.")
        if column_name == "Serial Number":
            serial_number = value
        else:
            sn_column_index = self.pw_utils.get_column_index_by_name("Serial Number")
            sn_column_selector = \
                TacDevicesSelectors.TABLE_ROW_COLUMN_TEMPLATE.format(matching_rows_indices[0], sn_column_index)
            serial_number = self.page.locator(sn_column_selector).text_content()
        self.page.locator(TacDevicesSelectors.TABLE_ROW_TEMPLATE.format(matching_rows_indices[0])).click()
        return TacDeviceDetailsPage(self.page, self.cluster, serial_number)

    def should_have_row_with_values_in_columns(self, column_to_text_dict):
        """Check that table has row with expected text-values in corresponding specified columns.

        :param column_to_text_dict: dictionary with key-value pairs, where 'key' is column name and 'value'
            is text to be in that column.
        :return: current instance of TAC Devices page object.
        """
        log.info(f"Playwright: check that row with expected text values in related columns is present in table.")
        matching_rows_indices = self.table_utils.get_rows_indices_by_values_in_columns(column_to_text_dict)
        if not matching_rows_indices:
            raise ValueError(f"Not found rows with expected text values at related columns.")
        self.pw_utils.save_screenshot(self.test_name)
        expect(self.page.locator(
            TacDevicesSelectors.TABLE_ROW_TEMPLATE.format(matching_rows_indices[0]))).to_be_visible()
        return self

    def should_have_error_containing_text(self, error_text):
        """Check that expected error message appeared at "Move Devices" dialog.

        :param error_text: expected error text at "Move Devices" dialog.
        :return: current instance of TAC Devices page object.
        """
        log.info(f"Playwright: check for appeared error containing text '{error_text}'.")
        expect(self.page.locator(TacDevicesSelectors.ERROR_MESSAGE_AREA)).to_contain_text(error_text)
        return self
