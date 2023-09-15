"""
Base Page for page object model
"""
import logging
import os

from playwright.sync_api import Page

from hpe_glcp_automation_lib.libs.commons.ui.locators import BasePageSelectors
from hpe_glcp_automation_lib.libs.commons.utils.pwright.pwright_utils import PwrightUtils

log = logging.getLogger(__name__)


class BasePage:
    """
    Base Page for page object model class
    """

    def __init__(self, page: Page, cluster: str):
        """
        Initialize with page and cluster
        :param page: Page
        :param cluster: cluster under test url
        """
        self.test_name = os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]
        self.pw_utils = PwrightUtils(page)
        self.page = page
        self.cluster = cluster
        self.url = None

    def open(self):
        """
        Navigating to page url
        :return: instance of current page object
        """
        if not self.url:
            raise Exception("URL was not specified.")
        self.page.goto(self.url)
        self.pw_utils.wait_for_url(f"{self.url}", timeout_ignore=True, timeout=20000)
        current_url = self.page.url
        if not current_url == self.url:
            log.error("Unexpected URL")
            self.pw_utils.save_screenshot(self.test_name)
            raise Exception(f"Wrong page opened instead of expected '{self.url.split('/')[-1]}': '{current_url}'")
        return self

    def wait_for_loaded_state(self):
        """
        Wait till page is loaded and loading spinner is not present
        :return: instance of current page object
        """
        self.page.wait_for_url(self.url)
        self.page.locator(BasePageSelectors.APP_LOADER).wait_for(state="hidden")
        self.pw_utils.wait_for_selector(BasePageSelectors.LOADER_SPINNER, state="visible", timeout_ignore=True,
                                        timeout=5000)
        self.page.locator(BasePageSelectors.LOADER_SPINNER).wait_for(state="hidden")
        self.page.wait_for_load_state("domcontentloaded")
        return self
