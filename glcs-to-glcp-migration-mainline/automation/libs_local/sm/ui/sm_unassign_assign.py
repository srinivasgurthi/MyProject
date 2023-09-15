import logging
import time

import allure

log = logging.getLogger(__name__)
time_delay = 7


class AssignUnassignPaths(object):
    def __init__(self):
        self.devices_menu_btn = 'data-testid=devices-nav-menu'
        self.search_field = 'data-testid=search-field'
        self.select_all_nth_btn = 'aria-label=select all'
        self.detach_subs_btn = 'data-testid=detach-subscription-btn'
        self.detach_btn = 'data-testid=detach-btn'
        self.close_btn = 'data-testid=close-btn'
        self.devices_btn = 'data-testid=devices-btn'
        self.apply_to_subs_btn = 'data-testid=apply-to-subscriptions-btn'
        self.apply_subs_btn = 'data-testid=apply-subscriptions-btn'
        self.lic_tier_dropdown = 'data-testid=license-tier-dropdown'
        self.adv_ap_text = 'text=Advanced AP'
        self.apply_sub_btn = 'data-testid=apply-subscription-btn'
        self.click_finish = 'data-testid=button-finish'
        self.assigned_lic_summary = 'data-testid=text-assigned-licensed-tab-summary'
        self.select_all = '[aria-label=\"select all\"] div'
        self.action_btn = '[data-testid=\"bulk-actions\"] [aria-label=\"Open Drop\"]'
        self.gw_foundation_lic = 'text=Foundation-70XX'
        self.gw_lic_text = "Foundation-70XX"


class SmUnassignAssignDevicePages(object):
    def __init__(self):
        self.selectors = AssignUnassignPaths()
        log.info(f"Initialize {__name__}")

    def SmUnassignAssignDevicePages_fn(self, page, record_dir, random_str, dm_pw_data, dm_pw_data_except, sm_pw_data,
                                       test_name):
        try:
            page.locator(self.selectors.devices_menu_btn).click()
            try:
                page.locator(dm_pw_data).nth(1).click()
            except:
                page.locator(dm_pw_data_except).nth(1).click()
                page.locator(self.selectors.action_btn).click()
                page.locator(self.selectors.detach_subs_btn).click()
                page.locator(self.selectors.detach_btn).click()
                page.locator(self.selectors.close_btn).click()
                page.locator(dm_pw_data).nth(1).click()
                time.sleep(time_delay)
                page.screenshot(path=record_dir + random_str + test_name + ".png", full_page=True)
                allure.attach.file(source=record_dir + random_str + test_name + ".png")
            page.locator(self.selectors.action_btn).click()

            page.locator(self.selectors.apply_to_subs_btn).click()
            page.locator(self.selectors.apply_subs_btn).click()

            if "Foundation-70XX" in sm_pw_data:
                page.locator(self.selectors.lic_tier_dropdown).click()
                page.locator(self.selectors.gw_foundation_lic).click()
            page.locator(sm_pw_data).nth(1).click()
            page.screenshot(path=record_dir + random_str + test_name + ".png", full_page=True)
            allure.attach.file(source=record_dir + random_str + test_name + ".png")
            page.locator(self.selectors.apply_sub_btn).click()
            page.locator(self.selectors.click_finish).click()
            page.locator(self.selectors.close_btn).click()
            page.screenshot(path=record_dir + random_str + test_name + ".png", full_page=True)
            allure.attach.file(source=record_dir + random_str + test_name + ".png")
            return True
        except Exception as e:
            page.screenshot(path=record_dir + random_str + test_name + ".png", full_page=True)
            allure.attach.file(source=record_dir + random_str + test_name + ".png")
            log.error("not able to locate the role on the page {}".format(e))
            return False
