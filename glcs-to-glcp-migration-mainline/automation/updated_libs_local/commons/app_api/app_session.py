"""
CCS APP API Session Library
"""
import json
import logging
import os
import time

from hpe_glcp_automation_lib.libs.authn.user_api.session.core.session import Session

log = logging.getLogger(__name__)


class AppSession(Session):
    """
    AppSession common API class
    """
    stored_sessions = {}

    def __init__(
            self,
            app_api_host,
            sso_host,
            client_id,
            client_secret,
            scope="read write",
            max_retries=3,
            retry_timeout=5,
            debug=True,
            **kwargs
    ):
        """
        :param app_api_host: CCS App API Hostname
        :param sso_host: SSO Host name of the Target Cluster
        :param client_id: Client ID
        :param client_secret: Client Secret
        :param scope: Token scope
        :param max_retries: Maximum number of retries for the Retriable errors
        :param retry_timeout: Timeout between the retries (in seconds)
        :param debug: Enable/Disable Debug logging of HTTP Requests/Responses
        :param kwargs: additional arguments for Session class
        """
        log.info("Initializing app_session for user api calls")
        super().__init__(max_retries=max_retries, retry_timeout=retry_timeout, debug=debug, **kwargs)
        self.sso_host = sso_host
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self.base_url = f"https://{app_api_host}"
        self.token_json = None
        self.get_token()

    @property
    def __client_details(self):
        return self.base_url, self.sso_host, self.client_id, self.client_secret, self.scope

    @staticmethod
    def __get_cluster_info_dict():
        cluster_info_file = "/configmap/data/infra_clusterinfo.json"
        with open(cluster_info_file) as cluster_info:
            cluster_info_json = cluster_info.read()
        return json.loads(cluster_info_json)

    @staticmethod
    def __get_hostname(hostname):
        if hostname.startswith("https://"):
            return hostname
        else:
            return f"https://{hostname}"

    def __store_current_session(self):
        self.stored_sessions[self.__client_details] = {"token": None, "session": None}
        self.stored_sessions[self.__client_details]["token"] = self.token_json
        self.stored_sessions[self.__client_details]["session"] = self.session
        self.stored_sessions[self.__client_details]["token_refresh_timestamp"] = int(time.time())
        log.info(f"App API session for {self.client_id} was stored successfully.")

    def __reuse_session(self, client_details):
        """
        :param client_details: key in format of tuple (host, sso_host, client_id, client_secret, scope)
         to get assigned session details
        """
        self.token_json = self.stored_sessions[client_details]["token"]
        self.session = self.stored_sessions[client_details]["session"]
        log.info(f"App API session for {self.client_id} was accessed successfully for reusing.")

    def __purge_current_session(self):
        session_purged = self.stored_sessions.pop(self.__client_details, False)
        if session_purged:
            log.info(f"Stored App API session for {self.client_id} was purged successfully.")
        else:
            log.warning(
                f"There is no stored App API session for {self.client_id}, but session purge was requested for it")

    def __set_headers(self):
        """Set the session headers
        """
        self.session.headers = {
            "Authorization": f"Bearer {self.token_json['access_token']}"
        }

    def _get_app_api_hostname(self):
        try:
            if os.getenv("POD_NAMESPACE") is None:
                log.info("running in local env, configmap is not available, getting from settings.json")
                cluster_config = self.get(f"{self.base_url}/settings.json")
                app_api_hostname = cluster_config["baseUrl"].replace('user', 'app_api')
                return app_api_hostname
            else:
                cluster_info_dict = self.__get_cluster_info_dict()
                if "LIST_OF_REGIONS" in cluster_info_dict.get("clusterinfo"):
                    rw_region = (cluster_info_dict.get("clusterinfo", {}).get('READ_WRITE_REGION'))
                    app_api_hostname = cluster_info_dict.get("clusterinfo", {}) \
                        .get("HOSTNAMES", {}).get(rw_region, {}).get('ccs_app_api_hostname', {})
                    return self.__get_hostname(app_api_hostname)
                else:
                    app_api_hostname = cluster_info_dict.get("clusterinfo", {}) \
                        .get("HOSTNAMES", {}).get("ccs_app_api_hostname", {})
                    return self.__get_hostname(app_api_hostname)
        except Exception as e:
            log.error("not able to get LIST_OF_REGIONS {}".format(e))

    def _get_secondary_app_api_hostname(self):
        try:
            if os.getenv("POD_NAMESPACE") is None:
                log.info("running in local env, configmap is not available, getting from settings.json")
                cluster_config = self.get(f"{self.base_url}/settings.json")
                prefix_base_url = cluster_config["baseUrl"].split(".")
                prefix_base_url[0] = cluster_config["baseUrl"].split('.')[0].replace('user', 'app_api') + "-r"
                return '.'.join(prefix_base_url)
            else:
                cluster_info_dict = self.__get_cluster_info_dict()
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
                        return self.__get_hostname(secondary_app_api_hostname)
                return None
        except Exception as e:
            log.error("not able to get LIST_OF_REGIONS {}".format(e))

    def get_token(self, set_auth_header=True):
        """Generates the token info from the sso
        :param set_auth_header: set or not value to object's Authorization header
        :return: Access Token if received successfully or None

        """
        if self.__client_details in self.stored_sessions:
            self.__reuse_session(self.__client_details)
        else:
            data = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "client_credentials",
                "scope": self.scope,
            }
            response = self.post(
                f"https://{self.sso_host}/as/token.oauth2",
                data=data,
                ignore_handle_response=True,
            )
            if response.status_code == 200:
                self.token_json = response.json()
                if set_auth_header:
                    self.__set_headers()
                self.__store_current_session()
            else:
                return None
        return self.stored_sessions[self.__client_details]["token"]['access_token']

    def refresh_token(self):
        """
        Refresh the token info from the authenticated session
        :return: Boolean (True or False)
        """

        session_stored = self.stored_sessions.get(self.__client_details)
        token_refresh_timestamp = session_stored["token_refresh_timestamp"] if session_stored else 0

        if int(time.time()) - token_refresh_timestamp > 300:
            self.__purge_current_session()
            return self.get_token()
        else:
            log.warning("Refresh token requested too frequently. Possible error")
            return False

    @staticmethod
    def validate_retriable_response(response):
        """
        Additional validation of retriable errors before going for retries
        :param response: Response object
        :return: True/False
        """
        if not response.headers.get("server") == "HPE":
            log.error("Server Header not found")
            return False
        return True
