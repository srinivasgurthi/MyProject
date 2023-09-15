"""
CCS UI Session Library
"""
import json
import os
import base64
import codecs
import random
import string
import logging
import hashlib
import requests
import urllib.parse as urlparse

from urllib.parse import parse_qs
from .login_factory import CCSLoginFactory
from ..core.ccs_session import CCSSession

from hpe_glcp_automation_lib.libs.authn.user_api.session.core.exceptions import TokenRefreshException

LOG = logging.getLogger(__name__)

class UISession(CCSSession):
    """
    UI Session Class to manage the CCS UI login
    """

    def __init__(
        self,
        host,
        username,
        password,
        pcid=None,
        max_retries=3,
        retry_timeout=5,
        debug=True,
        login_type=None,
        **kwargs
    ):
        """
        :param host: CCS UI Hostname
        :param username: Login Credentials - Username
        :param password: Login Credentials - Password
        :param pcid: Platform Customer ID
        :param max_retries: Maximum number of retries for the Retriable errors
        :param retry_timeout: Timout between the retries (in seconds)
        :param debug: Enable/Disable Debug logging of HTTP Requests/Responses
        :param login_type: type of login - okta, okta_mfa, okta_sso, pf
        """
        super(UISession, self).__init__(
            max_retries=max_retries, retry_timeout=retry_timeout, **kwargs
        )
        self.host = host
        self.user = username
        self.password = password
        self.pcid = pcid
        self.cluster_config = self.get_settings()
        self.sso_host = self.cluster_config["authorityURL"]
        self.base_url = self._get_user_api_hostname()
        self.domain_name = self.base_url.split('https://')[-1]
        self.redirect_uri = "https://" + self.host + "/authentication/callback"
        self.secondary_base_url = self._get_secondary_user_api_hostname()
        self.token_json = None
        self.debug = debug
        self.login_type = login_type
        self.kwargs = kwargs

    @staticmethod
    def _generate_random_hexstring(len):
        """
        Generate randome hex string for a given length
        :param len: Length of the string to be generated
        :return: Hex string
        """
        return "".join(random.choice(string.hexdigits) for _ in range(len))

    def get_settings(self):
        return self.get("https://" + self.host + "/settings.json")

    def _get_secondary_url(self, base_url):
        prefix_base_url = base_url.split(".")
        prefix_base_url[0] = prefix_base_url[0] + "-r"
        return '.'.join(prefix_base_url)

    def _get_current_setup(self):
        try:
            if os.getenv("POD_NAMESPACE") is None:
                LOG.info("running in local env, configmap is not avalaible")
                return None
            else:
                cluster_info_dict = self._get_cluster_info_dict()
                return cluster_info_dict.get("clusterinfo", {}).get("SETUP", {})
        except Exception as e:
            LOG.error("not able to get LIST_OF_REGIONS {}".format(e))

    def _get_multi_region_flag(self):
        try:
            if os.getenv("POD_NAMESPACE") is None:
                LOG.info("running in local env, configmap is not avalaible")
                return False
            else:
                cluster_info_dict = self._get_cluster_info_dict()
                if "LIST_OF_REGIONS" in cluster_info_dict.get("clusterinfo"):
                    if (len((
                      cluster_info_dict.get("clusterinfo", {}).get("LIST_OF_REGIONS", [])))) > 1:
                        all_regions = (cluster_info_dict.get("clusterinfo", {}).get("LIST_OF_REGIONS", {}))
                        LOG.info("list of regions: {}".format(all_regions))
                        return True
                    else:
                        LOG.info("list of regions is not more than one")
                        return False
                else:
                    LOG.info("multi region is not enabled")
                    return False
        except Exception as e:
            LOG.error("not able to get LIST_OF_REGIONS {}".format(e))

    def _get_ui_hostname(self):
        try:
            if os.getenv("POD_NAMESPACE") is None:
                LOG.info("running in local env, configmap is not avalaible")
                return False
            else:
                cluster_info_dict = self._get_cluster_info_dict()
                if "LIST_OF_REGIONS" in cluster_info_dict.get("clusterinfo"):
                    rw_region = (cluster_info_dict.get("clusterinfo", {}).get('READ_WRITE_REGION'))
                    ui_hostname = cluster_info_dict.get("clusterinfo", {}) \
                        .get("HOSTNAMES", {}).get(rw_region, {}).get('ccs_ui_hostname', {})
                    return self.ret_hostname(ui_hostname)
                else:
                    ui_hostname = cluster_info_dict.get("clusterinfo", {})\
                        .get("HOSTNAMES", {})\
                        .get("ccs_ui_hostname", {})
                    return self.ret_hostname(ui_hostname)
        except Exception as e:
            LOG.error("not able to get LIST_OF_REGIONS {}".format(e))

    def _get_user_api_hostname(self):
        try:
            if os.getenv("POD_NAMESPACE") is None:
                LOG.info("running in local env, configmap is not avalaible, getting from settings.json")
                cluster_config = self.get("https://" + self.host + "/settings.json")
                return cluster_config["baseUrl"]
            else:
                cluster_info_dict = self._get_cluster_info_dict()
                if "LIST_OF_REGIONS" in cluster_info_dict.get("clusterinfo"):
                    rw_region = (cluster_info_dict.get("clusterinfo", {}).get('READ_WRITE_REGION'))
                    user_api_hostname = cluster_info_dict.get("clusterinfo", {}) \
                        .get("HOSTNAMES", {}).get(rw_region, {}).get('ccs_user_api_hostname', {})
                    return self.ret_hostname(user_api_hostname)
                else:
                    user_api_hostname = cluster_info_dict.get("clusterinfo", {})\
                        .get("HOSTNAMES", {}).get("ccs_user_api_hostname", {})
                    return self.ret_hostname(user_api_hostname)
        except Exception as e:
            LOG.error("not able to get LIST_OF_REGIONS {}".format(e))

    def _get_app_api_hostname(self):
        try:
            if os.getenv("POD_NAMESPACE") is None:
                LOG.info("running in local env, configmap is not avalaible, getting from settings.json")
                cluster_config = self.get("https://" + self.host + "/settings.json")
                app_api_hostname = cluster_config["baseUrl"].replace('user', 'app_api')
                return app_api_hostname
            else:
                cluster_info_dict = self._get_cluster_info_dict()
                if "LIST_OF_REGIONS" in cluster_info_dict.get("clusterinfo"):
                    rw_region = (cluster_info_dict.get("clusterinfo", {}).get('READ_WRITE_REGION'))
                    app_api_hostname = cluster_info_dict.get("clusterinfo", {}) \
                        .get("HOSTNAMES", {}).get(rw_region, {}).get('ccs_app_api_hostname', {})
                    return self.ret_hostname(app_api_hostname)
                else:
                    app_api_hostname = cluster_info_dict.get("clusterinfo", {})\
                        .get("HOSTNAMES", {}).get("ccs_app_api_hostname", {})
                    return self.ret_hostname(app_api_hostname)
        except Exception as e:
            LOG.error("not able to get LIST_OF_REGIONS {}".format(e))

    def _get_secondary_user_api_hostname(self):
        try:
            if os.getenv("POD_NAMESPACE") is None:
                LOG.info("running in local env, configmap is not avalaible, gettins from settings.json")
                cluster_config = self.get("https://" + self.host + "/settings.json")
                prefix_base_url = cluster_config["baseUrl"].split(".")
                prefix_base_url[0] = prefix_base_url[0] + "-r"
                return '.'.join(prefix_base_url)
            else:
                cluster_info_dict = self._get_cluster_info_dict()
                if "LIST_OF_REGIONS" in cluster_info_dict.get("clusterinfo"):
                    if (len((
                            cluster_info_dict.get("clusterinfo", {}).get("LIST_OF_REGIONS", [])))) > 1:
                        all_regions = (cluster_info_dict.get("clusterinfo", {}).get("LIST_OF_REGIONS", {}))
                        region1 = all_regions[0]
                        region2 = all_regions[1]
                        rw_region = (cluster_info_dict.get("clusterinfo", {}).get('READ_WRITE_REGION', {}))
                        if rw_region == region1:
                            ro_region = region2
                        else:
                            ro_region = region1
                        secondary_user_api_hostname = cluster_info_dict.get("clusterinfo", {}) \
                            .get("HOSTNAMES", {}).get(ro_region, {}).get('ccs_user_api_hostname', {})
                        return self.ret_hostname(secondary_user_api_hostname)
                return None
        except Exception as e:
            LOG.error("not able to get LIST_OF_REGIONS {}".format(e))

    def _get_secondary_app_api_hostname(self):
        try:
            if os.getenv("POD_NAMESPACE") is None:
                LOG.info("running in local env, configmap is not avalaible, getting from settings.json")
                cluster_config = self.get("https://" + self.host + "/settings.json")
                prefix_base_url = cluster_config["baseUrl"].split(".")
                prefix_base_url[0] = cluster_config["baseUrl"].split('.')[0].replace('user', 'app_api') + "-r"
                return '.'.join(prefix_base_url)
            else:
                cluster_info_dict = self._get_cluster_info_dict()
                if "LIST_OF_REGIONS" in cluster_info_dict.get("clusterinfo"):
                    if (len((
                            cluster_info_dict.get("clusterinfo", {}).get("LIST_OF_REGIONS", [])))) > 1:
                        all_regions = (cluster_info_dict.get("clusterinfo", {}).get("LIST_OF_REGIONS", {}))
                        region1 = all_regions[0]
                        region2 = all_regions[1]
                        rw_region = (cluster_info_dict.get("clusterinfo", {}).get('READ_WRITE_REGION', {}))
                        if rw_region == region1:
                            ro_region = region2
                        else:
                            ro_region = region1
                        secondary_app_api_hostname = cluster_info_dict.get("clusterinfo", {}) \
                            .get("HOSTNAMES", {}).get(ro_region, {}).get('ccs_app_api_hostname', {})
                        return self.ret_hostname(secondary_app_api_hostname)
                return None
        except Exception as e:
            LOG.error("not able to get LIST_OF_REGIONS {}".format(e))

    def _get_cluster_info_dict(self):
        cluster_info_file = "/configmap/data/infra_clusterinfo.json"
        with open(cluster_info_file) as cluster_info:
            cluster_info_json = cluster_info.read()
        return json.loads(cluster_info_json)

    def ret_hostname(self, hostname):
        if hostname.startswith("https://"):
            return hostname
        else:
            return "https://" + hostname

    def __generate_codes(self):
        """
        Generate codes 'code_verifier' and 'code_challenge'
        :return:
        """
        self.code_verifier = self._generate_random_hexstring(96)
        self.state = self._generate_random_hexstring(32)
        hash = hashlib.sha256(bytes(self.code_verifier, 'utf-8')).hexdigest()
        hex = codecs.decode(hash, 'hex')
        self.code_challenge = base64.urlsafe_b64encode(hex).decode("utf-8")[:-1]

    def __get_tokens(self, response):
        """
        Generates the token info from the authenticated session
        :param response: Response object post authentication
        :return:
        """
        parsed = urlparse.urlparse(response.url)
        query_params = parse_qs(parsed.query)
        data = {
            "client_id" : self.cluster_config["client_id"],
            "redirect_uri" : self.redirect_uri,
            "code" : query_params['code'][0],
            "code_verifier": self.code_verifier,
            "grant_type": "authorization_code"
        }
        LOG.debug("Fetching the token info from the auth code")
        self.token_json = self.post(self.sso_host + "/as/token.oauth2", data=data)

    def __get_session(self):
        """
        Generate the session cookies for the UI host
        :return:
        """
        LOG.debug("Fetching the session cookies")
        data = { "id_token" : self.token_json['id_token'], }
        return self.post("/authn/v1/session", json=data)

    def refresh_token(self):
        """
        Refresh the token info from the authenticated session
        :return: Boolean status (True/False)
        """
        if not self.token_json:
            return False
        data = {
            "client_id" : self.cluster_config["client_id"],
            "grant_type" : "refresh_token",
            "refresh_token" : self.token_json["refresh_token"]
        }
        LOG.debug("Refreshing the token")
        # Work-around to get the refresh token in the PF cluster setup
        for i in range(3):
            try:
                self.token_json = self.post(
                    self.sso_host + "/as/token.oauth2", data=data
                )
                break
            except:
                pass
        else:
            raise TokenRefreshException("Could not refresh the token")
        self.__set_headers()
        return True

    def __set_headers(self):
        """
        Set the session headers
        :return:
        """
        self.session.headers = {
            "Authorization" : f"Bearer {self.token_json['access_token']}"
        }

    def __load_account(self):
        """
        Load a Platform Customer ID into the session
        :return:
        """
        response = self.get(
            self.base_url + f"/accounts/ui/v1/user/load-account/{self.pcid}"
        )
        LOG.info(f"Successfully loaded into customer account : {self.pcid}")
        return response

    def login(self):
        """
        Method responsible for the entire session creation
        :return:
        """
        self.__generate_codes()
        LOG.debug("Initiating the OAuth procedure")
        query_params = {
            "client_id" : self.cluster_config["client_id"],
            "redirect_uri" : self.redirect_uri,
            "response_type" : "code",
            "scope" : "openid profile email",
            "state" : self.state,
            "code_challenge" : self.code_challenge,
            "code_challenge_method" : "S256",
            "response_mode" : "query"
        }
        response = self.get(self.sso_host + "/as/authorization.oauth2",
                                    params=query_params)
        login_method = CCSLoginFactory(
            self.cluster_config, self, user=self.user, password=self.password,
            login_type= self.login_type, **self.kwargs
        )
        response = login_method.login(response)
        self.__get_tokens(response)
        self.__set_headers()
        self.__get_session()
        LOG.info("Successfully logged into CCS")
        if self.pcid:
            self.__load_account()

    def load_account(self, pcid):
        if pcid:
            self.pcid = pcid
            return self.__load_account()

    def logout(self):
        """
        Logout from the session
        :return:
        """
        self.session.get(self.base_url + "/authn/v1/session/end-session")
        LOG.info("Logged-out of CCS successfully")
