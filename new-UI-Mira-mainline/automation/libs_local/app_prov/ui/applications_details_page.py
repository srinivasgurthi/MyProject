import logging

from playwright.sync_api import Page

from hpe_glcp_automation_lib.libs.commons.ui.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.app_prov.ui.locators import AppsDetailsSelectors
from hpe_glcp_automation_lib.libs.app_prov.ui.installed_applications_page import InstalledApplications

log = logging.getLogger()


class ApplicationsDetails(HeaderedPage):
    """
    Applications Details page object model
    """

    def __init__(self, page: Page, cluster: str, app_uuid: str, region: str = None):
        """
         Initialize with page and cluster
        :param page: Page
        :param cluster: cluster under test url
        """
        log.info(f"Playwright: Initialize the application details page for '{app_uuid}'")
        super().__init__(page, cluster)
        if region:
            _region = '-'.join(region.lower().split())
            self.url = f"{cluster}/applications/app-details/{app_uuid}/{_region}"
        else:
            self.url = f"{cluster}/applications/app-details/{app_uuid}"
        self.app_uuid = app_uuid
        self.region = region

    def setup_application(self, region: str):
        """
         Install the application to the given region
        :param region: region to deploy application
        :return current instance of Install Applications page object.
        """
        log.info(f"Playwright: Install the application for the region: '{region}'")
        self.pw_utils.click_selector(AppsDetailsSelectors.SETUP_APPLICATION_BTN)
        self.page.wait_for_selector(AppsDetailsSelectors.ADD_APPLICATION_MODAL)
        self.page.locator(AppsDetailsSelectors.DEPLOYMENT_REGION).click()
        self.page.locator(AppsDetailsSelectors.REGION_OPTION_TEMPLATE.format(region)).click()
        self.page.locator(
            AppsDetailsSelectors.TERMS_CHECKBOX).click()
        self.page.locator(AppsDetailsSelectors.DEPLOY_BTN).click()
        return InstalledApplications(self.page, self.cluster, self.app_uuid)
