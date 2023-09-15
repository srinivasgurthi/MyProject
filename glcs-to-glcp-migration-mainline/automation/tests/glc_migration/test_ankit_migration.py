"""
Team: GLC Migration
Scrum Master: Sundari
Description: Test GLC migration and Launch GLC App in GLCP
"""
import logging
import pytest

from pytest_pytestrail import pytestrail

from automation.updated_libs_local.utils import pwright_utils
from automation.updated_libs_local.authn.ui.login_to_homepage import Login, GLCAuthnPage
from automation.updated_libs_local.identity_access.users import UsersPage
from automation.updated_libs_local.usr_mgmt.glcp.app import GreenLakeCentralApp
from automation.updated_libs_local.usr_mgmt.glc.user_management import UserMgmtPage
from automation import conftest


LOG = logging.getLogger(__name__)

pytestmark = [
    pytest.mark.team_name("Sundari"),
]

active_devices = conftest.ExistingUserAcctDevices()
test_data = active_devices.test_data


@pytestrail.case('C1196442')
@pytest.mark.glc_migration
def test_login_to_glcp_as_admin_credentials(
        plcontext
        ):
    """
    login to glcp with administrator credentials
    """

    page = plcontext[0].new_page()
    login = Login(test_data["ADMIN_USER"],test_data["ADMIN_PASSWORD"])
    LOG.info("Login Using administrator credentials")
    login.go_to_home(page,test_data['GLCP_URL'],test_data['ADMIN_USER'])

@pytestrail.case('C1235204')
@pytest.mark.glc_migration
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


@pytestrail.case('C1235205')
@pytest.mark.glc_migration
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


@pytestrail.case('C1196446')
@pytest.mark.glc_migration
def test_login_to_glc_using_direct_link(
        plcontext
        ):
    """
    Login to GLC with direct link
    """

    users = pwright_utils.load_json_from_file(test_data["KNOWN_GLC_USERS"])
    test_user = users[0]["userName"]
    test_pass = users[0]["password"]

    page = plcontext[0].new_page()
    page.goto(test_data["GLC_URL"])
    glc_auth_page = GLCAuthnPage(page)

    LOG.info("Login using GLC direct link")
    glc_auth_page.login(test_user, test_pass)


@pytestrail.case('C1196444')
@pytest.mark.glc_migration
def test_login_to_glcp_using_operator_credentials(
        login_into_glcp_as_admin_user
        ):
    """
    Login to GLCP using operator credentials
    """

    users = pwright_utils.load_json_from_file(test_data["KNOWN_GLC_USERS"])
    test_user_email = users[0]["userName"]
    test_password = users[0]["password"]

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




@pytestrail.case('C1196428')
@pytest.mark.glc_migration
def test_change_role_from_operator_to_admin_in_glcp(
        login_into_glcp_as_admin_user
        ):
    """
    Change Role from Operator to Administrator in GLCP
    """

    users = pwright_utils.load_json_from_file(test_data["KNOWN_GLC_USERS"])
    test_user_email = users[0]["userName"]
    test_password = users[0]["password"]

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
        users_page.delete_recursive_role(email_address=test_user_email, role=role)
        page.click("[data-testid='user-back-btn']")
        users_page.assign_role(email_address=test_user_email, role=role)

    page.context.clear_cookies()
    login = Login(test_user_email, test_password)
    login.go_to_home(page, test_data["GLCP_URL"], test_user_email)


@pytestrail.case('C1196427')
@pytest.mark.glc_migration
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


@pytestrail.case('C1196447')
@pytest.mark.glc_migration
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


