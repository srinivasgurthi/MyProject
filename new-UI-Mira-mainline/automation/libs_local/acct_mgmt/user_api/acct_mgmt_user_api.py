"""
App Provision UI API Library
"""
import logging

from hpe_glcp_automation_lib.libs.commons.user_api.ui_session import UISession

log = logging.getLogger(__name__)


class AcctMgmtUserApi(UISession):
    """
    Account Management UI API Class
    """

    def __init__(self, host, user, password, pcid):
        """
        :param host: CCS UI Hostname
        :param user: Login Credentials - Username
        :param password: Login Credentials - Password
        :param pcid: Platform Customer ID
        """
        log.info("Initializing acct_mgmt for user api calls")
        super().__init__(host, user, password, pcid)
        self.base_path = "/accounts/ui"
        self.api_version = "/v1"

    def get_account_contact(self, secondary=None):
        if secondary:
            return self.get_secondary(f"{self.base_path}{self.api_version}/customer/profile/contact")
        else:
            return self.get(f"{self.base_path}{self.api_version}/customer/profile/contact")
