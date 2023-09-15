"""
Authz User API
"""
import json
import logging

from hpe_glcp_automation_lib.libs.commons.user_api.ui_session import UISession

log = logging.getLogger(__name__)


class AuthzUserApi(UISession):
    """
    Authz UI API Class
    """

    def __init__(self, host, user, password, pcid):
        """
        :param host: CCS UI Hostname
        :param user: Login Credentials - Username
        :param password: Login Credentials - Password
        :param pcid: Platform Customer ID

        """
        log.info("Initializing authz for user api calls")
        super().__init__(host, user, password, pcid)
        self.base_path = "/authorization/ui"
        self.api_version = "/v1"

    def role_assign(self, platform_cust_id, invited_username, role_data):
        """
        Create role in authz
        :param platform_cust_id: Platform Customer ID
        :param invited_username: username
        :param role_data: Details of the role to assign
        :return: response_code, response body
        """
        logging.info("Role_assign")
        return self.put(
            f"{self.base_path}{self.api_version}/customers/{platform_cust_id}/users/{invited_username}/roles",
            data=json.dumps(role_data))

    def role_unassign(self, platform_cust_id, user_name, application_id, role_slug):
        """
        Update an role in authz
        :param platform_cust_id: Platform Customer ID
        :param user_name: username
        :param application_id: Application ID
        :param role_slug: Details to update for the role
        :return: response_code, response body
        """
        log.info("Role_unassign")

        role_data = {"delete": [{"application_id": application_id, "slug": role_slug}]}
        return self.put(f"{self.base_path}{self.api_version}/customers/{platform_cust_id}/users/{user_name}/roles",
                        data=json.dumps(role_data))

    def create_role_for_app(self, application_id, platform_cust_id, role_data):
        logging.info("role_data {}".format(role_data))
        return self.post(
            f"{self.base_path}{self.api_version}/customers/{platform_cust_id}/applications/{application_id}/roles",
            data=json.dumps(role_data))

    def role_delete(self, platform_cid, application_id, role_slug):
        """
        Delete an role from authz
        :param platform_cid: Platform Customer ID
        :param application_id: Application ID
        :param role_slug: Slug for the role to delete
        :return: response_code, response body
        """
        return self.delete(
            f"{self.base_path}{self.api_version}/customers/{platform_cid}/applications/{application_id}/roles/{role_slug}")

    def ccs_get_role(self, platform_cust_id, secondary=None):
        """
        get ccs role
        :param platform_cid: Platform Customer ID
        :return: response_code, response body
        """
        if secondary:
            return self.get_secondary(f"{self.base_path}{self.api_version}/customers/{platform_cust_id}/roles")
        else:
            self.get(f"{self.base_path}{self.api_version}/customers/{platform_cust_id}/roles")

    def app_get_role(self, platform_cust_id, application_id, secondary=None):
        """
        get app role
        :param platform_cid: Platform Customer ID
        :return: response_code, response body
        """
        if secondary:
            return self.get_secondary(
                f"{self.base_path}{self.api_version}/customers/{platform_cust_id}/applications/{application_id}/roles")
        else:
            return self.get(
                f"{self.base_path}{self.api_version}/customers/{platform_cust_id}/applications/{application_id}/roles")
