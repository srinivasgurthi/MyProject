"""
Activate Device Details page object model.
"""
import logging
import time
from pathlib import Path

from playwright.sync_api import Page, expect


from hpe_glcp_automation_lib.libs.adi.ui.locators import ActivateDeviceDetailsSelectors
from hpe_glcp_automation_lib.libs.commons.ui.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import TableUtils
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import PwrightUtils


log = logging.getLogger(__name__)


class ActivateDeviceDetails(HeaderedPage):
    """
    Activate Device Details page object model class.
    """

    def __init__(self, page: Page, cluster: str, serial_number: str):
        """
        Initialize Activate Device Details page object.
        :param page: page.
        :param cluster: cluster url.
        :param serial_number: device serial number.
        """
        log.info("Initialize Activate Device Details page object")
        super().__init__(page, cluster)
        self.page = page
        self.table_utils = TableUtils(page)
        self.pw_utils = PwrightUtils(page)
        self.url = f"{cluster}/manage-account/activate/devices/{serial_number.upper()}"

    def edit_device_details(self, device_name, device_full_name, device_desc):
        """ Edit the existing device details of device name, device full name & device description
        :param: device name, device full name and device description
        :return: current instance of Activate Device Details page object.
        """
        log.info("Playwright: Edit device details")
        self.pw_utils.click_selector(ActivateDeviceDetailsSelectors.EDIT_DEVICE_DETAILS_BTN)
        self.pw_utils.enter_text_into_element(ActivateDeviceDetailsSelectors.DEVICE_NAME_INPUT, device_name)
        self.pw_utils.enter_text_into_element(ActivateDeviceDetailsSelectors.DEVICE_FULL_NAME_INPUT, device_full_name)
        self.page.get_by_test_id(ActivateDeviceDetailsSelectors.DEVICE_DESC_INPUT).fill(device_desc)
        self.pw_utils.click_selector(ActivateDeviceDetailsSelectors.SAVE_CHANGES_BTN)
        return self

    def should_have_details_update_success_notification(self, text):
        """Validate the device details update success notification
        :param: text message to be validated
        :return: current instance of Activate Device Details page object.
        """
        log.info("Playwright: Validate the device details update success notification")
        self.page.wait_for_load_state("domcontentloaded")
        expect(self.page.locator(ActivateDeviceDetailsSelectors.DEVICE_UPDATED_SUCCESS_NOTIFICATION)).to_have_text(text)
        return self
