import os
import uuid

def pavo_test_data(url):
    """
    Usage: Test bed data will be initialized in conftest.py
    define username, acct_name, app_name, device serials, subscriptions in this file
    Password and api_secret need to be in user_creds.json file
    """
    tb_data = {}
    tb_data["test_or_workflow_name1"] = {}
    tb_data["test_or_workflow_name2"] = {}
    if "pavo" in url:
        tb_data["url"] = url
        tb_data["test_or_workflow_name1"]["username"] = "username"
        tb_data["test_or_workflow_name1"]["account_name1"] = "account_name1"
        tb_data["test_or_workflow_name1"]["app_api_user"] = "_api"


        # new params
        tb_data["GLCP_URL"] = "https://pavo.common.cloud.hpe.com"

        tb_data["ADMIN_USER"] = os.environ.get("ADMIN_USER")
        tb_data["ADMIN_PASSWORD"] = os.environ.get("ADMIN_PASSWORD")
        tb_data["GLCP_ACCOUNTS"] = ["GLCP Solution Testing 20230222"]
        tb_data["GLC_TENANTS"] = ["GLCP Solution Testing 20230222"]

        tb_data["GLC_URL"] = "https://client.greenlake.hpe-gl-intg.com/"
        tb_data["KNOWN_GLC_USERS"] = os.environ.get("KNOWN_GLC_USERS")  # this JSON file contains existing or known users created in previous test runs.
        tb_data["GLC_API_TOKEN"] = os.environ.get("GLC_API_TOKEN")
        tb_data["IAM_BASE_URL"] = "https://iam.intg.hpedevops.net"
        tb_data["CREATE_GLC_USERS"] = {
            "number_of_users": 1,
            "spaceId": "2b27e55e-0388-42a9-a531-76f828b65f2d",
            "applicationId": "APP000114",
            "displayName": "glc_migration_testuser",
            "email_domain": "test.glc.hpe.com"
        }


        tb_data["GLCP_ROLES"] = ["Operator Built-in", "Observer Built-in", "Account Administrator Built-in"]
        tb_data["GLC_ROLES"] = ["IAM Owner"]
        tb_data["GLC_SPACES"] = ["Default"]
        tb_data["HPE_GREENLAKE_APPLICATION_ID"] = "59786f55-cc2a-403c-a561-db907d1203cc"
        tb_data["GLCP_ACCOUNT_NAME"] = f"GLCP-Testing-{uuid.uuid1()}"


        # playwright trace files
        tb_data["PLAYWRIGHT_TRACE_FILE_PATH"] = "/tmp/trace_files"
        tb_data["BROWSER_HEADLESS"] = False
        tb_data["BROWSER_NAME"] = "chromium"
        tb_data["SCREENSHOTS"] = True
        tb_data["SNAPSHOTS"] = True
        tb_data["SOURCES"] = True
        tb_data["TRACE_ON"] = True
        
        return tb_data




