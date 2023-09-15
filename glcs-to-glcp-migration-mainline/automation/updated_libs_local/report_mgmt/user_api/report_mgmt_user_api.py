"""
Report Management UI API Library
"""
import logging
import pprint
import time
import json
from functools import wraps

from hpe_glcp_automation_lib.libs.commons.user_api.ui_session import UISession

log = logging.getLogger(__name__)


class ReportMgmt(UISession):
    """
    Report Mgmt UI API Class
    """

    def __init__(self, host, user, password, pcid):
        """
        :param host: CCS UI Hostname
        :param user: Login Credentials - Username
        :param password: Login Credentials - Password
        :param pcid: Platform Customer ID

        """
        log.info("Initializing report_mgmt for user api calls")
        super().__init__(host, user, password, pcid)
        self.host = host
        self.pcid = pcid
        self.base_path = "/report-mgmt/ui"
        self.api_version = "/v1"

    def _get_path(self, path):
        return f"{self.base_path}{self.api_version}/{path}"

    def _log_response(func):
        @wraps(func)
        def decorated_func(*args, **kwargs):
            log.debug(
                f"{' '.join(func.__name__.title().split('_'))} API Request"
            )
            res = func(*args, **kwargs)
            log.debug(
                f"{' '.join(func.__name__.title().split('_'))} API Response" \
                + "\n\n" + pprint.pformat(res) + "\n"
            )
            return res

        return decorated_func

    @_log_response
    def get_session(self):
        """
        call the session api
        """
        return self.session.post(
            url=self._get_path("/session"),
            headers=self.session.session.headers,
            json=self.session.session.token_json,
        )

    @_log_response
    def status_check(self):
        """
        Get status of the Report Mgmt service UI API
        :return: JSON object of the status
        """
        return self.get(
            url=self._get_path("status"), ignore_handle_response=True
        )

    @_log_response
    def post_data_source(self, payload):
        return self.post(
            url=self._get_path("datasources"), ignore_handle_response=True, json=payload
        )

    @_log_response
    def get_data_source(self):
        return self.get(
            url=self._get_path("datasources"), ignore_handle_response=True
        )

    @_log_response
    def get_data_source_with_id(self, id):
        return self.get(
            url=self._get_path(f"datasources/{id}"), ignore_handle_response=True
        )

