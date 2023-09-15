import logging
import os

import allure
from allure_commons.types import AttachmentType
from playwright.sync_api import expect, Browser

from hpe_glcp_automation_lib.libs.utils.pwright.pwright_utils import PwrightUtils
from hpe_glcp_automation_lib.libs.utils.random_gens import RandomGenUtils

log = logging.getLogger(__name__)
RECORD_DIR = os.path.join('tmp', 'results')


class AuditLogsPaths:
    go_to_acct_button = "[data-testid=\"tile-action-btn\"]:has-text('Go to Account')"
    manage_nav_menu = "[data-testid=\"manage-nav-menu\"]"
    card_audit_logs = "[data-testid=\"card-audit-logs\"]"
    search_field = "[data-testid=\"search-field\"]"
    heading_audit_log_description = "[data-testid=\"heading-audit-log-details\"] div"
    # close_button = "[data-testid=\"close-button\"]"
    # menu_item_user_button = "[data-testid=\"drop-btn-glcp-header-all-menu-item-user\"]"
    # sign_out_button = "[data-testid=\"text-desc-sign-out-hpe-nav-menu\"]"
    audit_log_sm_item_template = "tr:has-text(\"Subscription Management\") td:has-text(\"{}\")"


class AuditLogs:
    def __init__(self):
        log.info("Initialize subscription audit logs check")
        self.selectors = AuditLogsPaths()
        self.s_shot = PwrightUtils()

    def check_subscr_audit_logs(self, url: str, browser: Browser, storage_state_path: str,
                                device_serial_number: str) -> bool:
        random_str = RandomGenUtils.random_string_of_chars(7)
        test_name = os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]
        context = browser.new_context(storage_state=storage_state_path, record_video_dir=RECORD_DIR)
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
        page = context.new_page()
        try:
            expected_description = f"Serial: {device_serial_number} op: DEVICE_SUBSCRIPTION_ASSIGNED"
            audit_log_sm_item = self.selectors.audit_log_sm_item_template.format(expected_description)
            page.set_default_timeout(30000)
            page.goto(url)
            homepage_opened = PwrightUtils.wait_after_url(page, f"{url}/home", timeout_ignore=True, timeout=20000,
                                                          delay=0)
            if not homepage_opened:
                log.info(f"Playwright: open first available account")
                page.locator(self.selectors.go_to_acct_button).nth(0).click()
                page.wait_for_load_state("domcontentloaded")
            self.s_shot.save_screenshot(page, test_name)
            log.info(f"Playwright: navigate to Audit Logs page")
            PwrightUtils.wait_after_selector(page, self.selectors.manage_nav_menu)
            page.locator(self.selectors.manage_nav_menu).click()
            PwrightUtils.wait_after_selector(page, self.selectors.card_audit_logs)
            page.locator(self.selectors.card_audit_logs).click()
            page.wait_for_load_state("domcontentloaded")
            self.s_shot.save_screenshot(page, test_name)
            log.info(f"Playwright: check that 'DEVICE_SUBSCRIPTION_ASSIGNED' item "
                     f"for S/N: '{device_serial_number}' is present in table")
            page.locator(self.selectors.search_field).click()
            page.locator(self.selectors.search_field).fill(device_serial_number)
            page.locator(self.selectors.search_field).press("Enter")
            page.wait_for_load_state("domcontentloaded")
            PwrightUtils.wait_after_selector(page,
                                             audit_log_sm_item,
                                             timeout_ignore=True,
                                             timeout=30000)
            self.s_shot.save_screenshot(page, test_name)
            expect(page.locator(audit_log_sm_item)).to_be_visible()
            log.info(f"Playwright: check that description in item details is correct")
            page.locator(audit_log_sm_item).click()
            page.wait_for_load_state("domcontentloaded")
            self.s_shot.save_screenshot(page, test_name)
            expect(page.locator(self.selectors.heading_audit_log_description)).to_have_text(expected_description)
            # TODO: Investigate reusing storage state after logout
            # page.locator(self.selectors.close_button).click()
            # page.locator(self.selectors.menu_item_user_button).click()
            # page.locator(self.selectors.sign_out_button).click()
            result = True

        except Exception as ex:
            log.error(f"Subscription audit logs check was not successful: {ex}")
            result = False

        finally:
            page.close()
            trace_attachment = f"{random_str}_{test_name}.zip"
            trace_attachment_path = f"{RECORD_DIR}{trace_attachment}"
            context.tracing.stop(path=trace_attachment_path)
            allure.attach.file(source=trace_attachment_path, name=trace_attachment)
            context.close()
            path = page.video.path()
            allure.attach.file(source=path, name="video", attachment_type=AttachmentType.WEBM)

        return result
