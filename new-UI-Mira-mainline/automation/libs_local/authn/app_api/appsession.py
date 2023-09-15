"""
CCS APP API Session Library
"""
import time
import logging
log = logging.getLogger(__name__)
import time
from hpe_glcp_automation_lib.libs.authn.user_api.session.core.ccs_session import CCSSession

class AppSession(CCSSession):
    """
    App Session Class for CCS App Instance APIs
    """

    def __init__(
        self,
        host,
        sso_host,
        client_id,
        client_secret,
        scope="read write",
        protocol="https",
        max_retries=3,
        retry_timeout=5,
        debug=True,
    ):
        """
        :param host: CCS App API Hostname
        :param sso_host: SSO Host name of the Target Cluster
        :param client_id: Client ID
        :param client_secret: Client Secret
        :param scope: Token scope
        :param max_retries: Maximum number of retries for the Retriable errors
        :param retry_timeout: Timout between the retries (in seconds)
        :param debug: Enable/Disable Debug logging of HTTP Requests/Responses
        """
        super(AppSession, self).__init__(
            max_retries=max_retries, retry_timeout=retry_timeout,
        )
        self.sso_host = sso_host
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = "https://" + host
        self.scope = scope
        self.token_json = None
        self.debug = debug
        self.refresh_timestamp = 0

    def get_token(self, head=None):
        """
        Generates the token info from the sso
        :return: Boolean (True or False)
        """
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
        if response.status_code == 200 and head == True:
            self.token_json = response.json()
            return self.token_json['access_token']
        elif response.status_code == 200:
            self.token_json = response.json()
            self.refresh_timestamp = int(time.time())
            self._set_headers()
            return True
        return False

    def refresh_token(self):
        """
        Refresh the token info from the authenticated session
        :return: Boolean (True or False)
        """
        if int(time.time()) - self.refresh_timestamp > 300:
            return self.get_token()
        else:
            log.warning("Refresh token requested too frequently. Possible error")
            return False

    def _set_headers(self):
        """
        Set the session headers
        :return:
        """
        self.session.headers = {
            "Authorization": f"Bearer {self.token_json['access_token']}"
        }
