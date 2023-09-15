"""
Activate Devices page object model.
"""
import logging
import time
from pathlib import Path

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.adi.ui.activate_folders_page import ActivateFolders
from hpe_glcp_automation_lib.libs.adi.ui.device_history_page import DeviceHistory
from hpe_glcp_automation_lib.libs.adi.ui.locators import ActivateDevicesSelectors
from hpe_glcp_automation_lib.libs.commons.ui.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import TableUtils
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import PwrightUtils
from hpe_glcp_automation_lib.libs.adi.ui.side_menu_navigable_page import SideMenuNavigablePage

log = logging.getLogger(__name__)


class ActivateDevices(HeaderedPage, SideMenuNavigablePage):
    """
    Activate Devices page object model class.
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize Activate Devices page object.
        :param page: page.
        :param cluster: cluster url.
        """
        log.info("Initialize Activate Devices page object")
        super().__init__(page, cluster)
        self.page = page
        self.table_utils = TableUtils(page)
        self.pw_utils = PwrightUtils(page)
        self.url = f"{cluster}/manage-account/activate/devices"

    def wait_for_loaded_table(self):
        """
        Wait for table rows are not empty and loader spinner is not present on the page.
        :return: current instance of Activate Devices page object.
        """
        log.info("Playwright: wait for table is loaded.")
        self.wait_for_loaded_state()
        self.page.wait_for_selector(ActivateDevicesSelectors.TABLE_ROWS, state="visible", strict=False)
        self.page.locator(ActivateDevicesSelectors.LOADER_SPINNER).wait_for(state="hidden")
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def open_device_history(self, device_identifier, column_name="Serial Number"):
        """Open device history for particular device from the table.

        :param device_identifier: Device info to search for (e.g. serial number, mac etc.)
        :param column_name: Name of column, where search_info will be shown. By default, its serial number
        :return: instance of Device History page object.
        """
        log.info("Playwright: Open device history page with particular data given")
        self.wait_for_loaded_table()
        self.page.locator(ActivateDevicesSelectors.SEARCH_FIELD).fill(device_identifier)
        self.wait_for_loaded_table()
        matching_row_index = self.table_utils.get_rows_indices_by_text_in_column(column_name, device_identifier)
        self.page.locator(ActivateDevicesSelectors.TABLE_ROW_TEMPLATE.format(matching_row_index[0])).click()
        return DeviceHistory(self.page, self.cluster, device_identifier)

    def download_allowed_list_cli(self):
        """
        Download Allowed List CLI for all workspace activate devices
        @return: Name of the downloaded file
        """
        name = "Allowed List CLI"
        return self._download_csv_for_all_devices(item_name=name)

    def download_legacy_allowed_list_cli(self):
        """
        Download Legacy Allowed List CLI for all workspace activate devices
        @return: Name of the downloaded file
        """
        name = "Legacy Allowed List CLI"
        return self._download_csv_for_all_devices(item_name=name)

    def download_inventory_csv(self):
        """
        Download Inventory CSV for all workspace activate devices
        @return: Name of the downloaded file
        """
        name = "Inventory CSV"
        return self._download_csv_for_all_devices(item_name=name)

    def download_allowed_list_csv(self):
        """
        Download Allowed List CSV for all workspace activate devices
        @return: Name of the downloaded file
        """
        name = "Allowed List CSV"
        return self._download_csv_for_all_devices(item_name=name)

    def get_devices_count(self):
        """
        Get the number of devices currently listed in the table on Activate Devices page
        :return: Integer number
        """
        return int(self.page.locator(ActivateDevicesSelectors.TABLE_SUMMARY_COUNT).text_content())

    def search_for_text(self, search_text):
        """
        Enter text to search field.
        :param search_text: search_text.
        :return: current instance of Activate Devices page object.
        """
        log.info(f"Playwright: search for text: '{search_text}' at devices inventory.")
        self.pw_utils.enter_text_into_element(ActivateDevicesSelectors.SEARCH_FIELD, search_text)
        self.wait_for_loaded_table()
        return self

    def navigate_to_folders(self):
        """Open Activate Folders page.

        :return: instance of Activate Folders page object.
        """
        log.info("Playwright: Navigate to Activate Folders page.")
        self.page.locator(ActivateDevicesSelectors.FOLDERS_TAB_BUTTON).click()
        return ActivateFolders(self.page, self.cluster)

    def move_device_to_another_folder(self, folder_name):
        """ Move the device to another folder
        :param: folder name
        :return: current instance of Activate Device Details page object.
        """
        log.info("Playwright: Move device to another folder")
        self.pw_utils.click_selector(ActivateDevicesSelectors.ACTIONS_BUTTON)
        self.pw_utils.click_selector(ActivateDevicesSelectors.MOVE_TO_FOLDER_BUTTON)
        self.pw_utils.click_selector(ActivateDevicesSelectors.MOVE_TO_FOLDER_DD)
        self.pw_utils.enter_text_into_element(ActivateDevicesSelectors.SEARCH_TEXT_BOX, folder_name)
        self.pw_utils.click_selector(ActivateDevicesSelectors.SELECT_OPTION)
        self.pw_utils.click_selector(ActivateDevicesSelectors.MOVE_TO_FOLDER_ACTION_BTN)
        self.pw_utils.click_selector(ActivateDevicesSelectors.MOVE_TO_FOLDER_CONFIRM_BTN)
        return self

    def activate_device_token_generation(self):
        """Generate the new token for activate devices.
        :param: None
        :return: current instance of Activate Devices page object.
        """
        log.info("Playwright: Activate Devices page actions - Generate new token")
        self.pw_utils.click_selector(ActivateDevicesSelectors.ACTIONS_DROPDOWN)
        self.pw_utils.click_selector(ActivateDevicesSelectors.GENERATE_TOKEN_BTN)
        self.pw_utils.click_selector(ActivateDevicesSelectors.GENERATE_TOKEN_CREATE_BTN)
        return self

    def select_all_device_type_filter(self, device_type):
        """ Select All device type filter
        :param: device type
        :return: current instance of Activate Devices page object.
        """
        log.info("Playwright: Select all device type filter")
        self.pw_utils.click_selector(ActivateDevicesSelectors.DEVICE_TYPE_FILTER)
        self.pw_utils.enter_text_into_element(ActivateDevicesSelectors.SEARCH_TEXT_BOX, device_type)
        self.pw_utils.click_selector(ActivateDevicesSelectors.SELECT_OPTION)
        return self

    def select_all_model_type_filter(self, model_name):
        """ Select All Models type filter
        :param: model name of the device
        :return: current instance of Activate Devices page object.
        """
        log.info("Playwright: Select all model type filter")
        self.pw_utils.click_selector(ActivateDevicesSelectors.MODELS_FILTER)
        self.pw_utils.enter_text_into_element(ActivateDevicesSelectors.SEARCH_TEXT_BOX, model_name)
        self.pw_utils.click_selector(ActivateDevicesSelectors.SELECT_OPTION)
        return self

    def select_all_folders_filter(self, folder_name):
        """ Select All Folders type filter
        :param: folder name
        :return: current instance of Activate Devices page object.
        """
        log.info("Playwright: Select all folders filter")
        self.pw_utils.click_selector(ActivateDevicesSelectors.FOLDER_NAME_FILTER)
        self.pw_utils.enter_text_into_element(ActivateDevicesSelectors.SEARCH_TEXT_BOX, folder_name)
        self.pw_utils.click_selector(ActivateDevicesSelectors.SELECT_OPTION)
        return self

    def clear_filter_option(self):
        """ Click on Clear Filter option
        :param: None
        :return: current instance of Activate Devices page object.
        """
        log.info("Playwright: Clicking on clear filter option")
        self.pw_utils.click_selector(ActivateDevicesSelectors.CLEAR_FILTER)
        return self

    def should_have_search_field(self, placeholder="Search by Serial, MAC, or Device Name"):
        """
        Check that search field with correct placeholder is present on the page.
        :return: current instance of Activate Devices page object.
        """
        log.info(f"Playwright: check search field is present at devices inventory.")
        search_field_locator = self.page.locator(ActivateDevicesSelectors.SEARCH_FIELD)
        self.pw_utils.save_screenshot(self.test_name)
        expect(search_field_locator).to_be_visible()
        expect(search_field_locator).to_have_attribute("placeholder", placeholder)
        return self

    def should_have_row_with_text_in_column(self, column_name, value):
        """Check that row with matched text in specified column is present and visible in table.

        :param column_name: column name where matching text should be looked at.
        :param value: text to be matched.
        :return: current instance of Activate Devices page object.
        """
        log.info(f"Playwright: check that row with text '{value}' in column '{column_name}' is present in table.")
        matching_rows_indices = self.table_utils.get_rows_indices_by_text_in_column(column_name, value)
        if not matching_rows_indices:
            raise ValueError(f"Not found rows with '{value}' value at '{column_name}' column.")
        expect(self.page.locator(
            ActivateDevicesSelectors.TABLE_ROW_TEMPLATE.format(matching_rows_indices[0]))).to_be_visible()
        return self

    def should_have_row_with_values_in_columns(self, column_to_text_dict):
        """Check that table has row with expected text-values in corresponding specified columns.

        :param column_to_text_dict: dictionary with key-value pairs, where 'key' is column name and 'value' is text
        to be in that column.
        :return: current instance of Activate Devices page object.
        """
        log.info(f"Playwright: check that row with expected text values in related columns is present in table.")
        matching_rows_indices = self.table_utils.get_rows_indices_by_values_in_columns(column_to_text_dict)
        if not matching_rows_indices:
            raise ValueError(f"Not found rows with expected text values at related columns.")
        expect(self.page.locator(
            ActivateDevicesSelectors.TABLE_ROW_TEMPLATE.format(matching_rows_indices[0]))).to_be_visible()
        return self

    def should_have_rows_count(self, count):
        """Check that displayed rows count in table is matched to expected.

        :param count: expected count of rows.
        :return: current instance of Activate Devices page object.
        """
        log.info("Playwright: wait for expected rows count in table.")
        expect(self.page.locator(ActivateDevicesSelectors.TABLE_ROWS)).to_have_count(count)
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def should_have_device_token_success_notification(self, text):
        """Validate the activate device token success text message
        :param: text message to be validated
        :return: current instance of Activate Devices page object.
        """
        log.info("Playwright: Validate the activate device token success notification")
        self.page.wait_for_load_state("domcontentloaded")
        expect(self.page.locator(ActivateDevicesSelectors.GENERATE_TOKEN_SUCCESS_NOTIFICATION)).to_have_text(text)
        return self

    def _download_csv_for_all_devices(self, item_name=""):
        """
        Download CSV for activated devices
        @type item_name: Export list Item name
        @return: downloaded file name
        """
        log.info(f"Playwright: Download {item_name} for activated devices")
        with self.page.expect_download() as download_info:
            self.page.locator(ActivateDevicesSelectors.DEVICES_ACTION_BTN).click()
            self.page.locator(ActivateDevicesSelectors.EXPORT_ALL_DEVICES_BTN).click()
            self.page.get_by_text(item_name).check()
            self.page.locator(ActivateDevicesSelectors.EXPORT_POPUP_BTN).click()
            start = time.time()
        download = download_info.value
        downloading_time = time.time() - start
        log.info(f"Playwright: Download of the {item_name} takes {round(downloading_time, 4)} seconds")
        download.save_as(Path(download.suggested_filename).resolve())
        self.page.locator(ActivateDevicesSelectors.POPUP_CANCEL_BTN).click()
        return download.suggested_filename
