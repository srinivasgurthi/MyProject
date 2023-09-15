"""
App Provision UI API Library
"""
import logging
import pprint
import time
from functools import wraps

from hpe_glcp_automation_lib.libs.commons.user_api.ui_session import UISession

log = logging.getLogger(__name__)


class AppProvision(UISession):
    """
    App Provision UI API Class
    """

    def __init__(self, host, user, password, pcid):
        """
        :param host: CCS UI Hostname
        :param user: Login Credentials - Username
        :param password: Login Credentials - Password
        :param pcid: Platform Customer ID

        """
        log.info("Initializing app_prov for user api calls")
        super().__init__(host, user, password, pcid)
        self.base_path = "/app-provision/ui"
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

    def get_status(self):
        """
        Get status of the App Provision service UI API
        :return: JSON object of the status
        """
        return self.session.get(self._get_path("status"))

    def get_provisions(self, app_cust_id="", **params):
        """
        Get provisions from App Provisions service
        :param params: Keyword argument of the following:
            offset : Pagination offset
            limit : Page length
            region : Region
            application_id : ID of the Application
            provision_status : Provision status like PROVISIONED,
                UNPROVISIONED etc
            account_type : Account type (STANDALONE or MSP)
        :return: JSON body containing provisions
        """
        if not app_cust_id:
            return self.session.get(self._get_path("provisions"), params=params)
        else:
            return self.session.get(self._get_path(f"provisions/{app_cust_id}"))

    def provision_app(self, app_id, region):
        """
        Initiate provisioning of the app_api to the customer
        :param app_id: ID of application to be provisioned
        :param region: Region
        :return: JSON body containing App Customer ID
        """
        data = {"application_id": app_id,
                "region": region, "action": "PROVISION"}
        return self.session.post(self._get_path("provisions"),
                                 json=data)

    def unprovision_app(self, app_cust_id):
        """
        Un-provision the app_api to the customer
        :param app_cust_id: Application customer id
        :return:
        """
        data = {"action": "UNPROVISION"}
        if app_cust_id:
            return self.session.patch(
                self._get_path(f"provisions/{app_cust_id}"),
                json=data
            )

    def delete_provision(self, app_cust_id):
        """
        Delete the provision
        :param app_cust_id: Application customer id
        :return:
        """
        return self.session.delete(
            self._get_path(f"provisions/{app_cust_id}")
        )

    def wait_for(self, cust_ids, status, iterations=20, delay=6):
        """
        Wait for the Customer IDs' status to reach the expected value
        :param cust_ids: List of Customer IDs that need to be queried
        :param status: Status value to be checked for
        :param iterations: No of times to check
        :param delay: Delay between the iterations
        :return: (True/False)
        """
        for iteration in range(1, iterations + 1):
            tmp_cust_ids = cust_ids[:]
            for cust_id in tmp_cust_ids:
                res = self.get_provisions(app_cust_id=cust_id)
                if res["provision_status"] == status:
                    cust_ids.remove(cust_id)
            if not cust_ids:
                log.info(f"The status for all customers reached '{status}'")
                return True
            time.sleep(delay)
            log.info(f"Waited for {iteration * delay} seconds for status change")
        else:
            log.error(f"Few customers did not attain '{status}' status\n\n" + pprint.pformat(cust_ids) + "\n")
            return False
