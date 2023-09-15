import os
import sys
import json
import pytest
import logging
from automation.constants import AUTOMATION_DIRECTORY
import time
from playwright.sync_api import sync_playwright
from automation.updated_libs_local.utils import pwright_utils
from automation.updated_libs_local.authn.ui.login_to_homepage import Login
from automation.updated_libs_local.authn.ui.login_to_homepage import GLCAuthnPage

# from lib.glc.api.glc_iam_client import GlcClient
# from lib.glc.ui.authn import GLCAuthnPage
# from lib.glcp.ui.authn.authn import GLCPAuthnPage


LOG = logging.getLogger(__name__)


sys.path.append(AUTOMATION_DIRECTORY)
if os.getenv("POD_NAMESPACE") is None:
    from automation.configs.local_tb_data.polaris_settings import polaris_test_data
    from automation.configs.local_tb_data.pavo_settings import pavo_test_data
    from automation.configs.local_tb_data.aquila_settings import aquila_test_data
    from automation.configs.local_tb_data.triton_lite_settings import triton_lite_test_data
    from automation.configs.local_tb_data.gemini_settings import gemini_test_data
    from automation.configs.local_tb_data.mira_settings import mira_test_data
else:
    from automation.configs.pipeline_tb_data.polaris_settings import polaris_test_data
    from automation.configs.pipeline_tb_data.pavo_settings import pavo_test_data
    from automation.configs.pipeline_tb_data.aquila_settings import aquila_test_data
    from automation.configs.pipeline_tb_data.triton_lite_settings import triton_lite_test_data
    from automation.configs.pipeline_tb_data.gemini_settings import gemini_test_data
    from automation.configs.pipeline_tb_data.mira_settings import mira_test_data

from hpe_glcp_automation_lib.libs.commons.common_testbed_data.settings import Settings, all_envs

log = logging.getLogger(__name__)
settings = Settings()

RECORD_DIR = os.path.join('tmp', 'results')
default_env = "polaris"
ONE_MINUTE_TIMEOUT = 60000

# Argument processing need to be executed before all imports, so pytest build in will not help, it's too late.
def pytest_addoption(parser):
    parser.addoption("--env", action="store", choices=all_envs.keys(), default=default_env)

# Real command line argument parser, as a workaround for refactoring all Settings implementation
os.environ["CURRENT_ENV"] = default_env
for index, arg in enumerate(sys.argv):
    if arg.startswith("--env"):
        if "=" in arg:
            if arg.split("=")[1] in all_envs.keys():
                os.environ["CURRENT_ENV"] = arg.split("=")[1]
                break
            else:
                raise Exception(f"Unsupported environment: {arg.split('=')[1]}")
        elif sys.argv[index + 1] in all_envs.keys():
            os.environ["CURRENT_ENV"] = sys.argv[index + 1]
            break
        else:
            raise ValueError(f"Unsupported environment: {sys.argv[index + 1]}")

class CreateLogFile(object):
    """
    Usage: Create log and result file location if not exists
    From this location Job will upload all logs and results
    """
    def log_file_location(self):
        return "/tmp/results/"

    def create_log_file(self):
        try:
            if not os.path.exists("/tmp/results/"):
                os.mkdir("/tmp/results/")
            if not os.path.exists("/tmp/results/log1.log"):
                with open("/tmp/results/log1.log", "w"):
                    pass
            return True
        except:
            log.info("not able to create log file and directory")

class CertFileLocation(object):
    """
    Usage: For activate device provisioning call certs are initialized from these locations
    Certs are needed to make the device provisioning calls in test cases.
    """
    def storage_certs_files(self):
        storage_cert_data = {
            "cert": "automation/configs/certs/storage-central-cert.pem",
            "key": "automation/configs/certs/storage-central-pkey.pem",
            "ca_cert": "automation/configs/certs/device.cloud.hpe.com.pem",
        }
        return storage_cert_data

    def compute_certs_files(self):
        compute_cert_data = {
            "cert": "automation/configs/certs/compute-central-cert.pem",
            "key": "automation/configs/certs/compute-central-pkey.pem",
            "ca_cert": "automation/configs/certs/device.cloud.hpe.com.pem",
        }
        return compute_cert_data

    def iap_cert_files(self):
        iap_cert_data = {
            "cert": "automation/configs/certs/iap-pem.pem",
            "key": "automation/configs/certs/iap-key.key",
        }
        return iap_cert_data


class ExistingUserAcctDevices:
    """
    Load common test environment data from common_tb_data -> Settings, all_envs
    Load test environment data from local_tb_data or pipeline_tb_data
    """
    current_env = settings.current_env()
    login_page_url = settings.login_page_url()

    CreateLogFile = CreateLogFile()
    CertFileLocation = CertFileLocation()
    
    get_app_api_hostname = settings.get_app_api_hostname()
    hpe_device_url = settings.get_hpe_device_url()
    aruba_device_url = settings.get_aruba_device_url()
    aruba_legacy_device_url = settings.get_aruba_legacy_device_url()
    create_log_file = CreateLogFile.create_log_file()
    ccs_device_url = settings.get_ccs_device_url()
    ccs_activate_v1_device_url = settings.get_ccs_activate_v1_device_url()
    ccs_activate_v2_device_url = settings.get_ccs_activate_v2_device_url()
    log_files = CreateLogFile.log_file_location()
    storage_certs = CertFileLocation.storage_certs_files()
    compute_certs = CertFileLocation.compute_certs_files()
    iap_certs = CertFileLocation.iap_cert_files()

    if "polaris" in current_env:
        test_data = polaris_test_data(current_env)
    if "mira" in current_env:
        test_data = mira_test_data(current_env)
    if "pavo" in current_env:
        test_data = pavo_test_data(current_env)
    if current_env.startswith('common'):
        test_data = aquila_test_data(current_env)
    if current_env == "triton-lite":
        test_data = triton_lite_test_data(current_env)
    if "gemini" in current_env:
        test_data = gemini_test_data(current_env)

    # if os.getenv("POD_NAMESPACE") is None:
    #     with open(
    #             os.path.join(AUTOMATION_DIRECTORY, "configs", "local_tb_data", "user_creds.json")) as fd:
    #         s3_login_data = json.load(fd)

    # else:
    #     with open(os.path.join("/opt/ccs/sol-auto/creds/user_creds.json")) as fd:
    #         s3_login_data = json.load(fd)
    #login_data = s3_login_data[current_env]

def browser_type(playwright, browser_name: str, headed=None):
    """
    Available Browser type to be used by the test cases
    """
    if browser_name == "chromium":
        browser = playwright.chromium
        if os.getenv("POD_NAMESPACE") is None:
            return browser.launch(headless=False, slow_mo=100)
        else:
            return browser.launch(headless=True, slow_mo=100)
    if browser_name == "firefox":
        browser = playwright.firefox
        if os.getenv("POD_NAMESPACE") is None:
            return browser.launch(headless=False, slow_mo=100)
        else:
            return browser.launch(headless=True, slow_mo=100)
    if browser_name == "webkit":
        browser = playwright.webkit
        if os.getenv("POD_NAMESPACE") is None:
            return browser.launch(headless=False, slow_mo=100)
        else:
            return browser.launch(headless=True, slow_mo=100)


@pytest.fixture(scope="session")
def browser_instance(playwright):
    """
    Initialize chromium browser for test case uses
    """
    browser = browser_type(playwright, "chromium")
    yield browser
    browser.close()

active_devices = ExistingUserAcctDevices()
test_data = active_devices.test_data


@pytest.fixture
def playwright():
    with sync_playwright() as playwright_object:
        yield playwright_object


@pytest.fixture
def browser_type(playwright):
    if test_data["BROWSER_NAME"] == "chromium":
        return playwright.chromium
    if test_data["BROWSER_NAME"] == "firefox":
        return playwright.firefox
    if test_data["BROWSER_NAME"] == "webkit":
        return playwright.webkit


@pytest.fixture
def plbrowser(browser_type):
    LOG.info("Browser type %s", browser_type)
    browser_headless = test_data["BROWSER_HEADLESS"]
    browser = browser_type.launch(headless=browser_headless)
    yield browser
    browser.close()


@pytest.fixture
def plcontext(plbrowser, request ):
    test_name = request.node.originalname
    timestamp = time.strftime("%Y%m%d%H%M%S")
    context = plbrowser.new_context()
    browser_context = context
    api_context = context.request
    if test_data["TRACE_ON"]:
        context.tracing.start(
            screenshots=test_data["SCREENSHOTS"],
            snapshots=test_data["SNAPSHOTS"],
            sources=test_data["SOURCES"],
        )
    yield browser_context, api_context
    if test_data["TRACE_ON"]:
        trace_file = (
            test_data["PLAYWRIGHT_TRACE_FILE_PATH"]
            + test_name
            + "_"
            + timestamp
            + ".zip"
        )
        LOG.debug("Trace file: %s", trace_file)
        context.tracing.stop(path=trace_file)
    context.close()


@pytest.fixture
def page_context(plcontext):
    page = plcontext[0].new_page()
    yield page
    page.close()


@pytest.fixture
def login_into_glc_as_test_user(request, plcontext):
    user = request.param
    page = plcontext[0].new_page()
    page.goto(test_data["GLC_URL"])
    LOG.info(f"Users: {user['displayName']}")
    import time
    time.sleep(60)
    username = user["userName"]
    password = user["password"]
    LOG.info(f"Login in to GLC as {username}")
    login = Login(username,password)
    login.go_to_home(page,test_data['GLC_URL'],test_data['GLC_TENANTS'][0])
    yield page
    page.close()


@pytest.fixture
def login_into_glc_as_admin_user(plcontext):
    page = plcontext[0].new_page()
    page.goto(test_data["GLC_URL"])
    username = test_data["ADMIN_USER"]
    password = test_data["ADMIN_PASSWORD"]
    LOG.info(f"Login in to GLC as {username}")
    GLCAuthnPage(page).login(
        username, password
    )
    yield page
    page.close()



# @pytest.fixture
# def login_into_glc_as_test_user_no_tenant(request, plcontext, test_data):
#     page = plcontext[0].new_page()
#     page.goto(test_data["GLC_URL"])
#     user = request.param
#     LOG.info(f"Users: {user['displayName']}")
#     username = user["userName"]
#     password = user["password"]
#     LOG.info("Login in to GLC as %s", username)
#     page.wait_for_load_state("domcontentloaded")
#     GLCAuthnPage(page).login(username, password)
#     yield page
#     page.close()


@pytest.fixture
def login_into_glcp_as_admin_user(plcontext):
    page = plcontext[0].new_page()
    # page.goto(test_data["GLCP_URL"], timeout=0)
    username = test_data["ADMIN_USER"]
    password = test_data["ADMIN_PASSWORD"]
    LOG.info(f"Login in to GLCP as {username}")
    login = Login(username,password)
    login.go_to_home(page,test_data['GLCP_URL'],test_data['GLCP_ACCOUNTS'][0])
    yield page
    page.close()


# @pytest.fixture
# def login_into_glcp_as_test_user(request, plcontext, test_data):
#     page = plcontext[0].new_page()
#     page.goto(test_data["GLCP_URL"])
#     user = request.param
#     LOG.info(f"Users: {user['displayName']}")
#     username = user["userName"]
#     password = user["password"]
#     LOG.info(f"Login in to GLC as {username}")
#     GLCPAuthnPage(page).login(
#         username, password
#     )
#     yield page
#     page.close()


# @pytest.fixture
# def login_into_glcp_as_test_user_no_account(request, plcontext, test_data):
#     page = plcontext[0].new_page()
#     page.goto(test_data["GLCP_URL"])
#     user = request.param
#     LOG.info(f"Users: {user['displayName']}")
#     username = user["userName"]
#     password = user["password"]
#     LOG.info(f"Login in to GLC as {username}")
#     GLCPAuthnPage(page).login(username, password)
#     yield page
#     page.close()


@pytest.fixture
def navigate_to_glc_login_page(plcontext ):
    page = plcontext[0].new_page()
    page.goto(test_data["GLC_URL"])
    yield page
    page.close()


@pytest.fixture
def navigate_to_glcp_login_page(plcontext ):
    LOG.info("Login in to GLCP Portal")
    page = plcontext[0].new_page()
    page.goto(test_data["GLCP_URL"])
    yield page
    page.close()


# @pytest.fixture
# def glc_api_context(test_data):
#     LOG.info("Creating GLC API Context")
#     api_context = plcontext[1]
#     api_access_token = test_data["GLC_API_TOKEN"]
#     api_base_url = test_data["IAM_BASE_URL"]
#     glc_api_object = GlcClient(api_context, api_access_token, api_base_url)
#     yield glc_api_object


@pytest.fixture
def create_new_glc_user(glc_api_context ):
    users = []
    known_user_list = pwright_utils.load_json_from_file(test_data["known_glc_users"])
    for user_data in range(test_data["glc_users"]["number_of_users"]):
        user_name = test_data["glc_users"][
            "displayName"
        ] + pwright_utils.generate_random_string(5)
        user_data = {
            "spaceId": test_data["glc_users"]["spaceId"],
            "userName": user_name + "@" + test_data["glc_users"]["email_domain"],
            "displayName": user_name,
            "applicationId": test_data["glc_users"]["applicationId"],
            "givenName": user_name,
            "familyName": user_name,
        }
        response = glc_api_context.create_new_test_user(user_data)
        known_user_list.append(response)
        users.append(
            {"userName": response["userName"], "password": response["password"]}
        )
    pwright_utils.dump_json_to_file(known_user_list)
    yield users
