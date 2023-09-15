import json
import logging
import os
import shutil
from logging import DEBUG
import ldclient
from ldclient.config import Config
from hpe_glcp_automation_lib.libs.commons.utils.s3.s3_download import download_file

log = logging.getLogger(__name__)

"""
Usage:
Settings.current_env = To find out the cluster under test when running local laptop or in k8s env
Settings.login_page_url: To find the login page url
Settings.get_app_api_hostname: To find the app_api_hostname
Settings.get_device_urls: Used for device provisioning test cases,
test bed specific urls for devices are in test case repository
"""

CLUSTER_INFO_FILE = "/configmap/data/infra_clusterinfo.json"

all_envs = {
    "mira": {
        "login_page": "https://mira.ccs.arubathena.com",
        "auth_url": "https://auth-itg.hpe.com",
        "sso_host": "qa-sso.ccs.arubathena.com",
        "app_api_hostname": "mira-default-app-api.ccs.arubathena.com",
        "user_api_hostname": "mira-default-user-api.ccs.arubathena.com",
        "ext_api_hostname": "mira-default-ext-api-api.ccs.arubathena.com",
        "org_api_hostname": "mira-default-org-api.ccs.arubathena.com",
        "ccs_device_cloud_url": "mira-device.ccs.arubathena.com",
        "ccs_activate_v1_device_url": "mira-activate-v1-device.ccs.arubathena.com",
        "ccs_activate_v2_device_url": "mira-activate-v2-device.ccs.arubathena.com",
        "hpe_device_cloud_url": "device.cloud.hpe.com",
        "aruba_device_v2_url": "devices-v2.arubanetworks.com",
        "aruba_device_v1_url": "device.arubanetworks.com",
        "aruba_legacy_activate_url": "activate.arubanetworks.com",
        "est_url": ""
    },
    "mira-r": {
        "login_page": "https://mira.ccs.arubathena.com",
        "auth_url": "https://auth-itg.hpe.com",
        "sso_host": "qa-sso.ccs.arubathena.com",
        "app_api_hostname": "mira-default-app-api-r.ccs.arubathena.com",
        "user_api_hostname": "mira-default-user-api-r.ccs.arubathena.com",
        "ext_api_hostname": "mira-default-ext-api-api-r.ccs.arubathena.com",
        "org_api_hostname": "mira-default-org-api-r.ccs.arubathena.com",
        "ccs_device_cloud_url": "mira-device-r.ccs.arubathena.com",
        "ccs_activate_v1_device_url": "mira-activate-v1-device-r.ccs.arubathena.com",
        "ccs_activate_v2_device_url": "mira-activate-v2-device-r.ccs.arubathena.com",
        "hpe_device_cloud_url": "device.cloud.hpe.com",
        "aruba_device_v2_url": "devices-v2.arubanetworks.com",
        "aruba_device_v1_url": "device.arubanetworks.com",
        "aruba_legacy_activate_url": "activate.arubanetworks.com",
        "est_url": ""
    },
    "polaris": {
        "login_page": "https://polaris.ccs.arubathena.com",
        "auth_url": "https://auth-itg.hpe.com",
        "sso_host": "qa-sso.ccs.arubathena.com",
        "app_api_hostname": "polaris-default-app-api.ccs.arubathena.com",
        "user_api_hostname": "polaris-default-user-api.ccs.arubathena.com",
        "ext_api_hostname": "polaris-default-ext-api-api.ccs.arubathena.com",
        "org_api_hostname": "polaris-default-org-api.ccs.arubathena.com",
        "ccs_device_cloud_url": "polaris-device.ccs.arubathena.com",
        "ccs_activate_v1_device_url": "polaris-activate-v1-device.ccs.arubathena.com",
        "ccs_activate_v2_device_url": "polaris-activate-v2-device.ccs.arubathena.com",
        "hpe_device_cloud_url": "device.cloud.hpe.com",
        "aruba_device_v2_url": "devices-v2.arubanetworks.com",
        "aruba_device_v1_url": "device.arubanetworks.com",
        "aruba_legacy_activate_url": "activate.arubanetworks.com",
        "est_url": ""
    },
    "gemini": {
        "login_page": "https://gemini.ccs.arubathena.com",
        "auth_url": "https://auth-itg.hpe.com",
        "sso_host": "qa-sso.ccs.arubathena.com",
        "app_api_hostname": "gemini-default-app-api.ccs.arubathena.com",
        "user_api_hostname": "gemini-default-user-api.ccs.arubathena.com",
        "ext_api_hostname": "gemini-default-ext-api.ccs.arubathena.com",
        "org_api_hostname": "gemini-default-org-api.ccs.arubathena.com",
        "ccs_device_cloud_url": "gemini-device.ccs.arubathena.com",
        "ccs_activate_device_url": "gemini-default-activate.device.ccs.arubathena.com",
        "ccs_activate_v1_device_url": "gemini-default-activate-v1-device.ccs.arubathena.com",
        "ccs_activate_v2_device_url": "gemini-default-activate-v2-device.ccs.arubathena.com",
        "hpe_device_cloud_url": "device.cloud.hpe.com",
        "aruba_device_v2_url": "devices-v2.arubanetworks.com",
        "aruba_device_v1_url": "device.arubanetworks.com",
        "aruba_legacy_activate_url": "activate.arubanetworks.com",
        "est_url": ""
    },
    "triton-lite": {
        "login_page": "https://triton-lite.ccs.arubathena.com",
        "auth_url": "https://auth-itg.hpe.com",
        "sso_host": "qa-sso.ccs.arubathena.com",
        "app_api_hostname": "triton-lite-app-api.ccs.arubathena.com",
        "user_api_hostname": "triton-lite-user-api.ccs.arubathena.com",
        "ext_api_hostname": "triton-lite-ext-api-api.ccs.arubathena.com",
        "org_api_hostname": "triton-lite--org-api.ccs.arubathena.com",
        "ccs_device_cloud_url": "triton-lite-device.ccs.arubathena.com",
        "ccs_activate_v1_device_url": "triton-lite-activate-v1-device.ccs.arubathena.com",
        "ccs_activate_v2_device_url": "triton-lite-activate-v2-device.ccs.arubathena.com",
        "hpe_device_cloud_url": "device.cloud.hpe.com",
        "aruba_device_v2_url": "devices-v2.arubanetworks.com",
        "aruba_device_v1_url": "device.arubanetworks.com",
        "aruba_legacy_activate_url": "activate.arubanetworks.com",
        "est_url": ""
    },
    "hoku": {
        "login_page": "https://hoku.ccs.arubathena.com",
        "auth_url": "https://auth-itg.hpe.com",
        "sso_host": "qa-sso.ccs.arubathena.com",
        "app_api_hostname": "hoku-app.ccs.arubathena.com",
        "user_api_hostname": "hoku-user.ccs.arubathena.com",
        "ext_api_hostname": "hoku-ext-api-api.ccs.arubathena.com",
        "org_api_hostname": "hoku-org-api.ccs.arubathena.com",
        "ccs_device_cloud_url": "hoku-device.ccs.arubathena.com",
        "ccs_activate_v1_device_url": "hoku-activate-v1-device.ccs.arubathena.com",
        "ccs_activate_v2_device_url": "hoku-activate-v2-device.ccs.arubathena.com",
        "hpe_device_cloud_url": "device.cloud.hpe.com",
        "aruba_device_v2_url": "devices-v2.arubanetworks.com",
        "aruba_device_v1_url": "device.arubanetworks.com",
        "aruba_legacy_activate_url": "activate.arubanetworks.com",
        "est_url": ""
    },
    "triton": {
        "login_page": "https://triton.ccs.arubathena.com",
        "auth_url": "https://auth-itg.hpe.com",
        "sso_host": "qa-sso.ccs.arubathena.com",
        "app_api_hostname": "triton-default-app-api.ccs.arubathena.com",
        "user_api_hostname": "triton-default-user-api.ccs.arubathena.com",
        "ext_api_hostname": "triton-default-ext-api-api.ccs.arubathena.com",
        "org_api_hostname": "triton-default-org-api.ccs.arubathena.com",
        "ccs_device_cloud_url": "triton-device.ccs.arubathena.com",
        "ccs_activate_v1_device_url": "triton-activate-v1-device.ccs.arubathena.com",
        "ccs_activate_v2_device_url": "triton-activate-v2-device.ccs.arubathena.com",
        "hpe_device_cloud_url": "device.cloud.hpe.com",
        "aruba_device_url": "devices-v2.arubanetworks.com",
        "aruba_legacy_device_url": "device.arubanetworks.com",
        "aruba_legacy_activate_url": "activate.arubanetworks.com",
        "aruba_device_v2_url": "devices-v2.arubanetworks.com",
        "aruba_device_v1_url": "device.arubanetworks.com",
        "est_url": ""
    },
    "pavo": {
        "login_page": "https://pavo.common.cloud.hpe.com",
        "auth_url": "https://auth-itg.hpe.com",
        "sso_host": "sso.common.cloud.hpe.com",
        "app_api_hostname": "pavo-app-api.common.cloud.hpe.com",
        "user_api_hostname": "pavo-user-api.common.cloud.hpe.com",
        "ext_api_hostname": "pavo-default-ext-api.common.cloud.hpe.com",
        "org_api_hostname": "pavo-default-org-api.common.cloud.hpe.com",
        "ccs_device_cloud_url": "pavo-device.common.cloud.hpe.com",
        "ccs_activate_v1_device_url": "pavo-activate-v1-device.common.cloud.hpe.com",
        "ccs_activate_v2_device_url": "pavo-activate-v2-device.common.cloud.hpe.com",
        "hpe_device_cloud_url": "device.cloud.hpe.com",
        "aruba_device_v2_url": "devices-v2.arubanetworks.com",
        "aruba_device_v1_url": "device.arubanetworks.com",
        "aruba_legacy_activate_url": "activate.arubanetworks.com",
        "est_url": "qa-est.arubanetworks.com"
    },
    "aquila": {
        "login_page": "https://common.cloud.hpe.com",
        "auth_url": "https://auth.hpe.com",
        "sso_host": "sso.common.cloud.hpe.com",
        "app_api_hostname": "aquila-app-api.common.cloud.hpe.com",
        "user_api_hostname": "aquila-user-api.common.cloud.hpe.com",
        "ext_api_hostname": "aquila-default-ext-api.common.cloud.hpe.com",
        "org_api_hostname": "aquila-default-org-api.common.cloud.hpe.com",
        "ccs_device_cloud_url": "aquila-device.common.cloud.hpe.com",
        "ccs_activate_device_url": "aquila-activate.device.common.cloud.hpe.com",
        "ccs_activate_v1_device_url": "aquila-activate-v1-device.common.cloud.hpe.com",
        "ccs_activate_v2_device_url": "aquila-activate-v2-device.common.cloud.hpe.com",
        "hpe_device_cloud_url": "device.cloud.hpe.com",
        "aruba_device_v2_url": "devices-v2.arubanetworks.com",
        "aruba_device_v1_url": "device.arubanetworks.com",
        "aruba_legacy_activate_url": "activate.arubanetworks.com",
        "est_url": "est.arubanetworks.com"
    }
}


humio_env = {
    "mira-us-west-2": {
        "humio_url": "https://mira-us-west-2.cloudops.ccs.arubathena.com/logs",
        "humio_repository": "ccsportal"
    },
    "mira-us-east-2": {
    "humio_url": "https://mira-us-east-2.cloudops.ccs.arubathena.com/logs",
    "humio_repository": "ccsportal"
    },
    "polaris-us-west-2": {
        "humio_url": "https://polaris-us-west-2.cloudops.ccs.arubathena.com/logs",
        "humio_repository": "ccsportal"
    },
    "triton-us-west-2": {
        "humio_url": "https://triton-us-west-2.cloudops.ccs.arubathena.com/logs",
        "humio_repository": "ccsportal"
    },
    "triton-lite": {
        "humio_url": "https://triton-us-west-2.cloudops.ccs.arubathena.com/logs",
        "humio_repository": "ccsportal"
    },
    "pavo-us-west-2": {
        "humio_url": "https://pavo-us-west-2.cloudops.common.cloud.hpe.com/logs/ccsportal",
        "humio_repository": "ccsportal"
    },
    "pavo-us-east-2": {
        "humio_url": "https://pavo-us-east-2.cloudops.common.cloud.hpe.com/logs/ccsportal",
        "humio_repository": "ccsportal"
    },
    "aquil-us-west-2": {
        "humio_url": "https://aquila-us-west-2.cloudops.common.cloud.hpe.com/logs/ccsportal",
        "humio_repository": "ccsportal"
    },
    "aquila-us-east-2": {
        "humio_url": "https://aquila-us-east-2.cloudops.common.cloud.hpe.com/logs/ccsportal",
        "humio_repository": "ccsportal"
    }
}

class Settings:
    """
    Settings should be loaded in pytest conftest.py for test cases usage
    """

    pod_namespace: str = ""
    log_level = DEBUG

    def __init__(self):
        pass

    def get_all_urls(self):
        return all_envs[self.current_env()]

    def login_page_url(self):
        log.info(f'login_page_url under test: {all_envs[self.current_env()]["login_page"]}')
        return all_envs[self.current_env()]["login_page"]

    def get_auth_url(self):
        log.info(f'auth_page_url under test: {all_envs[self.current_env()]["auth_url"]}')
        return all_envs[self.current_env()]["auth_url"]

    def get_sso_host(self):
        log.info(f'login_page_url under test: {all_envs[self.current_env()]["sso_host"]}')
        return all_envs[self.current_env()]["sso_host"]

    def get_app_api_hostname(self):
        log.info(f'app_api_hostname under test: {all_envs[self.current_env()]["app_api_hostname"]}')
        return all_envs[self.current_env()]["app_api_hostname"]

    def get_user_api_hostname(self):
        log.info(f'user_api_hostname under test: {all_envs[self.current_env()]["user_api_hostname"]}')
        return all_envs[self.current_env()]["user_api_hostname"]

    def get_ccs_device_url(self):
        log.info(f'user_api_hostname under test: {all_envs[self.current_env()]["ccs_device_cloud_url"]}')
        return all_envs[self.current_env()]["ccs_device_cloud_url"]

    def get_ccs_activate_v1_device_url(self):
        log.info(f'user_api_hostname under test: {all_envs[self.current_env()]["ccs_activate_v1_device_url"]}')
        return all_envs[self.current_env()]["ccs_activate_v1_device_url"]

    def get_ccs_activate_v2_device_url(self):
        log.info(f'user_api_hostname under test: {all_envs[self.current_env()]["ccs_activate_v2_device_url"]}')
        return all_envs[self.current_env()]["ccs_activate_v2_device_url"]

    def get_hpe_device_url(self):
        log.info(f'user_api_hostname under test: {all_envs[self.current_env()]["hpe_device_cloud_url"]}')
        return all_envs[self.current_env()]["hpe_device_cloud_url"]

    def get_aruba_device_url(self):
        log.info(f'user_api_hostname under test: {all_envs[self.current_env()]["aruba_device_v1_url"]}')
        return all_envs[self.current_env()]["aruba_device_v1_url"]

    def get_aruba_switch_device_url(self):
        log.info(f'user_api_hostname under test: {all_envs[self.current_env()]["aruba_device_v2_url"]}')
        return all_envs[self.current_env()]["aruba_device_v2_url"]

    def get_aruba_legacy_device_url(self):
        log.info(f'user_api_hostname under test: {all_envs[self.current_env()]["aruba_legacy_activate_url"]}')
        return all_envs[self.current_env()]["aruba_legacy_activate_url"]

    def home_page_url(self):
        return f"{self.login_page_url}home"

    def _get_cluster_info_dict(self):
        with open(CLUSTER_INFO_FILE) as cluster_info:
            cluster_info_json = cluster_info.read()
        return json.loads(cluster_info_json)

    def get_humio_url(self):
        humio_url = None
        if os.getenv("ClusterUnderTest"):
            humio_url = humio_env[os.getenv("ClusterUnderTest")]['humio_url']
        else:
            if self.current_env() == "polaris":
                humio_url = "https://polaris-us-west-2.cloudops.ccs.arubathena.com/logs"
            if self.current_env() == "mira":
                humio_url = "https://mira-us-east-2.cloudops.ccs.arubathena.com/logs"
            if self.current_env() == "pavo":
                humio_url = "https://pavo-us-west-2.cloudops.common.cloud.hpe.com/logs"
            if self.current_env() == "aquila":
                humio_url = "https://aquila-us-east-2.cloudops.common.cloud.hpe.com/logs"
            if "triton" in self.current_env():
                humio_url = "https://triton-us-west-2.cloudops.ccs.arubathena.com/logs"
        return humio_url

    def get_humio_repository(self, env_region=os.getenv("ClusterUnderTest")):
        return humio_env[env_region]['humio_repository']

    def current_env(self):
        if os.getenv("ClusterUnderTest"):
            cluster_under_test = os.getenv("ClusterUnderTest")
            cluster_split_list = cluster_under_test.split("-")
            if len(cluster_split_list) > 2:
                cluster_name = cluster_split_list[0]
            elif len(cluster_split_list) == 2:
                cluster_name = cluster_under_test
            else:
                raise ValueError(f"cluster_under_test is not matching format: {cluster_under_test}")
            return cluster_name
        else:
            return os.getenv("CURRENT_ENV")

    @staticmethod
    def downloaded_creds():
        """
        download LD creds from remote s3 locations if available or use from local directory
        """
        s3_file_location = "akuc/auto-activate-sm-workflows/creds/"
        get_cwd = os.getcwd()
        automation_directory = os.environ["AUTOMATION_DIRECTORY"]
        try:
            download_file(s3_file_location)
            shutil.copy(
                f"{get_cwd}/{s3_file_location}user_creds.json",
                automation_directory,
            )
            with open(os.path.join(automation_directory, "user_creds.json")) as fd:
                s3_login_data = json.load(fd)
                log.info("downloading creds from remote locations")
        except:
            with open(os.path.join(automation_directory, "user_creds.json")) as fd:
                s3_login_data = json.load(fd)
                log.info("using creds from local locations")
        return s3_login_data

    def resolve_creds(self, cluster):
        """
        downloading creds from remote s3 locations if available
        """
        log.info("getting creds from remote or local location")
        try:
            getcreds = self.downloaded_creds()
            users_passwords = getcreds[cluster]["users"]
            log.info(users_passwords)
            return users_passwords
        except Exception as e:
            log.error(f"not able to download credentials, check logs:\n{e}")

    def get_ld_flags(self, ld_flag):
        """
        :param: launch darkly flag name
        :return: bool
        """
        ld_flag_status = False
        try:
            current_env = self.current_env()
            passwords = self.resolve_creds(current_env)
            sdk_key = passwords["ld_sdk_user"]
            ldclient.set_config(Config(sdk_key))
            client = ldclient.get()
            user = {"key": current_env}
            state = client.all_flags_state(context=user)
            ld_flag_status = state.to_json_dict().get(ld_flag)
        except:
            log.info("not able to get ld_flag_status, return default as False")
        return ld_flag_status
