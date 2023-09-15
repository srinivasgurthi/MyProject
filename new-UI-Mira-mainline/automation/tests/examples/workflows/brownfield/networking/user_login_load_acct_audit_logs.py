import logging
import os
from automation.conftest import ExistingUserAcctDevices, RECORD_DIR
from hpe_glcp_automation_lib.libs.authn.ui.login_to_homepage import Login
from playwright.sync_api import BrowserContext
from hpe_glcp_automation_lib.libs.audit_logs.ui.audit_logs_pages.audit_logs import AuditLogs

log = logging.getLogger(__name__)

class WfUserLoginLoadAcctAudit():
    def __init__(self):
        self.cluster = ExistingUserAcctDevices.login_page_url
        self.test_data = ExistingUserAcctDevices.test_data
        self.login_data = ExistingUserAcctDevices.login_data

    def wf_webui_login(self, browser):
        context: BrowserContext = browser.new_context(record_video_dir=RECORD_DIR)
        page = context.new_page()
        page.goto(self.cluster)
        username = self.test_data['test_name_username']
        password = self.login_data['users'][username]
        pcid_name = self.test_data['test_name_acct_name']
        ui_login = Login(username, password)
        login_successful = ui_login.login_acct(page)
        page.wait_for_url(url=f"{self.cluster}/home")
        storage_state_path = os.path.join(RECORD_DIR, "user_login_load_acct_info_store.json")
        context.storage_state(path=storage_state_path)
        page.close()
        context.close()
        if not login_successful:
            raise Exception(f"Error: Login by {self.login_data.user} has failed.")
        return storage_state_path

    def wf_sm_iap_audit_log_info(self, browser_instance, storage_state_path, device_order_info=None) -> bool:
        """ Step #15: Check subscription for device's serial number."""
        if not device_order_info:
            search_str = self.test_data['test_name_iap_serial']
            app_instance_name = self.test_data['test_name_app_instance_name']
        "Device with serial STIAP7S2VU is assigned to application Central_yoda2"
        log.info(f"Playwright: verifying Device with serial '{search_str}' is assigned to application '{app_instance_name}'")
        audit_logs = AuditLogs()
        return audit_logs.check_subscr_audit_logs(self.cluster, browser_instance, storage_state_path,
                                                  search_str)

    def wf_sm_sw_audit_log_info(self, browser_instance, storage_state_path, device_order_info=None) -> bool:
        """ Step #15: Check subscription for device's serial number."""
        if not device_order_info:
            search_str = self.test_data['test_name_iap_serial']
            app_instance_name = self.test_data['test_name_app_instance_name']
        "Device with serial STIAP7S2VU is assigned to application Central_yoda2"
        log.info(f"Playwright: verifying Device with serial '{search_str}' is assigned to application '{app_instance_name}'")
        audit_logs = AuditLogs()
        return audit_logs.check_subscr_audit_logs(self.cluster, browser_instance, storage_state_path,
                                                  search_str)