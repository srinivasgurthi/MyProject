# Copyright 2023 - Hewlett Packard Enterprise Company
""" GLC app page"""

import logging
from playwright.sync_api import expect
import re
LOG = logging.getLogger(__name__)

class GLCPPaths:
    glcp_logo = "glcp-header-all-brand"
    dashboard_menu = "dashboard-nav-menu"
    application_menu = "application-nav-menu"
    devices_menu = "devices-nav-menu"
    manage_menu = "manage-nav-menu"
    user_icon = "drop-btn-glcp-header-all-menu-item-user"
    installed_app_list = "installed-app-list-action-btn"
    manage_subscription = "manage-subscription-btn"
    region_dropdown = "app-detail-region-dropdown"
    deployed_regions = "view-deplopyed-regions-btn"
    launch_action = "launch-action-btn"
    api_action = "card-api"
    create_client_credentails_button = "create-credentials-btn"
    create_client_credentails_form_button = "create-credential-form-btn"
    

class GreenLakeCentralApp(object):
    def __init__(self) -> None:
        self.selectors = GLCPPaths()
        LOG.info(f"Initialize {__name__}")

    def navigate_to_glcp_account(self, page, account_name):
        page.get_by_text(account_name).click()
    
    def navigate_to_applications_page(self, page):
        # if "my-apps" not in page.url:
        LOG.info("Navigate to Applications page")
        page.get_by_test_id(self.selectors.application_menu).click()

    def navigate_to_applications_details_page(self, page, application_name = "HPE GreenLake Central"):
        # if "app-details" not in page.url:
        LOG.info(f"Navigate to {application_name} details page")
        self.navigate_to_applications_page(page)
        page.wait_for_load_state()        
        page.get_by_text(application_name).click()
        page.wait_for_load_state()
        page.get_by_test_id(self.selectors.installed_app_list).get_by_role("button", name="Open Drop").click()
        page.get_by_text("View Application Details").click()

    def check_manage_subscriptions(self, page, application_name = "HPE GreenLake Central"):
        LOG.info(f"Check \"Manage Subscriptions\" is NOT shown in {application_name} details page.")
        self.navigate_to_applications_details_page(application_name)
        return not page.get_by_test_id(self.selectors.manage_subscription).is_visible()

    def check_region_drop_down(self, page, application_name = "HPE GreenLake Central"):
        LOG.info(f"Check \"Region drop down\" is NOT shown in {application_name} details page.")
        self.navigate_to_applications_details_page(application_name)
        return not page.get_by_test_id(self.selectors.region_dropdown).is_visible()

    def check_view_deployed_region(self, page, application_name = "HPE GreenLake Central"):
        LOG.info(f"Check \"View Deployed Regions\" is shown in {application_name} details page.")
        self.navigate_to_applications_details_page(page=page, application_name=application_name)
        return page.get_by_test_id(self.selectors.deployed_regions).is_enabled()

    def check_application(self, page, application_name):
        LOG.info(f"Checking {application_name} present in My Applications page.")
        self.navigate_to_applications_page(page)
        page.wait_for_load_state()
        return page.get_by_text(application_name).is_enabled()

    def launch_glc_app(self, page):
        LOG.info(f"Entering {GreenLakeCentralApp.launch_glc_app.__qualname__}")
        self.navigate_to_applications_page(page)
        page.get_by_text("HPE GreenLake Central").click()
        page.get_by_test_id(self.selectors.launch_action).click()
        page.wait_for_load_state()

    def verify_useremail_and_tenant_in_glc(self, page, useremail, tenant):
        page.get_by_role("button", name="User").click()
        page.wait_for_load_state()
        return page.get_by_text(useremail).is_visible() and page.get_by_text(tenant).is_visible()

    def _click_change_tenant(self, page):
        page.get_by_role("button", name = "User").click()
        if not page.get_by_role("menuitem", name="Change Tenant").is_enabled():
            page.get_by_role("button", name = "User").click()
        page.wait_for_load_state()
        page.get_by_role("menuitem", name="Change Tenant").click()

    def check_tenant(self, page, tenant):
        LOG.info(f"Search tenant {tenant}")
        return page.locator(f"text={tenant}Go to tenant").is_enabled()

    def navigate_to_manage_api(self, page, account_name):
        account_id = None
        page.get_by_test_id(self.selectors.manage_menu).click()
        page.wait_for_load_state()
        expect(page.get_by_test_id("heading-company-name").get_by_text(f"{account_name}", exact=True)).to_be_visible()
        account_id = page.locator("data-testid=account-id-val").text_content()
        page.get_by_test_id(self.selectors.api_action).click()
        return account_id

    def create_client_credentials(self, page, creadential_name = "Test-API", application_name = "HPE GreenLake Central ( US West )"):
        LOG.info(f"Create Client Credentials")
        client_secret = None
        page.wait_for_load_state()
        page.get_by_test_id(self.selectors.create_client_credentails_button).click()
        expect(page.get_by_test_id(self.selectors.create_client_credentails_form_button).get_by_text("Create Credentials", exact=True)).to_be_visible()
        page.get_by_test_id("credential-name-input").fill(creadential_name)
        page.get_by_role('button', name="Select Application").click()
        page.get_by_role('option', name=f"{application_name}").first.click()
        page.get_by_test_id(self.selectors.create_client_credentails_form_button).click()
        page.wait_for_load_state()
        expect(page.get_by_test_id('heading-modal-title').get_by_text("Credentials Created", exact=True)).to_be_visible()
        client_secret = page.get_by_test_id('client-secret-copy-field-text-field-input').input_value()
        page.get_by_test_id('create-credential-close-modal-btn').click()
        page.wait_for_load_state()
        LOG.info(f"Client Credentials Created")
        return client_secret
    
    def generate_accesstoken(self, page, client_secret, creadential_name):
        jwt_token = None
        LOG.info(f"Generating Accesstoken from client secret")
        expect(page.get_by_test_id("undefined-accordion-panel").get_by_text(f"{creadential_name}", exact=True)).to_be_visible()
        page.get_by_test_id("undefined-accordion-panel").click()
        expect(page.get_by_test_id("generate-access-token-btn").get_by_text(f"Generate Access Token", exact=True)).to_be_visible()
        page.get_by_test_id("generate-access-token-btn").click()
        expect(page.get_by_test_id("heading-modal-title").get_by_text(f"Generate Access Token", exact=True)).to_be_visible()
        page.get_by_test_id("client-secret-input").fill(client_secret)
        page.get_by_test_id("create-access-token-form-btn").click()
        expect(page.get_by_test_id("heading-modal-title").get_by_text(f"Access Token Created", exact=True)).to_be_visible()
        jwt_token = page.get_by_test_id("access-token-text-field-input").input_value()
        page.get_by_test_id("generate-token-close-modal-btn").click()
        return jwt_token
    
    def get_data_test_id_from_available_applications(self, page, application_name):
        application_id = None
        html_data = page.content()
        page.wait_for_load_state()
        pattern = r'<span data-testid="text-application-name-(?P<id>[^"]+)"[^>]*>{}</span>'.format(application_name)
        match = re.search(pattern, html_data)
        if match:
            application_id = match.group('id')
            LOG.info(f"Found application id {application_id} for application name {application_name}")
        else:
            LOG.error(f"Unable to find application id for application name {application_name}")
        return application_id


        

        

        
    




