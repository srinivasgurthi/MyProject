"""
Team: GLC Migration
Scrum Master: Sundari
Description: Remove assignment of IAM owner in GLC for a GLCP admin.
"""

import logging
import re

import pytest
from automation import conftest
from playwright.sync_api import expect
from pytest_pytestrail import pytestrail 
from automation.updated_libs_local.authn.ui.login_to_homepage import Login, GLCAuthnPage
from automation.updated_libs_local.usr_mgmt.glc.user_management import UserMgmtPage
from automation.updated_libs_local.usr_mgmt.glcp.app import GreenLakeCentralApp
from automation.updated_libs_local.utils import pwright_utils

LOG = logging.getLogger(__name__)

pytestmark = [
    pytest.mark.team_name("Sundari")
]

active_devices = conftest.ExistingUserAcctDevices()
test_data = active_devices.test_data


@pytestrail.case('C1196430')
@pytest.mark.glc_migration
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

    page.goto(test_data["GLC_URL"])
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
    expect(page).to_have_url(re.compile("sign-out-complete"), timeout=30000)

    page.context.clear_cookies()
    page.wait_for_load_state()

    page.goto(test_data["GLC_URL"])
    login = Login(test_user_email, test_user_password)
    login.go_to_home(page, test_data['GLCP_URL'], test_data['GLCP_ACCOUNTS'][0])

    test_user_page = GreenLakeCentralApp()

    test_user_page.navigate_to_glcp_account(page, test_data["GLCP_ACCOUNTS"][0])

    test_user_page.navigate_to_applications_page(page)
    test_user_page.launch_glc_app(page)

    expect(page).to_have_url(re.compile(test_data["GLC_URL"]), timeout=30000)
    
    assert test_user_page.verify_useremail_and_tenant_in_glc(
        page, test_user_email, test_data["GLC_TENANTS"][0]
    )





@pytestrail.case('C1196431')
@pytest.mark.glc_migration
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





@pytestrail.case('C1196441')
@pytest.mark.glc_migration
def test_invite_user_from_glc_to_glcp(
    plcontext
    ):
    """
    The test checks the whether a user invited from GLC to GLCP lands on the same tenant.
    """
    users = pwright_utils.load_json_from_file(test_data["KNOWN_GLC_USERS"])
    LOG.info("Log in GLC as admin user and invite test user.")
    LOG.info(f"Users: {users[0]['displayName']}")

    test_user_email = users[0]["userName"]
    test_user_password = users[0]["password"]
    first_name = users[0]["name"]["givenName"]
    last_name = users[0]["name"]["familyName"]

    page = plcontext[0].new_page()
    # login = Login(users[0]['userName'], users[0]['password'])
    # login = Login(test_data["ADMIN_USER"], test_data["ADMIN_PASSWORD"])
    # login.go_to_home(page, test_data['GLC_URL'], test_data['GLC_TENANTS'][0])
    
    page.goto(test_data["GLC_URL"])
    page.wait_for_load_state()
    GLCAuthnPage(page).login(test_data["ADMIN_USER"], test_data["ADMIN_PASSWORD"])

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

    page.goto(test_data["GLC_URL"])
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

    page.goto(test_data["GLCP_URL"])
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




@pytestrail.case('C1196445')
@pytest.mark.glc_migration
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

    page.goto(test_data["GLC_URL"])
    page.wait_for_load_state()
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





@pytestrail.case('C1196448')
@pytest.mark.glc_migration
def test_uninvite_user_from_glcs(
    plcontext
):
    """
    The test suspends the GLCS user from GLCP.
    """
    users = pwright_utils.load_json_from_file(test_data["KNOWN_GLC_USERS"])
    LOG.info("Log in GLC as admin user and invite test user.")
    LOG.info(f"Users: {users[0]['displayName']}")

    test_user_email = users[0]["userName"]

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
    #assert users_management_page.uninvite_user(page, test_user_email)




@pytestrail.case('C1196449')
@pytest.mark.glc_migration
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




@pytestrail.case('C1235473')
@pytest.mark.glc_migration
def test_verify_glc_application_start_button(
    plcontext
):
    """
    The test verifies whether the HPE GreenLake Central App is displayed under My Applications tab.
    """
    users = pwright_utils.load_json_from_file(test_data["KNOWN_GLC_USERS"])
    LOG.info("Log in GLC as admin user and invite test user.")
    LOG.info(f"Users: {users[1]['displayName']}")

    page = plcontext[0].new_page()
    login = Login(users[1]['userName'], users[1]['password'])
    login.go_to_home(page, test_data['GLCP_URL'], test_data['GLCP_ACCOUNTS'][0])

    users_page = GreenLakeCentralApp()
    users_page.navigate_to_glcp_account(page, test_data["GLCP_ACCOUNTS"][0])
    assert users_page.check_application(page, "HPE GreenLake Central")
