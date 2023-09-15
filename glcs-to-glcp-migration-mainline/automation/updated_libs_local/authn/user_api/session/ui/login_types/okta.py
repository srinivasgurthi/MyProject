"""
Login Type - OKTA
"""
import logging
import re
from bs4 import BeautifulSoup
import pyotp as pt

import urllib.parse as urlparse

from hpe_glcp_automation_lib.libs.authn.user_api.session.core.exceptions import (
    SessionException, LoginFailedException, MFASecretKeyFailedException
)


LOG = logging.getLogger(__name__)


class Okta(object):
    """
    Class for handling OKTA login
    """

    def __init__(self, *args, **kwargs):
        """
        :param args: Argument tuple (cluser config and session)
        :param kwargs: Keyword arguments (user and password)
        """
        self.cluster_config = args[0]
        self.session = args[1]
        self.user = kwargs["user"]
        self.password = kwargs["password"]
        self.sso_host = self.cluster_config["authorityURL"]
        self.token = None
        self.auth_host = None

    def login(self, response):
        """
        Handles UI login by parsing the HTML content
        :response: Response object containing the login HTML page
        :return: Response object after the login is successful
        """
        for line in response.text.splitlines():
            if "stateToken" in line:
                break
        self.auth_host = urlparse.urlparse(response.url).netloc
        t = re.compile('.*stateToken":"(.*)","helpLinks.*').match(line)[1]
        self.token = t.encode().decode('unicode-escape').encode('latin1').decode('utf-8')
        authn_url = f"https://{self.auth_host}/api/v1/authn"
        payload = {
            "multiOptionalFactorEnroll": True,
            "warnBeforePasswordExpired": True,
            "password": self.password,
            "stateToken": self.token,
            "username": self.user
        }
        try:
            r = self.session.post(authn_url, json=payload)
        except SessionException as e:
            if e.response.status_code == 401:
                raise LoginFailedException("Login Failed")
            raise e

        if r['status'] != "MFA_REQUIRED":
            okta_redirect = f"https://{self.auth_host}/login/token/redirect"
            return self.session.get(okta_redirect, params={"stateToken": self.token})
        return r

class Okta_SSO(Okta):
    """
    Class for handling OKTA SSO login
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def fetch_idp_id(self, idp_id_list):
        idp_id = None

        host = re.compile("https://(.*).hpe.com").match(self.cluster_config["oktaURL"])[1]

        re_complie_str = ".*var .* = { text: 'Sign in with SSO', id: '(.*)' };.*"
        if host == "auth-itg":
            if "qa-sso" in self.cluster_config["authorityURL"]:
                idp_id = re.compile(re_complie_str).match(idp_id_list[1])[1]
            else:
                idp_id = re.compile(re_complie_str).match(idp_id_list[2])[1]
        elif host == "auth-dev":
            idp_id = re.compile(re_complie_str).match(idp_id_list[1])[1]
        elif host == "auth":
            idp_id = re.compile(re_complie_str).match(idp_id_list[1])[1]

        return idp_id


    def login(self, response):
        """
        Handles UI login by parsing the HTML content
        :response: Response object containing the login HTML page
        :return: Response object after the login is successful
        """

        # ------ Step 2 -----------#

        for line in response.text.splitlines():
            if "okta_key" in line:
                break

        value = line[16:-1].split(',')[0]
        value = value[2:-1].replace('\\x', '%')
        okta_key = urlparse.unquote(value).split('=')[-1]

        idp_id_list = []
        for line in response.text.splitlines():
            if "text: 'Sign in with SSO'" in  line:
                idp_id_list.append(line)

        idp_id = self.fetch_idp_id(idp_id_list)

        payload = {'okta_key': okta_key}
        url = "https://" + urlparse.urlparse(response.url).netloc + "/sso/idps/" + idp_id + \
                  "?fromURI=/oauth2/v1/authorize/redirect"

        try:
            response = self.session.get(url, params=payload)
        except SessionException as e:
            if e.response.status_code == 401:
                raise LoginFailedException("Login Failed")
            raise e

        # -------- Step 3 --------
        soup = BeautifulSoup(response.text, 'html.parser')
        input_list = soup.find_all('input')

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        data_params_1 = {
            "SAMLRequest": urlparse.unquote(input_list[0]['value']),
            "RelayState": urlparse.unquote(input_list[1]['value'] + "%3Fokta_key%3D") + okta_key
        }
        url = self.sso_host + "/idp/SSO.saml2"

        try:
            response = self.session.post(url, data=data_params_1, headers=headers)
        except SessionException as e:
            if e.response.status_code == 401:
                raise LoginFailedException("Login Failed")
            raise e

        # ------- Step 4 ---------

        soup = BeautifulSoup(response.text, 'html.parser')
        input_list = soup.find_all('form')
        url_query = input_list[0]['action']

        data_params_2 = {
            "subject": self.user,
            "clear.previous.selected.subject": "",
            "cancel.identifier.selection": "false"
        }
        url = self.sso_host + url_query

        try:
            response = self.session.post(url, data=data_params_2, headers=headers)
        except SessionException as e:
            if e.response.status_code == 401:
                raise LoginFailedException("Login Failed")
            raise e

        # ------- Step 5 --------
        soup = BeautifulSoup(response.text, 'html.parser')
        form_list = soup.find_all('form')
        url = form_list[0]['action']
        okta_url = urlparse.urlparse(url).netloc
        input_list = soup.find_all('input')

        data_params_3 = {
            "SAMLRequest": input_list[0]['value'],
            "RelayState": input_list[1]['value']
        }

        try:
            response = self.session.post(url, data=data_params_3, headers=headers)
        except SessionException as e:
            if e.response.status_code == 401:
                raise LoginFailedException("Login Failed")
            raise e

        # --------- Check the login type --------
        if self.__check_idp_login_type(response):
            response = self.__signin_with_state_token(okta_url, response)
        else:
            response = self.__signin_with_authn(okta_url, response)

        # ------- Step 6 -------
        soup = BeautifulSoup(response.text, 'html.parser')
        input_list = BeautifulSoup(response.text, 'html.parser').find_all('input')
        SAMLResponse = input_list[0]['value']
        RelayState = input_list[1]['value']
        url = self.sso_host + "/sp/ACS.saml2"

        payload = {
            'SAMLResponse': SAMLResponse,
            'RelayState': RelayState
        }

        try:
            response = self.session.post(url, data=payload, headers=headers)
        except SessionException as e:
            if e.response.status_code == 401:
                raise LoginFailedException("Login Failed")
            raise e

        # ----- Step 7 -------
        soup = BeautifulSoup(response.text, 'html.parser')
        input_list = BeautifulSoup(response.text, 'html.parser').find_all('input')
        RelayState = input_list[0]['value']
        SAMLResponse = input_list[1]['value']
        url_list = BeautifulSoup(response.text, 'html.parser').find_all('form')
        url = url_list[0]["action"]
        payload = {
            'SAMLResponse': SAMLResponse,
            'RelayState': RelayState
        }

        try:
            response = self.session.post(url, data=payload, headers=headers)
        except SessionException as e:
            if e.response.status_code == 401:
                raise LoginFailedException("Login Failed")
            raise e

        return response

    def __check_idp_login_type(self, response):
        for line in response.text.splitlines():
            if "stateToken" in line:
                break

        state_token = re.compile('.*stateToken =(.*);').match(line)[1].strip()[1:]
        return len(state_token) > 3

    def __signin_with_authn(self, okta_url, response):
        # ------- STEP 1 -------
        url = "https://" + okta_url + "/api/v1/authn"
        soup = BeautifulSoup(response.text, 'html.parser')
        redirect_url = soup.find_all('input')[1]['value']

        payload = {
            "password": self.password,
            "username": self.user,
            "options": {
                "warnBeforePasswordExpired": True,
                "multiOptionalFactorEnroll": True
            }
        }

        try:
            response = self.session.post(url, json=payload)
        except SessionException as e:
            if e.response.status_code == 401:
                raise LoginFailedException("Login Failed")
            raise e

        # ------- Step 2 --------
        url = "https://" + okta_url + "/login/sessionCookieRedirect"
        sessionToken = response["sessionToken"]

        payload = {
            "checkAccountSetupComplete": True,
            "repost": True,
            "token": sessionToken,
            "redirectUrl": redirect_url
        }

        try:
            response = self.session.post(url, data=payload,
                                         headers={'Content-Type': 'application/x-www-form-urlencoded'})
        except SessionException as e:
            if e.response.status_code == 401:
                raise LoginFailedException("Login Failed")
            raise e

        return response

    def __signin_with_state_token(self, okta_url, response):
        # ------- STEP 1 -------
        for line in response.text.splitlines():
            if "stateToken" in line:
                break

        auth_host = urlparse.urlparse(response.url).netloc
        t = re.compile('.*stateToken =(.*);').match(line)[1].strip()[1:]
        stateToken = t.encode().decode('unicode-escape').encode('latin1').decode()
        url = f"https://{auth_host}/idp/idx/identify"

        payload = {
            'identifier': self.user,
            'credentials': {
                'passcode': self.password
            },
            'stateHandle': stateToken
        }

        try:
            response = self.session.post(url, json=payload)
        except SessionException as e:
            if e.response.status_code == 401:
                raise LoginFailedException("Login Failed")
            raise e

        # ------- Step 2 -----
        url = response['success']['href']

        try:
            response = self.session.get(url)
        except SessionException as e:
            if e.response.status_code == 401:
                raise LoginFailedException("Login Failed")
            raise e

        return response

class OktaMFA(Okta):
    """
    Class for handling MFA OKTA login
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.device_secret_id = kwargs.get("device_secret_id", None)

    def login(self, response):

        if self.device_secret_id is None:
            raise MFASecretKeyFailedException("MFA Device ID is not given")

        r = Okta.login(self, response)
        if r['status'] != "MFA_REQUIRED":
            raise Exception('Instead of Okta class, OktaMFA class is called !!')

        id = r['_embedded']['factors'][0]['id']
        try:
            r = self.mfa_login(id)
        except SessionException as e:
            if e.response.status_code == 401:
                raise LoginFailedException("Login Failed")
            raise e

        okta_redirect = f"https://{self.auth_host}/login/token/redirect"
        return self.session.get(okta_redirect, params={"stateToken": self.token})

    def mfa_login(self, id):
        if self.device_secret_id is None:
            raise MFASecretKeyFailedException("MFA Device Secret ID not given!!!, hence login failed")
        otp = pt.TOTP(self.device_secret_id)
        payload = {
            "passCode": otp.now(),
            "stateToken": self.token
        }
        url = f"https://{self.auth_host}/api/v1/authn/factors/{id}/verify?rememberDevice=false"
        r = self.session.post(url, json=payload)
        return r
