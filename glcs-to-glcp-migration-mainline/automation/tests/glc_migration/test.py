"""
Team: GLC Migration
Scrum Master: Sundari
Description: Test GLC migration and Launch GLC App in GLCP
"""
import logging
import pytest
import re
from datetime import datetime
import jwt
import json
import time
from pytest_pytestrail import pytestrail


from hpe_glcp_automation_lib.libs.commons.utils.aop_tokens import AOP_Token_Utils

from automation.updated_libs_local.authn.ui.base import GlcpBasePage
from automation.updated_libs_local.identity_access.users import UsersPage
from automation.updated_libs_local.usr_mgmt.glc.base import GlcBasePage
from automation.updated_libs_local.usr_mgmt.glc.user_management import UserMgmtPage
from automation.updated_libs_local.usr_mgmt.glcp.app import GreenLakeCentralApp
from automation.updated_libs_local.utils import pwright_utils
from automation.updated_libs_local.authn.ui.login_to_homepage import Login,GLCAuthnPage,GlcBasePage
from automation import conftest
from playwright.sync_api import expect,Page

LOG = logging.getLogger(__name__)

# pytestmark = [
#     pytest.mark.team_name("Sundari"),
# ]

active_devices = conftest.ExistingUserAcctDevices()
test_data = active_devices.test_data


@pytestrail.case('C1196438')
def test_invite_user_with_admin_role_glcp(
        login_into_glcp_as_admin_user
        ):
    """
    Log in GLCP as test user with admin role and launch GLC app
    """

    users = pwright_utils.load_json_from_file(test_data["KNOWN_GLC_USERS"])
    LOG.info("Log in GLCP as test user with admin role and launch GLC app")
    LOG.info(f"Users: {users[0]}")

    page = login_into_glcp_as_admin_user
    glcp = GlcpBasePage(page)
    account = glcp.current_account()
    if account is None:
        glcp.select_acct(test_data['GLCP_ACCOUNTS'][0])
        users_page = UsersPage(page)
        users_page.navigate_to_manage_users_page()
        assert users_page.invite_user(users[0]["userName"], role=test_data["GLCP_ROLES"][2])
    else:
        users_page = UsersPage(page)
        users_page.navigate_to_manage_users_page()
        assert users_page.invite_user(users[0]["userName"], role=test_data["GLCP_ROLES"][2])

@pytestrail.case('C1196439')
def test_invite_user_with_observer_role_glcp(
        login_into_glcp_as_admin_user
        ):
    """
        Invite a user with observer role in GLCP    
    """

    users = pwright_utils.load_json_from_file(test_data["KNOWN_GLC_USERS"])
    LOG.info("Invite a user with observer role in GLCP")
    LOG.info(f"Users: {users[1]}")

    page = login_into_glcp_as_admin_user
    glcp = GlcpBasePage(page)
    account = glcp.current_account()
    if account is None:
        glcp.select_acct(test_data['GLCP_ACCOUNTS'][0])
        users_page = UsersPage(page)
        users_page.navigate_to_manage_users_page()
        assert users_page.invite_user(users[1]["userName"], role=test_data["GLCP_ROLES"][1])
    else:
        users_page = UsersPage(page)
        users_page.navigate_to_manage_users_page()
        assert users_page.invite_user(users[1]["userName"], role=test_data["GLCP_ROLES"][1])

@pytestrail.case('C1196440')
def test_invite_user_with_operator_role_glcp(
        login_into_glcp_as_admin_user
        ):
    """
        Invite a user with operator role in GLCP    
    """

    users = pwright_utils.load_json_from_file(test_data["KNOWN_GLC_USERS"])
    LOG.info("Invite a user with operator role in GLCP")
    LOG.info(f"Users: {users[2]}")

    page = login_into_glcp_as_admin_user
    glcp = GlcpBasePage(page)
    account = glcp.current_account()
    if account is None:
        glcp.select_acct(test_data['GLCP_ACCOUNTS'][0])
        users_page = UsersPage(page)
        users_page.navigate_to_manage_users_page()
        assert users_page.invite_user(users[2]["userName"], role=test_data["GLCP_ROLES"][0])
    else:
        users_page = UsersPage(page)
        users_page.navigate_to_manage_users_page()
        assert users_page.invite_user(users[2]["userName"], role=test_data["GLCP_ROLES"][0])

@pytestrail.case('C1196442')
def test_login_test_user_to_glcp_as_admin_role(
        plcontext
        ):
    """
    Log in GLCP as test user with admin role and launch GLC app
    """

    users = pwright_utils.load_json_from_file(test_data["KNOWN_GLC_USERS"])
    LOG.info("Log in GLCP as test user with admin role and launch GLC app")
    LOG.info(f"Users: {users[0]}")


    page = plcontext[0].new_page()
    
    login = Login(users[0]['userName'],users[0]['password'])
    login.go_to_home(page,test_data['GLCP_URL'],test_data['GLCP_ACCOUNTS'][0])

@pytestrail.case('C1196443')
def test_login_to_glcp_using_observer_credentials(
        login_into_glcp_as_admin_user
        ):
    """
    Login to GLCP using observer credentials
    """

    users = pwright_utils.load_json_from_file(test_data["KNOWN_GLC_USERS"])
    test_user_email = users[1]["userName"]
    test_password = users[1]["password"]

    roles = test_data["GLCP_ROLES"]
    role = roles[1]

    page = login_into_glcp_as_admin_user

    
    users_page = UsersPage(page)
    users_page.navigate_to_manage_users_page()
    role_exist_flag = users_page.check_role_assigned(test_user_email, role)
    if role_exist_flag == False:
        page.click("[data-testid='user-back-btn']")
        users_page.assign_role(email_address=test_user_email, role=role)
        page.context.clear_cookies()
        login = Login(test_user_email, test_password)
        login.go_to_home(page, test_data["GLCP_URL"], test_user_email)
    else:
        page.context.clear_cookies()
        login = Login(test_user_email, test_password)
        login.go_to_home(page, test_data["GLCP_URL"], test_user_email)

@pytestrail.case('C1196444')
def test_login_to_glcp_using_operator_credentials(
        login_into_glcp_as_admin_user
        ):
    """
    Login to GLCP using operator credentials
    """

    users = pwright_utils.load_json_from_file(test_data["KNOWN_GLC_USERS"])
    test_user_email = users[2]["userName"]
    test_password = users[2]["password"]

    roles = test_data["GLCP_ROLES"]
    role = roles[0]

    page = login_into_glcp_as_admin_user

    
    users_page = UsersPage(page)
    users_page.navigate_to_manage_users_page()
    role_exist_flag = users_page.check_role_assigned(test_user_email, role)
    if role_exist_flag == False:
        users_page.assign_role(email_address=test_user_email, role=role)
        page.context.clear_cookies()
        login = Login(test_user_email, test_password)
        login.go_to_home(page, test_data["GLCP_URL"], test_user_email)
    else:
        page.context.clear_cookies()
        login = Login(test_user_email, test_password)
        login.go_to_home(page, test_data["GLCP_URL"], test_user_email)

@pytestrail.case('C1235204')
def test_login_to_glcp_user_exist_wrong_password(
        plcontext
        ):
    """
    Login to GLCP with user that exist but with wrong password.
    """

    users = pwright_utils.load_json_from_file(test_data["KNOWN_GLC_USERS"])
    LOG.info("Log in GLCP as test user with admin role and launch GLC app")
    test_user = users[0]["userName"]
    LOG.info(f"Users: Login using {test_user}")

    wrong_pass = "wrong_pass"

    page = plcontext[0].new_page()
    
    login = Login(test_user,wrong_pass)
    LOG.info("Login with user who exist in database with wrong password")
    login.wrong_password(page,test_data['GLCP_URL'])

@pytestrail.case('C1196435')
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

# @pytestrail.case('C1196436', 'C1235473')
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
    if application_id == None:
        assert False
    page.get_by_test_id(f"view-details-action-btn-{application_id}").get_by_text("View Details", exact=True).click()
    page.wait_for_load_state()
    expect(page.get_by_text(text='Start Test Drive', exact=True)).to_be_visible()

@pytestrail.case('C1196437')
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


@pytestrail.case('C1235205')
def test_login_to_glcp_user_not_exist(
        plcontext
        ):
    """
    Login to GLCP with user that doesn't exist.
    """

    wrong_username = "wrong@username.com"
    wrong_pass = "wrong_pass"

    page = plcontext[0].new_page()
    
    login = Login(wrong_username, wrong_pass)
    LOG.info("Login with user who exist in database with wrong password")
    login.wrong_user(page, test_data['GLCP_URL'])

@pytestrail.case('C1235474')
def test_validate_redirect_tenant_glcp_to_glc(
        login_into_glcp_as_admin_user
        ):
    """
        Validate we are redirecting to correct tenant from GLCP to GLC 
         
    """

    users = pwright_utils.load_json_from_file(test_data["KNOWN_GLC_USERS"])
    LOG.info("Validate we are redirecting to correct tenant from GLCP to GLC ")
    # LOG.info(f"Users: {users[1]}")
    page = login_into_glcp_as_admin_user
    
    page.get_by_test_id("text-desc-application-nav-menu").click()
    # page.locator("data-testid=text-tile-title-application-tile-59786f55-cc2a-403c-a561-db907d1203cc").locator("span",has_text='HPE GreenLake Central').first.click()
    page.get_by_text("HPE GreenLake Central", exact=True).click()
    LOG.info(f"HPE GreenLake Central is visible")
    page.wait_for_selector('data-testid=text-app-name')
    expect(page.locator("data-testid=text-app-name",has_text='HPE GreenLake Central')).to_be_visible()
    LOG.info(f"Launch button visible")
    page.locator("data-testid=launch-action-btn").first.click()
    page.wait_for_selector("h3")
    expect(page.locator("h3",has_text='Build your IT skills with HPE Education Services')).to_be_visible()

#TODO: C1238959

@pytestrail.case('C1196427')
def test_change_role_from_admin_to_operator_in_glcp(
        login_into_glcp_as_admin_user
        ):
    """
    Change Role from Observer or Operator to Administrator in GLCP
    """

    users = pwright_utils.load_json_from_file(test_data["KNOWN_GLC_USERS"])
    test_user_email = users[0]["userName"]
    test_password = users[0]["password"]

    roles = test_data["GLCP_ROLES"]
    role = roles[0]
    LOG.info(f"{role} Selected")
    page = login_into_glcp_as_admin_user

    
    users_page = UsersPage(page)
    users_page.navigate_to_manage_users_page()
    role_exist_flag = users_page.check_role_assigned(test_user_email, role)
    LOG.info(role_exist_flag)
    if role_exist_flag == False:
        page.click("[data-testid='user-back-btn']")
        users_page.assign_role(email_address=test_user_email, role=role)

    else:
        page.click("[data-testid='user-back-btn']")
        users_page.delete_role(email_address=test_user_email, role=role)
        page.click("[data-testid='user-back-btn']")
        users_page.assign_role(email_address=test_user_email, role=role)

    LOG.info(f"{role} role successfully assigned for {test_user_email}.")

    page.context.clear_cookies()
    login = Login(test_user_email, test_password)
    login.go_to_home(page, test_data["GLCP_URL"], test_user_email)

@pytestrail.case('C1196428')
def test_change_role_from_operator_to_admin_in_glcp(
        login_into_glcp_as_admin_user
        ):
    """
    Change Role from Observer or Operator to Administrator in GLCP
    """

    users = pwright_utils.load_json_from_file(test_data["KNOWN_GLC_USERS"])
    test_user_email = users[2]["userName"]
    test_password = users[2]["password"]

    roles = test_data["GLCP_ROLES"]
    role = roles[2]
    LOG.info(f"{role} Selected")
    page = login_into_glcp_as_admin_user

    
    users_page = UsersPage(page)
    users_page.navigate_to_manage_users_page()
    role_exist_flag = users_page.check_role_assigned(test_user_email, role)
    LOG.info(role_exist_flag)
    if role_exist_flag == False:
        page.click("[data-testid='user-back-btn']")
        users_page.assign_role(email_address=test_user_email, role=role)

    else:
        page.click("[data-testid='user-back-btn']")
        users_page.delete_role(email_address=test_user_email, role=role)
        page.click("[data-testid='user-back-btn']")
        users_page.assign_role(email_address=test_user_email, role=role)

    page.context.clear_cookies()
    login = Login(test_user_email, test_password)
    login.go_to_home(page, test_data["GLCP_URL"], test_user_email)

@pytestrail.case('C1196431')
def test_verify_glc_application_availability(
    plcontext
):
    """
    The test verifies whether the test user has "HPE GreenLake Central App" setup.
    """
    users = pwright_utils.load_json_from_file(test_data["KNOWN_GLC_USERS"])
    LOG.info("Log in GLCP as test user and launch GLC app")
    LOG.info(f"Users: {users[0]['displayName']}")

    page = plcontext[0].new_page()
    
    login = Login(users[0]['userName'], users[0]['password'])
    login.go_to_home(page, test_data['GLCP_URL'], test_data['GLCP_ACCOUNTS'][0])

    users_page = GreenLakeCentralApp()
    users_page.navigate_to_glcp_account(page, test_data["GLCP_ACCOUNTS"][0])
    assert users_page.check_application(page, "HPE GreenLake Central")

@pytestrail.case('C1196434')
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

@pytestrail.case('C1196445')
def test_logout_of_glc_then_login_to_glcp(
    plcontext
):
    """
    The test verifies whether the HPE GreenLake Central App is displayed under My Applications tab.
    """
    users = pwright_utils.load_json_from_file(test_data["KNOWN_GLC_USERS"])
    LOG.info("Log in GLC as admin user and invite test user.")
    LOG.info(f"Users: {users[0]['displayName']}")
    test_user_email = users[0]['userName']
    test_user_password = users[0]['password']
    
    page = plcontext[0].new_page()
    
    # login = Login(test_user_email, test_user_password)
    # login.go_to_home(page, test_data['GLC_URL'], test_data['GLC_TENANTS'][0])

    page.goto(test_data["GLC_URL"], timeout=0)
    GLCAuthnPage(page).login(test_user_email, test_user_password)

    user_glc_page = UserMgmtPage()

    page.wait_for_load_state()
    # user_glc_page.navigate_to_glc_tennant(page, test_data['GLC_TENANTS'][0])

    user_glc_page.signout(page)
    page.wait_for_load_state()
    expect(page).to_have_url(re.compile("sign-out-complete"), timeout=30000)

    page.context.clear_cookies()

    login = Login(test_user_email, test_user_password)
    login.go_to_home(page, test_data['GLCP_URL'], test_data['GLCP_ACCOUNTS'][0])

    user_glcp_page = GreenLakeCentralApp()

    user_glcp_page.navigate_to_glcp_account(page, test_data["GLCP_ACCOUNTS"][0])

@pytestrail.case('C1196441')
def test_invite_user_from_glc_to_glcp(
    plcontext
    ):
    """
    The test checks the whether a user invited from GLC to GLCP lands on the same tenant.
    """
    users = pwright_utils.load_json_from_file(test_data["KNOWN_GLC_USERS"])
    LOG.info("Log in GLC as admin user and invite test user.")
    LOG.info(f"Users: {users[3]['displayName']}")

    test_user_email = users[3]["userName"]
    test_user_password = users[3]["password"]
    first_name = users[3]["name"]["givenName"]
    last_name = users[3]["name"]["familyName"]

    page = plcontext[0].new_page()

    page.goto(test_data["GLC_URL"], timeout=0)
    page.wait_for_load_state()
    GLCAuthnPage(page).login(test_data["ADMIN_USER"], test_data["ADMIN_PASSWORD"])
    LOG.info(f"Users: {users[3]['displayName']}")

    user_page = UserMgmtPage()

    page.wait_for_load_state()
    user_page.navigate_to_glc_tennant(page, test_data['GLC_TENANTS'][0])
    user_page.open(page)

    if not user_page.check_user(page, test_user_email):
        user_page.invite_user(page,
            firstname=first_name, lastname=last_name, email_address=test_user_email
        )
        LOG.info(f"Invitation sent to {test_user_email}")
    else:
        LOG.info(f"{test_user_email} already invited.")

    user_page.signout(page)
    page.wait_for_load_state()
    expect(page).to_have_url(re.compile("sign-out-complete"), timeout=30000)

    page.context.clear_cookies()
    page.wait_for_load_state()

    # login = Login(test_user_email, test_user_password)
    # login.go_to_home(page, test_data['GLC_URL'], test_data['GLC_TENANTS'][0])

    page.goto(test_data["GLC_URL"], timeout=0)
    page.wait_for_load_state()
    GLCAuthnPage(page).login(test_user_email, test_user_password)

    invited_user_page = UserMgmtPage()

    assert invited_user_page.verify_useremail_and_tenant_in_glc(
        page, test_user_email, test_data["GLC_TENANTS"][0]
    )

    invited_user_page.signout(page)
    page.wait_for_load_state()
    expect(page).to_have_url(re.compile("sign-out-complete"), timeout=30000)

    page.context.clear_cookies()

    page.goto(test_data["GLCP_URL"], timeout=0)
    login = Login(test_user_email, test_user_password)
    login.go_to_home(page, test_data['GLCP_URL'], test_data['GLCP_ACCOUNTS'][0])

    invited_user_glcp_page = GreenLakeCentralApp()
    invited_user_glcp_page.navigate_to_glcp_account(page, test_data["GLCP_ACCOUNTS"][0])

    invited_user_glcp_page.navigate_to_applications_page(page)
    invited_user_glcp_page.launch_glc_app(page)

    expect(page).to_have_url(re.compile(test_data["GLC_URL"]), timeout=30000)

    assert invited_user_glcp_page.verify_useremail_and_tenant_in_glc(
        page, test_user_email, test_data["GLC_TENANTS"][0]
    )

@pytestrail.case('C1196430')
def test_remove_iam_owner_in_glc_for_glcp_admin(
    plcontext
):
    """
    The test checks the removal of IAM ownership in GLC for a GLCP admin test user.
    """
    users = pwright_utils.load_json_from_file(test_data["KNOWN_GLC_USERS"])
    LOG.info("Log in GLC as admin user and invite test user.")
    LOG.info(f"Users: {users[0]['displayName']}")

    test_user_email = users[0]["userName"]
    test_user_password = users[0]["password"]

    page = plcontext[0].new_page()
    
    # login = Login(users[0]['userName'], users[0]['password'])
    # login = Login(test_data["ADMIN_USER"], test_data["ADMIN_PASSWORD"])
    # login.go_to_home(page, test_data['GLC_URL'], test_data['GLC_TENANTS'][0])

    page.goto(test_data["GLC_URL"], timeout=0)
    page.wait_for_load_state()
    GLCAuthnPage(page).login(test_data["ADMIN_USER"], test_data["ADMIN_PASSWORD"])

    user_page = UserMgmtPage()
    user_page.navigate_to_glc_tennant(page, test_data['GLC_TENANTS'][0])
    page.wait_for_load_state()
    user_page.open(page)

    if not user_page.check_assignment(page, test_user_email, test_data["GLC_ROLES"][0]):
        user_page.create_assignment(page, test_user_email, test_data["GLC_ROLES"][0])

    if user_page.check_assignment(page, test_user_email, test_data["GLC_ROLES"][0]):
        user_page.delete_assignment(page, test_user_email, test_data["GLC_ROLES"][0])

    user_page.signout(page)
    page.wait_for_load_state()
    expect(page).to_have_url(re.compile("sign-out-complete"), timeout=0)

    page.context.clear_cookies()
    page.wait_for_load_state()

    page.goto(test_data["GLC_URL"], timeout=0)
    login = Login(test_user_email, test_user_password)
    login.go_to_home(page, test_data['GLCP_URL'], test_data['GLCP_ACCOUNTS'][0])
    test_user_page = GreenLakeCentralApp()

    # test_user_page.navigate_to_glcp_account(page, test_data["GLCP_ACCOUNTS"][0])

    test_user_page.navigate_to_applications_page(page)
    test_user_page.launch_glc_app(page)

    expect(page).to_have_url(re.compile(test_data["GLC_URL"]), timeout=30000)
    
    assert test_user_page.verify_useremail_and_tenant_in_glc(
        page, test_user_email, test_data["GLC_TENANTS"][0]
    )

@pytestrail.case('C1196446')
def test_login_to_glc_using_direct_link(
        plcontext
        ):
    """
    Login to GLC with direct link
    """

    users = pwright_utils.load_json_from_file(test_data["KNOWN_GLC_USERS"])
    test_user = users[3]["userName"]
    test_pass = users[3]["password"]

    page = plcontext[0].new_page()
    
    page.goto(test_data["GLC_URL"], timeout=0)
    glc_auth_page = GLCAuthnPage(page)

    LOG.info("Login using GLC direct link")
    glc_auth_page.login(test_user, test_pass)

@pytestrail.case('C1196450')
def test_delete_a_user_glcp(
        login_into_glcp_as_admin_user
        ):
    """
        Delete a user from GLCP
    """

    users = pwright_utils.load_json_from_file(test_data["KNOWN_GLC_USERS"])
    LOG.info("Delete a user from GLCPP")
    LOG.info(f"Users: {users[2]}")

    page = login_into_glcp_as_admin_user

    
    glcp = GlcpBasePage(page)
    account = glcp.current_account()
    if account is None:
        glcp.select_acct(test_data['GLCP_ACCOUNTS'][0])
        users_page = UsersPage(page)
        users_page.navigate_to_manage_users_page()
        users_page.delete_user(users[2]["userName"])
    else:
        users_page = UsersPage(page)
        users_page.navigate_to_manage_users_page()
        users_page.delete_user(users[2]["userName"])

@pytestrail.case('C1196449')
def test_suspend_user_from_glcs(
    plcontext
):
    """
    The test suspends the GLCS user from GLCP.
    """
    users = pwright_utils.load_json_from_file(test_data["KNOWN_GLC_USERS"])
    LOG.info("Log in GLC as admin user and invite test user.")
    LOG.info(f"Users: {users[1]['displayName']}")

    test_user_email = users[1]["userName"]

    page = plcontext[0].new_page()
    
    login = Login(test_data["ADMIN_USER"], test_data["ADMIN_PASSWORD"])
    login.go_to_home(page, test_data['GLCP_URL'], test_data['GLCP_ACCOUNTS'][0])

    users_page = GreenLakeCentralApp()

    users_page.navigate_to_glcp_account(page, test_data["GLCP_ACCOUNTS"][0])
    if users_page.check_application(page, "HPE GreenLake Central"):
        LOG.info(f"HPE GreenLake Central application is present.")

    users_page.launch_glc_app(page)

    expect(page).to_have_url(re.compile(test_data["GLC_URL"]), timeout=30000)

    if users_page.verify_useremail_and_tenant_in_glc(page, test_data["ADMIN_USER"], test_data["GLC_TENANTS"][0]):
        LOG.info(f"{test_data['ADMIN_USER']} migrated to proper tenant.")

    users_management_page = UserMgmtPage()

    page.wait_for_load_state()
    assert users_management_page.suspend_user(page, test_user_email)

@pytestrail.case('C1196448')
def test_uninvite_user_from_glcs(
    plcontext
):
    """
    The test suspends the GLCS user from GLCP.
    """
    users = pwright_utils.load_json_from_file(test_data["KNOWN_GLC_USERS"])
    LOG.info("Log in GLC as admin user and invite test user.")
    LOG.info(f"Users: {users[3]['displayName']}")

    test_user_email = users[3]["userName"]

    page = plcontext[0].new_page()
    
    login = Login(test_data["ADMIN_USER"], test_data["ADMIN_PASSWORD"])
    login.go_to_home(page, test_data['GLCP_URL'], test_data['GLCP_ACCOUNTS'][0])

    users_page = GreenLakeCentralApp()

    users_page.navigate_to_glcp_account(page, test_data["GLCP_ACCOUNTS"][0])
    if users_page.check_application(page, "HPE GreenLake Central"):
        LOG.info(f"HPE GreenLake Central application is present.")

    users_page.launch_glc_app(page)

    expect(page).to_have_url(re.compile(test_data["GLC_URL"]), timeout=30000)

    if users_page.verify_useremail_and_tenant_in_glc(page, test_data["ADMIN_USER"], test_data["GLC_TENANTS"][0]):
        LOG.info(f"{test_data['ADMIN_USER']} migrated to proper tenant.")

    users_management_page = UserMgmtPage()

    page.wait_for_load_state()
    assert users_management_page.uninvite_user(page, test_user_email)


@pytestrail.case('C1196447')
def test_uninvite_user_from_glcs_not_verified_in_glcp(
        login_into_glcp_as_admin_user
        ):
    """
    uninvite a user from GLCS who never verified in GLCP
    """

    users = pwright_utils.load_json_from_file(test_data["KNOWN_GLC_USERS"])
    test_user_email = users[0]["userName"]

    page = login_into_glcp_as_admin_user

    
    users_page = UsersPage(page)
    users_page.navigate_to_manage_users_page()
    users_page.search_user(test_user_email)
    status = users_page.get_status()
    assert status == 'Verified'
    LOG.info(f"{test_user_email} has status {status}")

    glc_page = GreenLakeCentralApp()
    glc_page.launch_glc_app(page)
    glc_users_page = UserMgmtPage()
    glc_users_page.uninvite_user(page, test_user_email)

    LOG.info(f"{test_user_email} has been uninvited.")
