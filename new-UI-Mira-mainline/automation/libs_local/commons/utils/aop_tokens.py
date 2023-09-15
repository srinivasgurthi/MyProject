import logging

from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session

log = logging.getLogger(__name__)


class AOP_Token_Utils(object):
    """
    Helper functions for AOP libs
    """

    def __init__(self):
        pass

    def __token_url(self, cluster):
        if "pavo" in cluster:
            token_url = "https://sso.common.cloud.hpe.com/as/token.oauth2"
        else:
            token_url = "https://qa-sso.ccs.arubathena.com/as/token.oauth2"
        return token_url

    def getOATHToken(self, cluster, existinguseracctdevices):
        try:
            (
            client_id, client_secret) = existinguseracctdevices.aop_client_id, existinguseracctdevices.aop_client_secret
            print("Generating OATHToken...")
            client = BackendApplicationClient(client_id=client_id)
            token_url = self.__token_url(cluster)
            oauth = OAuth2Session(client=client)
            auth = HTTPBasicAuth(client_id, client_secret)
            token = oauth.fetch_token(token_url=token_url, auth=auth, verify=False)

            return token['access_token']

        except Exception as ex:
            log.info("Error while generating access_token")
            raise RuntimeError(ex)
