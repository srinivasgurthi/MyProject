"""
This file holds functions to set up new user and new account

"""
import json
import logging
import os
import time

from hpe_glcp_automation_lib.libs.acct_mgmt.ui.acct_mgmt_pages.create_new_acct import CreateAcct
from hpe_glcp_automation_lib.libs.acct_mgmt.ui.acct_mgmt_pages.create_user import CreateUser
from hpe_glcp_automation_lib.libs.utils.gmail.gmail_imap2 import GmailOps_okta

log = logging.getLogger(__name__)
RESULTS_DIR = os.path.join('tmp', 'results')
USER_PASSWORD = "Aruba@123456789"


class HlpCreateUserCreateAcct:
    """
    Helper class to create user and account

    """

    def __init__(self, gmail_creds):
        self.gmail_user, self.gmail_passwd = gmail_creds
        log.info("Create new user")

    def svc_new_user_signup(self, browser, hostname, random_email_id, end_username):
        """
        Creates new user; verifies the user and creates new account

        :param browser: browser instance
        :param hostname: target hostname
        :param random_email_id: e-mail id for the new user
        :param end_username: username for the new user
        """
        log.info(hostname)
        create_user = CreateUser()
        random_email_id, company_name = create_user.create_user_fn(hostname, browser,
                                                                   random_email_id)
        log.info("going to check email in gmail account")
        time.sleep(20)
        gmail_session = GmailOps_okta()
        try:
            verify_url = gmail_session.get_okta_verification_link(
                my_email=random_email_id,
                gmail_username=self.gmail_user,
                gmail_password=self.gmail_passwd,
            )
            if verify_url == "None":
                raise Exception("FAIL: not able to get okta verify link")
            log.info(verify_url)
            log.info("opening browser for ui_api login {}".format(verify_url))

            create_acct = CreateAcct()
            pcid = create_acct.create_acct_fn(hostname, browser, verify_url, end_username)

            if pcid:
                setup_info = {"url": str(hostname),
                              "user": random_email_id,
                              "password": USER_PASSWORD, "pcid": pcid}
                res_setup_info = json.dumps(setup_info)
                log.info("user creation successful with first account")
                return res_setup_info
            else:
                raise Exception("FAIL: first account is not created successfully")

        except Exception as e:
            log.error(f"Error during new user signup:\n{e}")
