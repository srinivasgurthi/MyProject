import logging

from playwright.sync_api import Page, expect

from hpe_glcp_automation_lib.libs.commons.ui.headered_page import HeaderedPage
from hpe_glcp_automation_lib.libs.app_prov.ui.applications_details_page import ApplicationsDetails
from hpe_glcp_automation_lib.libs.app_prov.ui.locators import AvailableAppsSelectors, AppNavigationSelectors

log = logging.getLogger()


class AvailableApplications(HeaderedPage):
    """
    Available Applications Page Object Model
    """

    def __init__(self, page: Page, cluster: str):
        """
         Initialize with page and cluster
        :param page: Page
        :param cluster: cluster under test url
        """
        log.info("Playwright: Initialize available apps page.")
        super().__init__(page, cluster)
        self.url = f"{cluster}/applications/available-apps"

    def wait_for_loaded_list(self):
        """
         Wait for list of applications is not empty and loader spinner is not present on the page.
        :return: current instance of Available Applications page object.
        """
        log.info("Playwright: wait for applications list is loaded.")
        self.page.locator(AvailableAppsSelectors.LOADER_SPINNER).wait_for(
            state="hidden")
        self.page.wait_for_selector(
            AvailableAppsSelectors.APPLICATION_CARD_TEMPLATE, state="visible", strict=False)
        self.page.wait_for_load_state("domcontentloaded")
        return self

    def open_view_details_on_application(self, app_uuid: str):
        """
        click on the view details to open the application.
        :param app_uuid: uuid of the application
        :return instance of ApplicatonDetails.
        """
        log.info(
            "Playwright: views details done clickable action after application open.")
        self.pw_utils.click_selector(
            AvailableAppsSelectors.VIEW_DETAILS_BTN_TEMPLATE.format(app_uuid))
        return ApplicationsDetails(self.page, self.cluster, app_uuid)

    def should_have_appplication(self, app_uuid: str):
        """
         Check for the application existence
        :param app_uuid: application uuid
        :return: current instance of Available Applications page object
        """
        log.info(
            f"Playwright: check the application existence with uuid '{app_uuid}' in My Applications page.")
        self.pw_utils.save_screenshot(self.test_name)
        expect(self.page.locator(
            AvailableAppsSelectors.APPLICATION_CARD_TEMPLATE.format(
                app_uuid))).to_be_visible()
        return self

    def open_my_applications(self):
        """
        Navigate to My Applcation page.
        """
        log.info("Playwright: navigate to My Applications page")
        self.page.wait_for_selector(AppNavigationSelectors.MY_APPS_BTN).click()
