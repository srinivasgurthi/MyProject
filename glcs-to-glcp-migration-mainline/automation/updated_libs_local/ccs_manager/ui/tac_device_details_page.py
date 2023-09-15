"""
TAC Device Details page object model.
"""
import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.ccs_manager.ui.locators import TacDeviceDetailsSelectors
from hpe_glcp_automation_lib.libs.commons.ui.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import TableUtils

log = logging.getLogger(__name__)


class TacDeviceDetailsPage(HeaderedPage):
    """
    TAC Device Details page object model class.
    """

    def __init__(self, page: Page, cluster: str, serial: str):
        """Initialize Device Details page object.

        :param page: page.
        :param cluster: cluster url.
        :param serial: serial number of opened device's details.
        """
        log.info("Initialize Device Details page object.")
        super().__init__(page, cluster)
        self.table_utils = TableUtils(page)
        self.url = f"{cluster}/manage-ccs/devices/{serial}"

    def go_back_to_devices(self):
        log.info("Playwright: navigating back to devices list.")
        self.page.locator(TacDeviceDetailsSelectors.DEVICES_BTN).click()
        # Note: page object cannot be returned when navigating to the previous pages due to the circular import

    def should_have_mac_address(self, mac_addr):
        """Check displayed MAC-address at device details page.

        :param mac_addr: expected value of MAC-address.
        :return: current instance of TAC Device Details page object.
        """
        log.info(f"Playwright: check that device has correct MAC-address '{mac_addr}' at device details page.")
        expect(self.page.locator(TacDeviceDetailsSelectors.MAC_ADDRESS_VALUE)).to_have_text(mac_addr)
        return self

    def should_have_serial(self, serial):
        """Check displayed serial number at device details page.

        :param serial: expected value of serial number.
        :return: current instance of TAC Device Details page object.
        """
        log.info(f"Playwright: check that device has correct serial number '{serial}' at device details page.")
        expect(self.page.locator(TacDeviceDetailsSelectors.SERIAL_NUMBER_VALUE)).to_have_text(serial)
        return self

    def should_have_part_no(self, part_no):
        """Check displayed part number at device details page.

        :param part_no: expected value of part number.
        :return: current instance of TAC Device Details page object.
        """
        log.info(f"Playwright: check that device has correct part number '{part_no}' at device details page.")
        expect(self.page.locator(TacDeviceDetailsSelectors.PART_NUMBER_VALUE)).to_have_text(part_no)
        return self

    def should_have_assigned_folder(self, folder_name):
        """Check displayed assigned folder name at device details page.

        :param folder_name: expected name of assigned folder.
        :return: current instance of TAC Device Details page object.
        """
        log.info(f"Playwright: check that device has correct folder name '{folder_name}' at device details page.")
        expect(self.page.locator(TacDeviceDetailsSelectors.FOLDER_NAME_VALUE)).to_have_text(folder_name)
        return self

    def should_have_assigned_pcid(self, pcid):
        """Check displayed assigned pcid at device details page.

        :param pcid: expected ID of assigned platform customer.
        :return: current instance of TAC Device Details page object.
        """
        log.info(f"Playwright: check that device has correct customer ID '{pcid}' at device details page.")
        expect(self.page.locator(TacDeviceDetailsSelectors.PCID_VALUE)).to_have_text(pcid)
        return self
