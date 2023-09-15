"""
UIDoorway User API
"""
import json
import logging
import re
import time
from typing import List

from hpe_glcp_automation_lib.libs.commons.user_api.ui_session import UISession

log = logging.getLogger(__name__)


# TODO: need to cleanup this module - to many unused and unreachable code.
#  E.g. get_license_list 'res' variable definition
class UIDoorway(UISession):
    """
    UIDoorway API Class
    """

    def __init__(self, host, user, password, pcid):
        """
        :param host: CCS UI Hostname
        :param user: Login Credentials - Username
        :param password: Login Credentials - Password
        :param pcid: Platform Customer ID

        """
        log.info("Initializing ui_doorway for user api calls")
        super().__init__(host, user, password, pcid)

        self.base_path = "/ui-doorway/ui"
        self.api_version = "/v1"

    def _get_path(self, path):
        return f"{self.base_path}{self.api_version}/{path}"

    def load_account(self, platform_customer_id):
        """
        Load into a Platform Customer Account
        :param platform_customer_id: Platform Customer ID
        :return:
        """
        self.get(f"/authn/v1/session/load-account/{platform_customer_id}")

    def sm_add_lic(self, key):
        headers = {'Content-type': 'application/json'}
        payload = {"key": key}
        result = self.post(f"{self.base_path}{self.api_version}/customers/license",
                           data=json.dumps(payload),
                           headers=headers)
        log.info("add device inventory result {}".format(result))
        return result

    def add_device_activate_inventory_emdm(self, device_list, dev_cat=None):
        """
        Add device to activate inventory
        :param device_list: list of dictionaries with devices' details (MAC-address, Serial number)
        :param dev_cat: device category
        :return:
        """
        devlist = []
        if dev_cat:
            for dev in device_list:
                new_dev = {
                    'mac_address': dev['device_1']['eth_mac'],
                    'serial_number': dev['device_1']['serial_no'],
                    'app_category': dev_cat
                }
                devlist.append(new_dev)
        devices = {'devices': devlist}
        headers = {'Content-type': 'application/json'}
        time.sleep(3)
        result = self.post(f"{self.base_path}{self.api_version}/activate/devices", data=json.dumps(devices),
                           headers=headers)
        log.info("add device inventory result {}".format(result))
        return result

    def verify_add_device_activate_inventory_emdm(self, device_list):
        """
        Add device to activate inventory
        :param device_list: list of dictionaries with devices' details (MAC-address, Serial number)
        :return:
        """
        mac = device_list[0]['device_1']['eth_mac']
        result = self.get(f"{self.base_path}{self.api_version}/activate/devices?mac_address={mac}")
        log.info("Get device inventory result {}".format(result))
        return result

    def add_device_activate_inventory(self, device_list):
        """
        Add device to activate inventory
        :param device_list: list of dictionaries with devices' details (MAC-address, Serial number)
        :return:
        """
        headers = {'Content-type': 'application/json'}
        result = self.post(f"{self.base_path}{self.api_version}/devices", data=json.dumps(device_list), headers=headers)
        log.info("add device inventory result {}".format(result))
        return result

    def list_devices(self, secondary=None):
        """
        List devices of customer in activate inventory
        :param secondary: Optional parameter, to use second get method
        :return: list of devices
        """
        if secondary:
            return self.get_secondary(f"{self.base_path}{self.api_version}/devices")
        else:
            return self.get(f"{self.base_path}{self.api_version}/devices")

    def assign_devices_to_app_in_activate_inventory(self, device_list, appid, application_instance_id):
        """
        Assign devices to app in activate inventory
        :param device_list: list of devices to be unassigned (limit 500)
            Example device_list: [{"serial_number":"APSNMR-01","device_type":"AP","part_number":"NWPRTTR01"}]
        :param appid: Application ID
        :param application_instance_id: application instance id for device assignment
        :return:
        """
        data = {
            "assign_list": [
                {
                    "devices": device_list,
                    "application_id": appid,
                    "application_instance_id": application_instance_id
                }
            ]
        }
        headers = {'Content-type': 'application/json'}
        result = self.post(f"{self.base_path}{self.api_version}/devices/application-instance", data=json.dumps(data),
                           headers=headers)
        log.info("assign devices result {}".format(result))
        return result

    def unassign_devices_from_app_in_activate_inventory(self, device_list):
        """
        Unassign devices to app in activate inventory
        :param device_list: list of devices to be unassigned (limit 500)
        :Example device_list: [{"serial_number":"APSNMR-01","device_type":"IAP","part_number":"NWPRTTR01"}]
        :return:
        """
        data = {"devices": device_list}
        headers = {'Content-type': 'application/json'}
        result = self.delete(f"{self.base_path}{self.api_version}/devices/application-instance", data=json.dumps(data),
                             headers=headers)
        log.info("unassign devices output result {}".format(result))
        return result

    def get_licenses(self, secondary=None, params=None):
        """
        List of customer licenses details of different devices
        :return: dict: list of customer license info of different devices
        Example: https://docs.ccs.arubathena.com/subscription-management/#operation/getCustomerInfoByLicenseKey

        Example: return dict: {'subscriptions':
                            [{'subscription_key': 'E18E41A85B77B4E17AF0949EE3943D38E',
                             'subscription_type': 'CENTRAL_GW',
                             'platform_customer_id': 'eb54bcb4a92611eb80665a60b9b8547a',
                              'application_customer_id': None,
                               'appointments': {'subscription_start': 1620267113000,
                                'subscription_end': 1628043113000,
                                'activation_date': 1620267174238,
                                'suspension_date': None, 'reactivation_date': None,
                                'cancellation_date': None, 'duration': None},
                                'product_sku': 'JZ121-EVALS',
                                'product_description': 'Aruba 70XX Gateway Foundation 90d Sb E-STU',
                                'evaluation_type': 'EVAL',
                                'license_tier': 'FOUNDATION',
                                'subscription_tier': 'FOUNDATION_70XX',
                                'attributes': [],
                                'quantity': 10,
                                'available_quantity': 10,
                                'support_attributes': []}
        """

        log.info("get_licenses: Listing licensing information for customer")
        log.info(f"Executing GET on request URL: {self.base_path}{self.api_version}/license/devices")
        if secondary:
            return self.post_secondary(f"{self.base_path}{self.api_version}/license", params=params)
        else:
            return self.post(f"{self.base_path}{self.api_version}/license", params=params)

    def assign_license_to_devices(self, license_device_tupl_list, device_type, part_number):
        """
        Assign device to respective license
        :param license_device_tupl_list: List of tuple of serial number and subscription key
        :param device_type: Type of device used to be assigned
        :param part_number: Device part number
        :return:
         """
        log.info(f"assign_license_to_devices: license assignment triggered with input {license_device_tupl_list}")

        data = []
        headers = {'Content-type': 'application/json'}
        for (device, license) in license_device_tupl_list:
            license_data = {
                "serial_number": device,
                "subscription_key": license,
                "device_type": device_type,
                "part_number": part_number
            }
            data.append(license_data)

        resp = None
        for index in range(3):
            resp = self.post(f"{self.base_path}{self.api_version}/license/devices", json=data, headers=headers)
            if resp[0]['status'] == 'SUCCESS':
                log.info("license response for device_type: {}, {}".format(device_type, resp))
                return resp
            else:
                log.warning("assign license output result {}".format(resp))
                time.sleep(5)
        log.info("assign license output result {}".format(resp))

    def unassign_license_from_devices(self, device_serial_list):
        """
        Unassign license from list of devices under device inventory
        :param device_serial_list: List of device serials license to be unassigned from
        :return:
        """
        headers = {'Content-type': 'application/json'}
        log.info(f"unassign_license_from_devices: license unassignment triggered with input {device_serial_list}")
        result = self.delete(
            f"{self.base_path}{self.api_version}/license/devices", json=device_serial_list,
            headers=headers)
        log.info("unassign license output result {}".format(result))
        return result

    def get_device_license(self, secondary=None):
        if secondary:
            return self.get_secondary(f"{self.base_path}{self.api_version}/license/devices")
        else:
            return self.get(f"{self.base_path}{self.api_version}/license/devices")

    def delete_application_customer(self, app_cust_id):
        """
        Delete or Un-provision the app for the customer
        :param app_cust_id: Application customer id
        :return:
        """
        data = {"action": "UNPROVISION"}
        if app_cust_id:
            return self.patch(
                f"/app-provision/ui/v1/provisions/{app_cust_id}", json=data
            )

    def get_provisions(self, secondary=None):
        """
        :return: Provision Apps details
        """
        if secondary:
            return self.get_secondary(f"{self.base_path}{self.api_version}/applications/provisions")
        else:
            return self.get(f"{self.base_path}{self.api_version}/applications/provisions")

    def get_account_contact(self, secondary=None):
        if secondary:
            return self.get_secondary(f"/accounts/ui/v1/customer/profile/contact")
        else:
            return self.get(f"/accounts/ui/v1/customer/profile/contact")

    def verify_claim_device(self, sub_key):
        """
        :return: Provision Apps details
        """
        data = {'key': sub_key}
        res = self.post(f"/{self.base_path}{self.api_version}customers/license", json=data)
        return res

    def apply_subscription_key(self, sub_key):
        """
        :return: Provision Apps details
        """
        data = {'key': sub_key}
        res = self.post(f"{self.base_path}{self.api_version}/customers/license", json=data)
        return res

    def provision_application(self, region, appid):
        """
        Create an Application Customer ID for an App
        :param region: CCS Region code
        :param appid: Application ID which need to provision
        :return: Application Customer ID
        :appid: ...
        """
        data = {
            "application_id": appid,
            "region": region,
            "action": "PROVISION"
        }
        res = self.post("/app-provision/ui/v1/provisions", json=data)
        return res

    def wait_for_provision_status(self, app_cust_id, status, iterations=30, delay=6):
        """
        Wait for the Application Customer ID's status to reach the expected state
        :param app_cust_id: Application Customer ID that need to be queried
        :param status: Status value to be checked for
        :param iterations: No of times to check
        :param delay: Delay between the iterations
        :return: (True/False)
        """
        for iteration in range(1, iterations + 1):
            try:
                res = self.get(f"/app-provision/ui/v1/provisions/{app_cust_id}")
            except Exception as e:
                if status == "UNPROVISIONED" and e.response.status_code == 404:
                    log.info(f"The status of customer reached '{status}'")
                    return True
                else:
                    raise e
            else:
                if status != "UNPROVISIONED" and res["provision_status"] == status:
                    log.info(f"The status of customers reached '{status}'")
                    return True
            time.sleep(delay)
            log.info(f"Waited for {iteration * delay} seconds for status change")

        log.error(f"The customer {app_cust_id} did not attain '{status}' status")

    def list_msp_tenants(self, offset=0, count_per_page=20):
        """
        :returns a list of tenants associated with this MSP account.
        Returns a pre-condition failure if this account is a Standard Enterprise Account.
        """
        try:
            return self.get(
                f"{self.base_path}{self.api_version}/tenants"
                f"?offset={offset}&count_per_page={count_per_page}&sort_by=-ACCOUNT_SORT_BY_RECENT")
        except Exception as e:
            raise Exception(f"Could not fetch msp tenants for this account: {str(e)}. Check pre-conditions!")

    def delete_tenant(self, customer_id):
        """
        Delete a given customer/tenant if this is a valid MSP account.
        Returns a pre-condition failure otherwise.
        """
        try:
            return self.delete(f"/accounts/ui/v1/managed-service/tenant/{customer_id}")
        except Exception as e:
            raise Exception(f"Delete tenant with customer_id {customer_id} failed: {str(e)}. Check pre-conditions!")

    def toggle_account_type(self):
        """
        This endpoint converts a given account from standard enterprise account to MSP and vice-versa,
        and returns the status of the new_type and old_type.
        Note that, the pre-requisite steps required to perform this action (like deleting tenants and applications etc )
        have to be done before this end-point call to avoid adverse account side-effects.
        """
        try:
            return self.patch(f"/accounts/ui/v1/managed-service/toggle-msp")
        except Exception as e:
            raise Exception(f"Could not toggle account type {str(e)}. Check pre-conditions!")

    def get_folders(self, pcid: str = None):
        """Get devices folders of specified (if pcid not None) or current customer.
        Note: call with specified target pcid supposed to be performed by TAC-user.

        :param pcid: targeted pcid.
        :return: dict with folders details.
        """
        log.info(f"Getting list of device folders for pcid '{pcid if pcid else self.pcid}'.")
        if pcid:
            api_path = f"/cm/activate/folders?limit=100&page=0&platform_customer_id={pcid}"
        else:
            api_path = "/activate/folders?limit=100&page=0"
        result = self.get(f"{self.base_path}{self.api_version}{api_path}")
        log.info(f"Get device folders result: '{result}'.")
        return result

    def delete_folder(self, folder_id: str, pcid: str = None):
        """Delete customer devices folder with folder_id of specified (if pcid not None) or current customer.
        Note: call with specified target pcid supposed to be performed by TAC-user.

        :param folder_id: folder id.
        :param pcid: targeted pcid.
        :return: dict with deletion response details.
        """
        log.info(f"Deleting device folder with id '{folder_id}' at pcid '{pcid if pcid else self.pcid}'.")
        if pcid:
            data = {"platform_customer_id": pcid}
            api_path = f"/cm/activate/folders/{folder_id}"
        else:
            data = None
            api_path = f"/activate/folders/{folder_id}"
        headers = {'Content-type': 'application/json'}
        result = self.delete(f"{self.base_path}{self.api_version}{api_path}", data=json.dumps(data), headers=headers)
        log.info(f"Delete customer's device folder response: '{result}'.")
        return result

    def get_folder_rules(self, pcid: str = None):
        """Get devices folders of specified (if pcid not None) or current customer.
        Note: call with specified target pcid supposed to be performed by TAC-user.

        :param pcid: targeted pcid.
        :return: dict with list of rules and assigned folders.
        """

        log.info(f"Getting list of folder rules for pcid '{pcid if pcid else self.pcid}'.")
        if pcid:
            api_path = f"/cm/activate/rules?limit=100&page=0&platform_customer_id={pcid}"
        else:
            api_path = "/activate/rules?limit=100&page=0"
        result = self.get(f"{self.base_path}{self.api_version}{api_path}")
        log.info(f"Get customer rules result: '{result}'.")
        return result

    def delete_folder_rule(self, rule_id: str, pcid: str = None):
        """Delete customer folders' rule with rule_id of specified (if pcid not None) or current customer.
        Note: call with specified target pcid supposed to be performed by TAC-user.

        :param rule_id: rule id.
        :param pcid: targeted pcid.
        :return: dict with deletion response details.
        """
        log.info(f"Deleting folder rule with id '{rule_id}' at pcid '{pcid if pcid else self.pcid}'.")
        if pcid:
            data = {"platform_customer_id": pcid}
            api_path = f"/cm/activate/rules/{rule_id}"
        else:
            data = None
            api_path = f"/activate/rules/{rule_id}"
        headers = {'Content-type': 'application/json'}
        result = self.delete(f"{self.base_path}{self.api_version}{api_path}", data=json.dumps(data), headers=headers)
        log.info(f"Delete customer folder's rule response: '{result}'.")
        return result

    def move_devices_to_folder(self, devices_details: List[dict], folder_name: str, pcid: str = None):
        """Move devices with provided details to folder_name folder of specified (if pcid not None) or current customer.
        Note: call with specified target pcid supposed to be performed by TAC-user.

        :param devices_details: list of dicts with devices details. Dicts should contain following keys:
            "serial_number", "mac_address", "part_number", "device_type".
        :param folder_name: folder name.
        :param pcid: targeted pcid.
        :return: dict with response details.
        """
        log.info(f"Move devices to folder '{folder_name}' of pcid '{pcid if pcid else self.pcid}'.")
        if pcid:
            data = {"devices": devices_details, "folder_name": folder_name, "platform_customer_id": pcid}
            api_path = f"/cm/activate/devices/folder"
        else:
            folders_dict = self.get_folders()
            for folder in folders_dict.get("folders", []):
                if folder["folder_name"] == folder_name:
                    folder_id = folder["folder_id"]
                    break
            else:
                raise Exception(f"Folder '{folder_name}' was not found.")
            data = {"devices": devices_details, "folder_name": folder_name, "folder_id": folder_id}
            api_path = f"/activate/devices/folder"
        headers = {'Content-type': 'application/json'}
        result = self.post(f"{self.base_path}{self.api_version}{api_path}", data=json.dumps(data), headers=headers)
        log.info(f"Move devices to folder response: '{result}'.")
        return result

    def move_devices_to_customer(self, devices_ids: List[str], pcid: str, folder_name: str):
        """Move devices with provided ids to folder_name folder of specified pcid.
        Note: this method is supposed to be called by TAC-user.

        :param devices_ids: list of devices serial numbers or mac-addresses.
        :param pcid: targeted pcid.
        :param folder_name: folder name.
        :return: dict with response details.
        """
        log.info(f"Move devices to folder '{folder_name}' of pcid '{pcid}'.")
        device_id_key = "mac_address" if re.match(r"(\w{2}:){5}\w{2}$", devices_ids[0]) else "serial_number"
        devices_list = [{device_id_key: device_id_value} for device_id_value in devices_ids]
        folders_dict = self.get_folders(pcid)
        for folder in folders_dict.get("folders", []):
            if folder["folder_name"] == folder_name:
                folder_id = folder["folder_id"]
                break
        else:
            raise Exception(f"Folder '{folder_name}' was not found.")
        data = \
            {"folder_name": folder_name, "folder_id": folder_id, "devices": devices_list, "platform_customer_id": pcid}
        api_path = f"/cm/activate/devices/customer"
        headers = {'Content-type': 'application/json'}
        result = self.post(f"{self.base_path}{self.api_version}{api_path}", data=json.dumps(data), headers=headers)
        log.info(f"Move devices between customers response: '{result}'.")
        return result

    def get_account_activate_devices(self, pcid: str = None, **kw):
        """Get activate devices with provided details (if pcid not None) or current customer.
        Note: call with specified target pcid supposed to be performed by TAC-user.

        :param pcid: targeted pcid.
        :param kw: key-valued set of parameters for request. E.g. limit=100, external_device_type="GATEWAY", ...
        :return: dict with response details.
        """
        log.info(f"Get devices for pcid '{pcid if pcid else self.pcid}'.")
        if pcid:
            params = {"platform_customer_id": pcid, "limit": kw.pop("limit", 10), "page": kw.pop("page", 0), **kw}
            api_path = "/cm/activate/devices"
        else:
            params = {**kw}
            api_path = "/activate/devices"
        headers = {'Content-type': 'application/json'}
        result = self.get(f"{self.base_path}{self.api_version}{api_path}", params=params, headers=headers)
        log.info(f"Devices for account response: '{result}'.")
        return result.get("devices", [])

    def get_license_service_subscription_info(self, params):
        """
        API for this function
        # previous url, replaced = f"{self.base_url}/subscription-management/internal/v1/subscriptions"
        # url = f"{self.ui_user_url}/ui-doorway/ui/v1/license/service-subscriptions"
        https://docs.ccs.arubathena.com/ui-doorway/#tag/UI-API-Licenses/operation/\
        get_service_subscriptions_list_ui_doorway_ui_v1_license_service_subscriptions_get
        :param params (refer link)
        :return: json with response details.
        """
        geturl = f"license/service-subscriptions"
        url = self._get_path(geturl)
        result = self.get(url=url, params=params)
        return result

    def get_license_tier_device_group(self, device_group):
        """
        Get License Tiers Device Group
        https://docs.ccs.arubathena.com/ui-doorway/ui/v1/license/tiers
        Example:
        https://aquila-user-api.common.cloud.hpe.com/ui-doorway/ui/v1/license/tiers?\
        :param device_group=AP,GATEWAY,SWITCH,COMPUTE,DHCI_COMPUTE,STORAGE,DHCI_STORAGE
        :return: json with response details.
        """

        add_url = f"license/tiers?device_group={device_group}"
        try:
            url = self._get_path(add_url)
            res = self.get(url=url)
            log.info(f"Output of License Tier {res}")
            return res
        except Exception as error:
            log.info(f"\nException while Get License Tiers Device Group: \n {error}")

    def get_license_tier_devices(self, devices):
        """
        Get the License Tiers by Devices
        https://docs.ccs.arubathena.com/ui-doorway/ui/v1/license/tiers/devices
        Example:
        https://aquila-user-api.common.cloud.hpe.com/ui-doorway/ui/v1/license/tiers/devices
        :param devices: {"devices":[{"serial_number":"VG2208274106","device_type":"GATEWAY","part_number":"MC-VA"}]}
        :return: json with response details.
        """

        add_url = f"license/tiers/devices"
        try:
            url = self._get_path(add_url)
            res = self.post(url=url, json=devices)
            log.info(f"Output of License Tier {res}")
            return res
        except Exception as error:
            log.info(f"\nException get_UI_License_Tier_Devices: \n {error}")

    def get_license_list(self, params={}, payload={}):
        """
        Get License List
        https://docs.ccs.arubathena.com/ui-doorway/ui/v1/license
        :param params dictionary
        :param payload: Optional argument, HTTP payload
        :return: json with response details.
        """
        add_url = f"license"
        try:
            url = self._get_path(add_url)
            if payload == {}:
                res = self.post(url=url, params=params)
            else:
                res = self.post(url=url, params=params, json=payload)
            log.info(f"{url} {params}")
            res = self.post(url=url, params=params)
            log.info(f"Output of get License  {res}")
            return res
        except Exception as error:
            log.info(f"\nException while get_license_list : \n {error}")

    def get_license_detail(self, subscription_key):
        """
        Get the License detail based on subscription key
        https://docs.ccs.arubathena.com/ui-doorway/ui/v1/license
        :param subscription_key
        :return: json with response details.:
        """

        add_url = f"license/detail"
        try:
            url = self._get_path(add_url)
            params = {"subscription_key": subscription_key}
            log.info(f"{url} {params}")
            res = self.get(url=url, params=params)
            log.info(f"Output of Get the License detail {url} with subscription_key {res}")
            return res
        except Exception as error:
            log.info(f"\nException while Get the License detail based on subscription key : \n {error}")

    def get_auto_license_information(self, params={}):
        """
        Get auto license information
        https://docs.ccs.arubathena.com/ui-doorway/ui/v1/license/autolicense
        :param params dictionary
        :return: json with response details.
        """

        add_url = f"license/autolicense"
        try:
            url = self._get_path(add_url)
            log.info(f"{url} {params}")
            res = self.get(url=url, params=params)
            log.info(f"Output of  Get auto license information{url} with {params} : {res}")
            return res
        except Exception as error:
            log.info(f"\nException Get auto license information : \n {error}")

    def modify_auto_license_info(self, details):
        """
        Modify auto license information

        https://docs.ccs.arubathena.com/ui-doorway/ui/v1/license/autolicense
        :param  details
            device_type required string (Device Type) Device Type
            enabled  required boolean (Enabled) Device status
            auto_license_subscription_tier_group required string (Auto License Subscription Tier Group)
        """
        add_url = "license/autolicense"
        params = details.keys()
        if "device_type" not in params or \
                "enabled" not in params or \
                "auto_license_subscription_tier_group" not in params:
            raise Exception("Please include all required details device_type, \
            enabled, auto_license_subscription_tier_group")
        try:
            url = self._get_path(add_url)
            log.info(f"{url} {params}")
            res = self.post(url=url, json=details)
            log.info(f"Output of Apply Licenses to devices {res}")
            return res
        except Exception as error:
            log.info(f"\nException while Apply Licenses to devices : \n {error}")

    def get_auto_license_groups(self, params={}):
        """
        Get the Auto License Groups
        https://docs.ccs.arubathena.com/ui-doorway/ui/v1/license/autolicense/groups
        :param params dictionary
        :return: json with response details.
        """

        add_url = f"license/autolicense/groups"
        try:
            url = self._get_path(add_url)
            res = self.get(url=url, params=params)
            log.info(f"Output of  Get auto license information{url} : {res}")
            return res
        except Exception as error:
            log.info(f"\nException Get auto license information : \n {error}")

    def get_device_license_list(self, params={}):
        """
        Get Devices - Require/Assigned Licenses List
        https://docs.ccs.arubathena.com/ui-doorway/ui/v1/license/devices
        :param params dictionary
        :return: json with response details.
        """

        add_url = f"license/devices"
        try:
            url = self._get_path(add_url)
            res = self.get(url=url, params=params)
            log.info(f"{url} {params}")
            log.info(
                f"Output of  Get Devices - Require/Assigned Licenses List{url}  based on {params} --> {res}")
            return res
        except Exception as error:
            log.info(f"\nException Get Devices - Require/Assigned Licenses List : \n {error}")

    def get_devices_Licensed(self):
        """
        Based on UI query device needs subscription
        #UI Filters frequenty called
        #https://mira-default-user-api.ccs.arubathena.com/ui-doorway/ui/v1/license/\
        devices?device_license_type=NOT_LICENSED&limit=50&offset=0
        :return: json with response details.
        """
        try:
            params = {"device_license_type": "LICENSED", "limit": 50, "offset": 0}
            res = self.get_device_license_list(params=params)

            log.info(f"Output of  get_devices_Licensed : {res}")
            return res
        except Exception as error:
            log.info(f"\nException get device list : \n {error}")

    def get_devices_require_subscription(self):
        """
        Based on UI query device needs subscription
        #UI Filters frequenty called
        #https://mira-default-user-api.ccs.arubathena.com/ui-doorway/ui/v1/\
        license/devices?device_license_type=NOT_LICENSED&limit=50&offset=0
        :return: json with response details.

        """
        try:

            params = {"device_license_type": "NOT_LICENSED", "limit": 50, "offset": 0}

            res = self.get_device_license_list(params=params)
            log.info(f"Output of  get_devices_not_Licensed : {res}")

            return res
        except Exception as error:
            log.info(f"\nException get device list : \n {error}")

    def get_devices_require_app_assignment(self):
        """
        Based on UI query device needs app assignments
        #UI Filters frequenty called
        #https://mira-default-user-api.ccs.arubathena.com/ui-doorway/ui/v1/license/devices?device_license_type=NOT_LICENSED&limit=50&offset=0
        :return: json with response details.
        """
        try:
            payload = {"unassigned_only": True, "archive_visibility": "ALL"}
            res = self.get_device_license_list(params=payload)
            log.info(f"Output of  get_UI_devices_require_app_assignment : {res}")

            return res
        except Exception as error:
            log.info(f"\nException get device list : \n {error}")

    def create_cm_eval_subscription(self, pcid: str, subscription_tiers: list) -> list:
        """Creates eval subscription for particular pcid. Performed by TAC-user.

        :param pcid: Platform Customer's ID
        :param subscription_tiers: a list of subscription tiers for a new subscription
        :return: list with generated subscriptions.
        """
        log.info(f"Creating eval subscription for pcid '{pcid}'.")
        data = {"platform_customer_id": pcid, "subscription_tiers": subscription_tiers}
        api_path = "/cm/subscriptions/eval"
        result = self.post(f"{self.base_path}{self.api_version}{api_path}", json=data)
        log.info(f"Generate eval subscription result: '{result}'.")
        return result.get("created_subscriptions")

    def update_cm_eval_subscription(
            self, pcid: str, sub_key: str, quantity_increment: int = 0, end_date_incremental: int = 0) -> dict:
        """Updates subscription for particular sub_key. Performed by TAC-user.

        :param pcid: Platform Customer's ID
        :param sub_key: targeted subscription key.
        :param quantity_increment: value for which quantity of devices need to be updated
        :param end_date_incremental: value for which end date of subscription need to be updated (seconds)
        :return: dict with subscriptions' update status.
        """
        data = {
            "subscription_key": sub_key,
            "platform_customer_id": pcid,
            "increase_quantity_by": quantity_increment,
            "extend_end_seconds": end_date_incremental
        }
        log.info(f"Updating eval subscription for subscription key '{sub_key}'.")
        api_path = "/cm/subscriptions/modify"
        result = self.post(f"{self.base_path}{self.api_version}{api_path}", json=data)
        log.info(f"Updating subscription result: '{result}'.")
        return result

    def get_cm_customer_subscriptions(self, **kwargs):
        """Get subscriptions for particular keys. Performed by TAC-user.

        :param kwargs: dict of filtering attributes, e.g. {'platform_customer_id': 'some',
        'subscription_tier': 'some_some', 'product_sku': 'some_some_some'}
        :return: list with detailed subscriptions.
        """
        log.info(f"Get customers' subscriptions by CCS manager.")
        api_path = "/cm/subscriptions"
        params = {"limit": 10, "offset": 0}
        params.update(**kwargs)
        result = self.get(f"{self.base_path}{self.api_version}{api_path}", params=params)
        log.info(f"Getting subscriptions result: '{result}'.")
        return result.get("subscriptions")

    def transfer_cm_eval_subscription(self, pcid: str, sub_key: str) -> dict:
        """Transfer Subscription to new customer. Performed by TAC-user.
        :param pcid: New Platform Customer ID of the customer to which the subscription key should be transfered
        :param sub_key: Subscription key which needs to be transferred
        :return: dict with subscriptions' data.
        """
        data = {
            "subscription_key": sub_key,
            "new_customer_id": pcid,
        }
        log.info(f"Transferring Subscription {sub_key} to new customer '{pcid}'.")
        api_path = "/cm/subscriptions/transfer"
        result = self.put(f"{self.base_path}{self.api_version}{api_path}", json=data)
        log.info(f"Transferring Subscription result: '{result}'.")
        return result

    def delete_cm_activate_alias(self, alias: str, pcid: str) -> dict:
        """Deleting alias from particular customer. Performed by TAC-user.
        :param alias: Alias to delete
        :param pcid: Platform Customer Id of specific customer
        :return: dict with alias' deletion status.
        """
        data = {
            "platform_customer_id": pcid,
        }
        log.info(f"Deleting Alias {alias} from customer '{pcid}'.")
        api_path = f"/cm/customers/aliases/{alias}"
        result = self.delete(f"{self.base_path}{self.api_version}{api_path}", json=data)
        log.info(f"Deleting Alias result: '{result}'.")
        return result

    def add_cm_activate_alias(self, alias: str, pcid: str, alias_type="CUSTOMER_NAME") -> dict:
        """Creating alias from particular customer. Performed by TAC-user.
        :param alias: Alias Name to add
        :param alias_type: Alias Type to add
        :param pcid: Platform Customer Id of specific customer
        :return: dict with alias' creation status.
        """
        data = {
            "alias": alias,
            "type": alias_type,
            "platform_customer_id": pcid
        }
        log.info(f"Creating Alias {alias} for customer '{pcid}'.")
        api_path = "/cm/customers/aliases"
        result = self.post(f"{self.base_path}{self.api_version}{api_path}", json=data)
        log.info(f"Creating Alias result: '{result}'.")
        return result
