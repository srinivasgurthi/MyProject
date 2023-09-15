import base64
import codecs
import hashlib
import json
import logging
import os
import random
import string
import urllib.parse as urlparse
from urllib.parse import parse_qs

from hpe_glcp_automation_lib.libs.authn.user_api.session.core.exceptions import TokenRefreshException
from hpe_glcp_automation_lib.libs.authn.user_api.session.core.session import Session
from hpe_glcp_automation_lib.libs.authn.user_api.session.ui.login_factory import CCSLoginFactory

log = logging.getLogger(__name__)


class UISession(Session):
    """
    UISession common API Class
    """
    stored_sessions = {}

    def __init__(self,
                 host,
                 user,
                 password,
                 pcid,
                 max_retries=3,
                 retry_timeout=5,
                 debug=True,
                 login_type=None,
                 **kwargs):
        """
        :param host: CCS UI Hostname
        :param user: Login Credentials - Username
        :param password: Login Credentials - Password
        :param pcid: Platform Customer ID
        :params max_retries, retry_timeout: retry parameters for methods annotated with @exception_handler decorator
        :param debug: Enable/Disable Debug logging of HTTP Requests/Responses
        :param login_type: login type of okta-authentication; should be one of "okta_mfa", "okta_sso", "okta"
        :param kwargs: additional arguments for Session class

        """
        log.info("Initializing ui_session for user api calls")
        super().__init__(max_retries=max_retries, retry_timeout=retry_timeout, debug=debug, **kwargs)

        self.host = host
        self.user = user
        self.password = password
        self.pcid = pcid
        self.login_type = login_type
        self.token_json = None
        self.cluster_config = self.get_settings()
        self.sso_host = self.cluster_config["authorityURL"]
        self.base_url = self._get_user_api_hostname()
        self.domain_name = self.base_url.split('https://')[-1]
        self.redirect_uri = "https://" + self.host + "/authentication/callback"
        self.secondary_base_url = self._get_secondary_user_api_hostname()
        self.kwargs = kwargs
        self.login()
        self.load_account(pcid)

    @staticmethod
    def _generate_random_hexstring(length):
        """
        Generate random hex string for a given length
        :param length: Length of the string to be generated
        :return: Hex string
        """
        return "".join(random.choice(string.hexdigits) for _ in range(length))

    def __store_current_session(self):
        self.stored_sessions[(self.host, self.user, self.password)] = {"token": None, "session": None}
        self.stored_sessions[(self.host, self.user, self.password)]["token"] = self.token_json
        self.stored_sessions[(self.host, self.user, self.password)]["session"] = self.session
        log.info(f"User API session for {self.user} was stored successfully.")

    def __reuse_session(self, user_details):
        """
        :param user_details: key in format of tuple (host, user, password) to get assigned session details
        """
        self.token_json = self.stored_sessions[user_details]["token"]
        self.session = self.stored_sessions[user_details]["session"]
        log.info(f"User API session for {self.user} was accessed successfully for reusing.")

    def __purge_current_session(self):
        session_purged = self.stored_sessions.pop((self.host, self.user, self.password), False)
        if session_purged:
            log.info(f"Stored User API session for {self.user} was purged successfully.")
        else:
            log.warning(f"There is no stored User API session for {self.user}, but session purge was requested for it")

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
            "client_id": self.cluster_config["client_id"],
            "redirect_uri": self.redirect_uri,
            "code": query_params['code'][0],
            "code_verifier": self.code_verifier,
            "grant_type": "authorization_code"
        }
        log.debug("Fetching the token info from the auth code")
        self.token_json = self.post(self.sso_host + "/as/token.oauth2", data=data)

    def __get_session(self):
        """
        Generate the session cookies for the UI host
        :return:
        """
        log.debug("Fetching the session cookies")
        data = {"id_token": self.token_json['id_token'], }
        return self.post("/authn/v1/session", json=data)

    def __set_headers(self):
        """
        Set the session headers
        :return:
        """
        self.session.headers = {
            "Authorization": f"Bearer {self.token_json['access_token']}"
        }

    def __load_account(self):
        """
        Load a Platform Customer ID into the session
        :return:
        """
        response = self.get(self.base_url + f"/accounts/ui/v1/user/load-account/{self.pcid}")
        log.info(f"Successfully loaded into customer account : {self.pcid}")
        return response

    def _get_current_setup(self):
        try:
            if os.getenv("POD_NAMESPACE") is None:
                log.info("running in local env, configmap is not available")
                return None
            else:
                cluster_info_dict = self._get_cluster_info_dict()
                return cluster_info_dict.get("clusterinfo", {}).get("SETUP", {})
        except Exception as e:
            log.error("not able to get LIST_OF_REGIONS {}".format(e))

    def _get_multi_region_flag(self):
        try:
            if os.getenv("POD_NAMESPACE") is None:
                log.info("running in local env, configmap is not available")
                return False
            else:
                cluster_info_dict = self._get_cluster_info_dict()
                if "LIST_OF_REGIONS" in cluster_info_dict.get("clusterinfo"):
                    if (len((
                            cluster_info_dict.get("clusterinfo", {}).get("LIST_OF_REGIONS", [])))) > 1:
                        all_regions = (cluster_info_dict.get("clusterinfo", {}).get("LIST_OF_REGIONS", {}))
                        log.info("list of regions: {}".format(all_regions))
                        return True
                    else:
                        log.info("list of regions is not more than one")
                        return False
                else:
                    log.info("multi region is not enabled")
                    return False
        except Exception as e:
            log.error("not able to get LIST_OF_REGIONS {}".format(e))

    def _get_ui_hostname(self):
        try:
            if os.getenv("POD_NAMESPACE") is None:
                log.info("running in local env, configmap is not available")
                return False
            else:
                cluster_info_dict = self._get_cluster_info_dict()
                if "LIST_OF_REGIONS" in cluster_info_dict.get("clusterinfo"):
                    rw_region = (cluster_info_dict.get("clusterinfo", {}).get('READ_WRITE_REGION'))
                    ui_hostname = cluster_info_dict.get("clusterinfo", {}) \
                        .get("HOSTNAMES", {}).get(rw_region, {}).get('ccs_ui_hostname', {})
                    return self.ret_hostname(ui_hostname)
                else:
                    ui_hostname = cluster_info_dict.get("clusterinfo", {}) \
                        .get("HOSTNAMES", {}) \
                        .get("ccs_ui_hostname", {})
                    return self.ret_hostname(ui_hostname)
        except Exception as e:
            log.error("not able to get LIST_OF_REGIONS {}".format(e))

    @staticmethod
    def _get_secondary_url(base_url):
        prefix_base_url = base_url.split(".")
        prefix_base_url[0] = prefix_base_url[0] + "-r"
        return '.'.join(prefix_base_url)

    def _get_user_api_hostname(self):
        try:
            if os.getenv("POD_NAMESPACE") is None:
                log.info("running in local env, configmap is not avalaible, getting from settings.json")
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
                    user_api_hostname = cluster_info_dict.get("clusterinfo", {}) \
                        .get("HOSTNAMES", {}).get("ccs_user_api_hostname", {})
                    return self.ret_hostname(user_api_hostname)
        except Exception as e:
            log.error("not able to get LIST_OF_REGIONS {}".format(e))

    def _get_secondary_user_api_hostname(self):
        try:
            if os.getenv("POD_NAMESPACE") is None:
                log.info("running in local env, configmap is not avalaible, gettins from settings.json")
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
            log.error("not able to get LIST_OF_REGIONS {}".format(e))

    @staticmethod
    def _get_cluster_info_dict():
        cluster_info_file = "/configmap/data/infra_clusterinfo.json"
        with open(cluster_info_file) as cluster_info:
            cluster_info_json = cluster_info.read()
        return json.loads(cluster_info_json)

    def refresh_token(self):
        """
        Refresh the token info from the authenticated session
        :return: Boolean status (True/False)
        """
        if not self.token_json:
            return False
        data = {
            "client_id": self.cluster_config["client_id"],
            "grant_type": "refresh_token",
            "refresh_token": self.token_json["refresh_token"]
        }
        log.debug("Refreshing the token")
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
        self.__store_current_session()
        return True

    def load_account(self, pcid):
        if pcid:
            self.pcid = pcid
            return self.__load_account()

    def get_settings(self):
        return self.get("https://" + self.host + "/settings.json")

    @staticmethod
    def ret_hostname(hostname):
        if hostname.startswith("https://"):
            return hostname
        else:
            return "https://" + hostname

    def login(self):
        """
        Method responsible for the entire session creation
        :return:
        """
        user_details = (self.host, self.user, self.password)
        if user_details in self.stored_sessions:
            log.warning(f"Already logged in by {self.user} via user API")
            self.__reuse_session(user_details)
        else:
            self.__generate_codes()
            log.debug("Initiating the OAuth procedure")
            query_params = {
                "client_id": self.cluster_config["client_id"],
                "redirect_uri": self.redirect_uri,
                "response_type": "code",
                "scope": "openid profile email",
                "state": self.state,
                "code_challenge": self.code_challenge,
                "code_challenge_method": "S256",
                "response_mode": "query"
            }
            response = self.get(self.sso_host + "/as/authorization.oauth2", params=query_params)
            login_method = CCSLoginFactory(self.cluster_config, self, user=self.user, password=self.password,
                                           login_type=self.login_type, **self.kwargs)
            response = login_method.login(response)
            self.__get_tokens(response)
            self.__set_headers()
            self.__get_session()
            self.__store_current_session()
            log.info("Successfully logged into CCS")

    def logout(self):
        """
        Logout from the session
        :return:
        """
        self.session.get(self.base_url + "/authn/v1/session/end-session")
        self.__purge_current_session()
        log.info("Logged-out of CCS successfully")
