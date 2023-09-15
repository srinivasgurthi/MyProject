"""
Team: GLC Migration
Scrum Master: Sundari
Description: Test GLC migration and Launch GLC App in GLCP
"""
import logging
import pytest
import re

from pytest_pytestrail import pytestrail

from automation.updated_libs_local.authn.ui.base import GlcpBasePage
from automation.updated_libs_local.identity_access.users import UsersPage
from automation.updated_libs_local.usr_mgmt.glc.base import GlcBasePage
from automation.updated_libs_local.usr_mgmt.glc.user_management import UserMgmtPage
from automation.updated_libs_local.usr_mgmt.glcp.app import GreenLakeCentralApp
from automation.updated_libs_local.utils import pwright_utils
from automation.updated_libs_local.authn.ui.login_to_homepage import Login,GLCAuthnPage,GlcBasePage
from automation import conftest
from playwright.sync_api import expect,Page
from datetime import datetime
import jwt
import json
import time


LOG = logging.getLogger(__name__)

pytestmark = [
    pytest.mark.team_name("Sundari"),
]

active_devices = conftest.ExistingUserAcctDevices()
test_data = active_devices.test_data


@pytestrail.case('C1196435')
@pytest.mark.glc_migration
def test_verify_that_for_a_glcp_account_without_backing_glc_tenant_there_i_no_glc_application_provisioned_in_the_my_application_page(
        plcontext
        ):
    """
    Verify that for a GLCP account without backing GLC tenant, there is no GLC application provisioned in the My application page
    """

    users = pwright_utils.load_json_from_file(test_data["KNOWN_GLC_USERS"])
    LOG.info("Log in GLCP as test user with admin role and launch GLC app")
    LOG.info(f"Users: {users[0]}")

    page = plcontext[0].new_page()
    login = Login(users[0]['userName'],users[0]['password'])
    login.go_to_home(page,test_data['GLCP_URL'],test_data['GLCP_ACCOUNTS'][0])

    glcp = GlcpBasePage(page)
    LOG.info("Clicking Switch account button")
    glcp.switch_account()
    LOG.info("Switch account button clicked")
    company_name = "HPE-Automation-{}"
    country = "United States"
    address = "CA"
    now = datetime.now()
    date_time_str = now.strftime("%Y%m%d%H%M%S")
    company_name = company_name.format(date_time_str)
    LOG.info(f"Creating new account with Company Name - {company_name}, Country - {country} and address - {address}")
    glcp.create_account(company_name=company_name, country=country, address=address)
    LOG.info(f"New account created with Company Name - {company_name}, Country - {country} and address - {address}")
    LOG.info("Clicking Application menu")
    glcp.application_menu.click()
    LOG.info("Application menu clicked")
    LOG.info("Waiting for View Available Applications button to be visible")
    expect(page.get_by_test_id("go-avail-apps-btn").get_by_text("View Available Applications", exact=True)).to_be_visible()
    LOG.info("View Available Applications button is now visible")


@pytestrail.case('C1196433')
@pytest.mark.glc_migration
def test_verify_that_the_invited_user_is_linked_to_the_workspace_and_the_organization_by_validating_the_token(
        plcontext
        ):
    """
    Verify that the invited user is linked to the workspace and the organization by validating the token
    """

    users = pwright_utils.load_json_from_file(test_data["KNOWN_GLC_USERS"])
    LOG.info("Log in GLCP as test user with admin role and launch GLC app")
    LOG.info(f"Users: {test_data['ADMIN_USER']}")

    page = plcontext[0].new_page()
    login = Login(test_data['ADMIN_USER'],test_data['ADMIN_PASSWORD'])
    login.go_to_home(page,test_data['GLCP_URL'],test_data['GLCP_ACCOUNTS'][0])
    page.wait_for_load_state()
    glca = GreenLakeCentralApp()
    glca.check_view_deployed_region(page=page)
    time.sleep(10)
    


@pytestrail.case('C1196437')
@pytest.mark.glc_migration
def test_verify_that_the_invited_user_is_linked_to_the_workspace_and_the_organization_by_validating_the_token(
        plcontext
        ):
    """
    Verify that the invited user is linked to the workspace and the organization by validating the token
    """

    users = pwright_utils.load_json_from_file(test_data["KNOWN_GLC_USERS"])
    LOG.info("Log in GLCP as test user with admin role and launch GLC app")
    LOG.info(f"Users: {test_data['ADMIN_USER']}")

    page = plcontext[0].new_page()
    login = Login(test_data['ADMIN_USER'],test_data['ADMIN_PASSWORD'])
    login.go_to_home(page,test_data['GLCP_URL'],test_data['GLCP_ACCOUNTS'][0])
    page.wait_for_load_state()
    glca = GreenLakeCentralApp()
    creadential_name = "Testing API"
    account_id = glca.navigate_to_manage_api(page=page, account_name=test_data['GLCP_ACCOUNTS'][0])
    if account_id == None:
        LOG.error(f"Unable to get account id")
        assert False
    client_secret = glca.create_client_credentials(page=page, creadential_name=creadential_name)
    if client_secret == None:
        LOG.error(f"Unable to generate client secret")
        assert False
    jwt_token = glca.generate_accesstoken(page=page, client_secret=client_secret, creadential_name=creadential_name)
    if jwt_token == None:
        LOG.error(f"Unable to generate access token from client secret {client_secret}")
        assert False
    decode_data = jwt.decode(jwt_token, options={"verify_signature": False})
    jwt_data = json.dumps(decode_data)
    jwt_data = json.loads(jwt_data)
    platform_customer_id = jwt_data['platform_customer_id']
    assert True if account_id == platform_customer_id else False


@pytestrail.case('C1196434')
@pytest.mark.glc_migration
def test_verify_that_the_application_launch_page_menu_will_not_have_an_option_to_remove_the_application_instance(
        plcontext
        ):
    """
    Verify that the application launch page menu will not have an option to remove the application instance
    """

    LOG.info("Log in GLCP as test user with admin role and launch GLC app")
    LOG.info(f"Users: {test_data['ADMIN_USER']}")

    page = plcontext[0].new_page()
    login = Login(test_data['ADMIN_USER'],test_data['ADMIN_PASSWORD'])
    login.go_to_home(page,test_data['GLCP_URL'],test_data['GLCP_ACCOUNTS'][0])
    page.wait_for_load_state()
    glca = GreenLakeCentralApp()
    application_name = "HPE GreenLake Central"
    application_preset = glca.check_application(page=page, application_name=application_name)
    if application_preset == False:
        LOG.error(f"Unable to see application {application_name}")
        assert False
    page.get_by_text(application_name).click()
    page.get_by_test_id("installed-app-list-action-btn").click()
    #TODO: How to find remove option here
    

@pytestrail.case('C1196436')
@pytest.mark.glc_migration
def test_verify_that_for_the_GLCP_account_without_backing_GLC_tenant_clicking_on_the_view_details_for_HPE_greenlake_central_app_will_show_the_option_to_start_test_drive(
        plcontext
        ):
    """
    Verify that for the GLCP account without backing GLC tenant, clicking on the View details for HPE greenlake central app will show the option to start test drive
    """

    LOG.info("Log in GLCP as test user with admin role and launch GLC app")
    LOG.info(f"Users: {test_data['ADMIN_USER']}")

    page = plcontext[0].new_page()
    login = Login(test_data['ADMIN_USER'],test_data['ADMIN_PASSWORD'])
    login.go_to_home(page,test_data['GLCP_URL'],test_data['GLCP_ACCOUNTS'][0])
    page.wait_for_load_state()

    glcp = GlcpBasePage(page)
    LOG.info("Clicking Switch account button")
    glcp.switch_account()
    LOG.info("Switch account button clicked")
    company_name = "HPE-Automation-{}"
    country = "United States"
    address = "CA"
    now = datetime.now()
    date_time_str = now.strftime("%Y%m%d%H%M%S")
    company_name = company_name.format(date_time_str)
    LOG.info(f"Creating new account with Company Name - {company_name}, Country - {country} and address - {address}")
    glcp.create_account(company_name=company_name, country=country, address=address)
    LOG.info(f"New account created with Company Name - {company_name}, Country - {country} and address - {address}")
    LOG.info("Clicking Application menu")

    glca = GreenLakeCentralApp()
    application_name = "HPE GreenLake Central"
    glca.navigate_to_applications_page(page=page)
    expect(page.get_by_test_id("go-avail-apps-btn").get_by_text("View Available Applications", exact=True)).to_be_visible()
    page.get_by_test_id("go-avail-apps-btn").get_by_text("View Available Applications", exact=True).click()
    page.wait_for_load_state()
    expect(page.get_by_text(text=application_name, exact=True)).to_be_visible()
    application_id = glca.get_data_test_id_from_available_applications(page=page, application_name=application_name)
    if application_id == False:
        assert False
    page.get_by_test_id(f"view-details-action-btn-{application_id}").get_by_text("View Details", exact=True).click()
    page.wait_for_load_state()
    expect(page.get_by_text(text='Start Test Drive', exact=True)).to_be_visible()

