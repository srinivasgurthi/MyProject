"""
Add Devices page object model.
"""
import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.adi.ui.locators import AddDevicesSelectors
from hpe_glcp_automation_lib.libs.audit_logs.ui.audit_logs_page import AuditLogs
from hpe_glcp_automation_lib.libs.commons.ui.base_page import BasePage

log = logging.getLogger(__name__)


class AddDevices(BasePage):
    """
    Add Devices page object model class.
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize Add Devices page object.
        :param page: page.
        :param cluster: cluster url.
        """
        log.info("Initialize Add Devices page object")
        super().__init__(page, cluster)
        self.url = f"{cluster}/devices/inventory/add-devices"

    def click_next_button(self):
        """Click next button of Add Devices wizard.

        :return: current instance of AddDevices page object.
        """
        log.info("Playwright: click next button at Add Devices wizard.")
        self.page.locator(AddDevicesSelectors.NEXT_BUTTON).click()
        return self

    def click_finish_button(self):
        """Click finish button of Add Devices wizard.

        :return: current instance of AddDevices page object.
        """
        log.info("Playwright: click finish button at Add Devices wizard.")
        self.page.locator(AddDevicesSelectors.FINISH_BUTTON).click()
        return self

    def select_device_type(self, device_type):
        """Choose element from the items list of "Device Type" dropdown.

        :param device_type: text, representing accessible name of the element to pick. Valid values:
            "Networking Devices", "Storage Devices", "Compute Devices".
        :return: current instance of AddDevices page object.
        """
        log.info(f"Playwright: choose '{device_type}' device type at Add Devices wizard.")
        self.pw_utils.select_drop_down_element(drop_menu_selector=AddDevicesSelectors.DEVICE_TYPE_DROPDOWN,
                                               element=device_type,
                                               element_role="option",
                                               exact_match=True)
        return self

    def select_serial_and_mac_option(self):
        """Choose option for adding by serial number and mac-address at Add Devices wizard.

        :return: current instance of AddDevices page object.
        """
        log.info("Playwright: Choose adding device by serial and mac-address at Add Devices wizard.")
        self.page.locator(AddDevicesSelectors.SERIAL_AND_MAC_RADIO).click()
        return self

    def enter_serial_and_mac(self, serial, mac_addr):
        """Enter serial number and mac-address at Add Devices wizard.

        :param serial: device's serial number.
        :param mac_addr: device's mac-address.
        :return: current instance of AddDevices page object.
        """
        log.info(f"Playwright: Enter serial '{serial}' and mac-address '{mac_addr}' at Add Devices wizard.")
        self.page.locator(AddDevicesSelectors.SERIAL_NUMBER_INPUT).fill(serial)
        self.page.locator(AddDevicesSelectors.MAC_ADDRESS_INPUT_SERIAL).fill(mac_addr)
        self.page.locator(AddDevicesSelectors.ENTER_BUTTON).click()
        return self

    def select_delivery_contact_by_number(self, index):
        """Choose element by index (starting from 1) of the item in "Service Delivery Contact" dropdown items list.

        :param index: index (starting from 1) of dropdown list item to pick.
        :return: current instance of AddDevices page object.
        """
        log.info(f"Playwright: choose delivery contact #{index} at Add Devices wizard.")
        self.pw_utils.select_drop_down_element_by_index(
            dropdown_selector=AddDevicesSelectors.DELIVERY_CONTACT_DROPDOWN,
            list_items_selector=AddDevicesSelectors.DELIVERY_CONTACT_LIST_ITEM,
            item_index=index
        )
        return self

    def click_view_audit_log(self):
        """Click "View Audit Log" button of Add Devices wizard's popup.

        :return: instance of AuditLogs page object.
        """
        log.info("Playwright: click 'View Audit Log' button at Add Devices wizard.")
        self.page.locator(AddDevicesSelectors.VIEW_AUDIT_LOG_BTN).click()
        return AuditLogs(self.page, self.cluster)

    def close_popup(self):
        """Click "Close" button of Add Devices wizard's popup.

        """
        log.info("Playwright: click 'Close' button at Add Devices wizard.")
        self.page.locator(AddDevicesSelectors.CLOSE_BTN).click()
        # Note: page object cannot be returned when navigating to the previous pages due to the circular import

    def should_have_rows_count(self, count):
        """Check that displayed rows count in table is matched to expected.

        :param count: expected count of rows.
        :return: current instance of AddDevices page object.
        """
        log.info(f"Playwright: wait for rows count {count} in table.")
        self.pw_utils.save_screenshot(self.test_name)
        expect(self.page.locator(AddDevicesSelectors.TABLE_ROWS)).to_have_count(count)
        self.page.wait_for_load_state("domcontentloaded")
        return self
