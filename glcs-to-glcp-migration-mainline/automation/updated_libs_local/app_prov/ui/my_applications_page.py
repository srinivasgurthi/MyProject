"""
My Applications page object model.
"""
import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.app_prov.ui.locators import MyApplicationsSelectors, AppNavigationSelectors
from hpe_glcp_automation_lib.libs.commons.ui.headered_page import HeaderedPage


log = logging.getLogger(__name__)


class MyApplications(HeaderedPage):
    """
    My Applications page object model class.
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize My Applications page object.
        :param page: page.
        :param cluster: cluster url.
        """
        log.info("Initialize My Applications page object")
        super().__init__(page, cluster)
        self.url = f"{cluster}/applications/my-apps"

    def wait_for_loaded_list(self):
        """
        Wait for list of applications is not empty and loader spinner is not present on the page.
        :return: current instance of My Applications page object.
        """
        log.info("Playwright: wait for applications list is loaded.")
        self.page.wait_for_selector(MyApplicationsSelectors.APPLICATION_TILE, state="visible", strict=False)
        self.page.locator(MyApplicationsSelectors.LOADER_SPINNER).wait_for(state="hidden")
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def should_contain_text_in_title(self, text):
        """
        Check that expected text is present as part of the heading page title.
        :param text: expected text to be contained in title.
        :return: current instance of My Applications page object.
        """
        log.info(f"Playwright: check that title contains text '{text}' in My Applications page.")
        self.pw_utils.save_screenshot(self.test_name)
        expect(self.page.locator(MyApplicationsSelectors.HEADING_PAGE_TITLE)).to_contain_text(text)
        return self

    def should_have_text_in_title(self, text):
        """
        Check that expected text matches with the heading page title.
        :param text: expected text to match with the text in title.
        :return: current instance of My Applications page object.
        """
        log.info(f"Playwright: check that title has text '{text}' in My Applications page.")
        self.pw_utils.save_screenshot(self.test_name)
        expect(self.page.locator(MyApplicationsSelectors.HEADING_PAGE_TITLE)).to_have_text(text)
        return self

    def should_have_appplication(self, app_uuid: str):
        """
         Check for the application existence
        :param app_uuid: application uuid
        :return: current instance of My Applications page object
        """
        log.info(f"Playwright: check the application existence with uuid '{app_uuid}' in My Applications page.")
        self.pw_utils.save_screenshot(self.test_name)
        expect(self.page.locator(MyApplicationsSelectors.APPLICATION_CARD_TEMPLATE.format(app_uuid))).to_be_enabled()
        return self

    def open_available_applications(self):
        """
        Navigate to Available Applcation page.
        """
        log.info("Playwright: navigate to Available Applications page")
        self.page.wait_for_selector(AppNavigationSelectors.AVAILABLE_APPS_BTN).click()
