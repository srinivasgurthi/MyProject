"""
Login Type - PingFed (PF)
"""
import logging
#import lxml.html

from hpe_glcp_automation_lib.libs.authn.user_api.session.core.exceptions import (
    SessionException, LoginFailedException, MFASecretKeyFailedException
)

LOG = logging.getLogger(__name__)


class PF(object):
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

    def login(self, response):
        """
        Handles UI login by parsing the HTML content
        :response: Response object containing the login HTML page
        :return: Response object after the login is successful
        """
        LOG.debug("Starting the UI Login flow")
        passwd_entered = False
        retries = 5
        while retries:
            html = lxml.html.fromstring(response.text)
            actionText = html.xpath('//form[@action]')
            if actionText:
                url = actionText[0].attrib['action']
                url = self.sso_host + url
                action = actionText[0].attrib['method']
                formInputs = html.xpath('//form//input')
                form = []
                for formInput in formInputs:
                    if "name" not in formInput.attrib.keys():
                        continue
                    else:
                        if formInput.attrib['type'] == "text":
                            form.append((formInput.attrib['name'], self.user))
                        elif formInput.attrib['type'] == "password":
                            if passwd_entered == False:
                                form.append((formInput.attrib['name'],
                                             self.password))
                                passwd_entered = True
                            else:
                                if "ping-error" in response.text:
                                    raise LoginFailedException("Login Failed")
                        else:
                            if formInput.attrib.get('value') != None:
                                form.append((formInput.attrib['name'],
                                             formInput.attrib['value']))
                            else:
                                form.append((formInput.attrib['name'], "allow"))
                if action.lower() == "post":
                    LOG.debug("Action : %s, URL : %s" % (action, url))
                    response = self.session.post(url, data=form, timeout=60)
                retries -= 1
            else:
                return response
        else:
            raise LoginFailedException("Login Failed")
