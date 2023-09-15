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
from pytest_testrail.plugin import pytestrail



from hpe_glcp_automation_lib.libs.commons.utils.aop_tokens import AOP_Token_Utils

from automation.libs_local.authn.ui.base import GlcpBasePage
from automation.libs_local.identity_access.users import UsersPage
from automation.libs_local.utils import pwright_utils
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