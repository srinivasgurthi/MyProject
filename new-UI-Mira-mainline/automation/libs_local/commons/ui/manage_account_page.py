"""
Manage account page object model
"""
import logging

from playwright.sync_api import Page

from hpe_glcp_automation_lib.libs.adi.ui.activate_devices_page import ActivateDevices
from hpe_glcp_automation_lib.libs.audit_logs.ui.audit_logs_page import AuditLogs
from hpe_glcp_automation_lib.libs.acct_mgmt.ui.account_type_page import AccountType
from hpe_glcp_automation_lib.libs.commons.ui.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.commons.ui.identity_page import Identity
from hpe_glcp_automation_lib.libs.commons.ui.locators import ManageAccountSelectors
from hpe_glcp_automation_lib.libs.sm.ui.device_subscriptions import DeviceSubscriptions

log = logging.getLogger(__name__)


class ManageAccount(HeaderedPage):
    """
    Manage account page object model class
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize manage account page object
        :param page: page
        :param cluster: cluster url
        """
        log.info("Initialize ManageAccount page object")
        super().__init__(page, cluster)
        self.url = f"{cluster}/manage-account"

    def open_audit_logs(self):
        """
        Navigate to Audit Logs page by clicking on tile on manage account page.
        :return: new instance of Audit Logs page object.
        """
        log.info(f"Playwright: navigate to Audit Logs page")
        self.pw_utils.wait_for_selector(ManageAccountSelectors.CARD_AUDIT_LOGS)
        self.page.locator(ManageAccountSelectors.CARD_AUDIT_LOGS).click()
        self.page.wait_for_load_state("domcontentloaded")
        self.pw_utils.save_screenshot(self.test_name)
        return AuditLogs(self.page, self.cluster)

    def open_identity_and_access(self):
        """
        Navigate to Identity & Access page by clicking on tile on manage account page.
        :return: new instance of Identity & Access page object.
        """
        log.info(f"Playwright: navigate to Identity & Access page")
        self.pw_utils.wait_for_selector(ManageAccountSelectors.CARD_IDENTITY_AND_ACCESS)
        self.page.locator(ManageAccountSelectors.CARD_IDENTITY_AND_ACCESS).click()
        self.page.wait_for_load_state("domcontentloaded")
        self.pw_utils.save_screenshot(self.test_name)
        return Identity(self.page, self.cluster)

    def open_subscriptions(self):
        """
        Navigate to Subscriptions page by clicking on tile on manage account page.
        :return: new instance of DeviceSubscriptions page object.
        """
        log.info(f"Playwright: navigate to Device Subscriptions page")
        self.pw_utils.wait_for_selector(ManageAccountSelectors.CARD_SUBSCRIPTIONS)
        self.page.locator(ManageAccountSelectors.CARD_SUBSCRIPTIONS).click()
        self.page.wait_for_load_state("domcontentloaded")
        self.pw_utils.save_screenshot(self.test_name)
        return DeviceSubscriptions(self.page, self.cluster)

    def open_account_type(self):
        """
        Navigate to Account Type page.
        :return: instance of Account Type page
        """
        log.info("Playwright: navigate to Account Type page")
        self.page.wait_for_selector(ManageAccountSelectors.MANAGE_ACCOUNT_TYPE_BUTTON).click()
        self.page.wait_for_load_state("domcontentloaded")
        self.pw_utils.save_screenshot(self.test_name)
        return AccountType(self.page, self.cluster)

    def open_activate(self):
        """
        Navigate to Activate page by clicking on tile on manage account page.
        :return: new instance of ActivateDevices page object.
        """
        log.info(f"Playwright: navigate to Activate Devices page")
        self.pw_utils.wait_for_selector(ManageAccountSelectors.CARD_ACTIVATE)
        self.page.locator(ManageAccountSelectors.CARD_ACTIVATE).click()
        self.page.wait_for_load_state("domcontentloaded")
        self.pw_utils.save_screenshot(self.test_name)
        return ActivateDevices(self.page, self.cluster)

    def get_pcid(self):
        """

        :return: Current logged in account platform customer ID value
        """
        return self.page.locator(ManageAccountSelectors.PCID_VALUE_SELECTOR).text_content()
