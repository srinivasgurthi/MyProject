"""
Activate and device inventory app apis
"""
import logging
import time
import uuid

from hpe_glcp_automation_lib.libs.commons.app_api.app_session import AppSession

log = logging.getLogger(__name__)


class ActivateInventory(AppSession):
    """
    ActivateInventory App API Class
    """

    def __init__(self, host, sso_host, client_id, client_secret):
        """
        Initialize ActivateInventory class
        :param host: cluster under test app api url
        :param sso_host: sso_host url
        :param client_id: app api client_id
        :param client_secret: app api client secret
        """
        log.info("Initializing adi_app_api for user api calls")
        super().__init__(host, sso_host, client_id, client_secret)
        self.base_path = "/activate-inventory/app"
        self.api_version = "/v1"

    def get_devices_by_pcid(self, platform_customer_id='', limit=None, page=None):
        url = f"{self.base_url}{self.base_path}{self.api_version}/devices/{platform_customer_id}"
        if limit:
            opt = "?limit=" + str(limit) + "&page=" + str(page)
            url = f"{self.base_url}{self.base_path}{self.api_version}/devices/{platform_customer_id}{opt}"
        log.info(url)
        resp = self.get(url=url)
        log.info(resp)
        return resp

    def get_devices_by_pcid_acid(self, platform_customer_id='', application_customer_id='', limit=None, page=None):
        url = f"{self.base_url}{self.base_path}{self.api_version}/devices/{platform_customer_id}" \
              f"/application/{application_customer_id}"
        if limit:
            url = f"{url}?limit={limit}&page={page}"
        log.info(url)
        resp = self.get(url=url)
        log.info(resp)
        return resp

    def get_devices_by_acid(self, application_customer_id='', limit=None, page=None):
        url = f"{self.base_url}{self.base_path}{self.api_version}/devices/application/{application_customer_id}"
        if limit:
            url = f"{url}?limit={limit}&page={page}"
        log.info(url)
        resp = self.get(url=url)
        log.info(resp)
        return resp

    def get_devices_list_by_acid(self, application_customer_id='', limit=None, page=None):
        url = f"{self.base_url}{self.base_path}{self.api_version}/devices/application/{application_customer_id}"
        data = {}
        if limit:
            url = f"{url}?limit={limit}&page={page}"
        log.info(url)
        resp = self.get(url=url, json=data)
        log.info(resp)
        return resp

    def get_device_stats_by_acid(self, application_customer_id=''):
        # TODO: "cus" is not used. Remove?
        cus = {}
        cus["application_customer_id"] = application_customer_id
        dev_st = {"device_type": "AP", "provisioned": 0}
        cus["device_counts"] = [dev_st]
        cus["total_devices"] = 0
        data = [cus]
        url = f"{self.base_url}{self.base_path}{self.api_version}/devices/application/stats"
        application_customer_ids = [application_customer_id]
        data = {'application_customer_ids': application_customer_ids}
        log.info(url)
        resp = self.get(url=url, json=data)
        log.info(resp)
        return resp

    def get_devices_by_app_inst_id(self, application_instance_id=''):
        url = f"{self.base_url}{self.base_path}{self.api_version}/application-instances/{application_instance_id}"
        log.info(url)
        resp = self.get(url=url)
        log.info(resp)
        return resp

    def get_prov_status_by_app_inst_id(self, application_customer_id=''):
        url = f"{self.base_url}{self.base_path}{self.api_version}/devices/application/{application_customer_id}/provision"
        return self.get(url=url)

    def claim_devices(self, platform_id, serial):
        """
         method to claim a serial in a platform customer account using internal api
         platform customer id is in the header of the request
        """

        self.session.headers.update({"CCS-Platform-Customer-Id": platform_id,
                                     "CCS-Transaction-Id": uuid.uuid1().hex})
        data = {
            "devices": [
                {
                    "serial": serial,
                    "entitlement_id": serial
                }
            ]
        }
        url = f"{self.base_url}/activate-inventory/internal/v1/devices/claim-serialentitlement"
        log.info(url)
        resp = self.get(url=url, json=data)
        log.info(resp)
        return resp

    def claim_device_app_api(self, device_category,
                             serial,
                             platform_id,
                             username,
                             mac=None,
                             part_num=None,
                             entitlement_id=None):
        """
            API: POST /activate-inventory/app/v1/devices/claim
            Claim a device of any kind using this app api. Add additional optional parameters to this function if needed.
            :param device_category: device category that is to be claimed. Could be NETWORK, STORAGE, COMPUTE etc.
            :param serial: serial_number of the device to be claimed
            :param platform_customer_id: Platform customer id of the account the device is to be claimed in
            :param username: Account email id to be passed in header
            :param mac: mac_address of the device to be claimed
            :param part_num: part_number of the device to be claimed
            :param entitlement_id: Entitlement id of the device to be claimed
            :return:
        """
        self.session.headers.update({"CCS-Platform-Customer-Id": platform_id,
                                     "CCS-Username": username,
                                     "CCS-Transaction-Id": uuid.uuid1().hex})
        if device_category == "NETWORK":
            data = {
                "devices": [
                    {
                        "serial_number": serial,
                        "mac_address": mac,
                        "app_category": device_category
                    }
                ]
            }
        elif device_category == "STORAGE":
            data = {
                "devices": [
                    {
                        "serial_number": serial,
                        "entitlement_id": entitlement_id,
                        "app_category": device_category
                    }
                ]
            }
        elif device_category == "COMPUTE":
            data = {
                "devices": [
                    {
                        "serial_number": serial,
                        "part_number": part_num,
                        "app_category": device_category
                    }
                ]
            }
        url = f"{self.base_url}/activate-inventory/app/v1/devices/claim"
        resp = self.post(url=url, json=data, headers=self.session.headers)
        log.info(resp)
        return resp

    def create_subscription_keys(self, license_key):
        """
        """
        data = {
            "obj_key": license_key,
            "reason": "Creation",
            "quote": "string",
            "entitlements": [
                {
                    "line_item": "string",
                    "licenses":
                        [
                            {
                                "subscription_key": license_key,
                                "device_serial_number": "JAYSN01",
                                "qty": "1",
                                "available_qty": "1",
                                "capacity": "string",
                                "appointments":
                                    {
                                        "term": "30DAYS",
                                        "subscription_start": "2021-04-25 11:31:13",
                                        "subscription_end": "2021-05-25 11:31:13",
                                        "delayed_activation": "2021-05-25 11:31:13"
                                    }
                            }
                        ],
                    "product":
                        {
                            "sku": "string",
                            "description": "string"
                        }
                }
            ],
            "activate":
                {
                    "sono": "string",
                    "sold_to": "string",
                    "sold_to_name": "string",
                    "sold_to_email": "bca@bca.com",
                    "ship_to": "string",
                    "ship_to_name": "string",
                    "ship_to_email": "bca@bca.com",
                    "end_user": "string",
                    "end_user_name": "string",
                    "end_user_email": "bca@bca.com",
                    "reseller": "string",
                    "reseller_name": "string",
                    "reseller_email": "abc@abc.com",
                    "po": "string",
                    "order_class": "string",
                    "party":
                        {
                            "id": "string",
                            "country_id": "string",
                            "global_id": "string"
                        }
                }
        }
        url = f"{self.base_url}/activate-order/v1/license/STORAGE"
        log.info(url)
        resp = self.get(url=url, json=data)
        log.info(resp)
        return resp

    def get_history(self, serial_list, appid, appinst, app_cid):
        """
        Get the device history
        """
        for dev in serial_list:
            data = {"pagination": {
                "offset": 0,
                "page": 0,
                "count_per_page": 0,
                "total_count": 0
            }}
            dev1 = {'mac_address': dev['mac_address'], 'serial_number': dev['serial_number']}
            data["device_history"] = [dev1]
            mac = dev['mac_address']
            serial = dev["serial_number"]
            param = "?mac_address={}&serial_number={}".format(mac, serial)
            url = f"{self.base_url}{self.base_path}{self.api_version}/devices/application/{app_cid}/device/history{param}"
            # url = f"{self.base_url}{self.base_path}{self.api_version}/devices/application/{app_cid}/device/history"
            res = self.get(url=url)
            # res = self.get(url=url, json=data)
            pass

    def provision_dev_acid(self, dev_list, acid, device_type='', part_number=''):
        """
        assign a list of serial numbers to give application instance
        """
        data = {
        }
        for dev in dev_list:
            time.sleep(.01)
            serial = dev['serial_number']
            mac = dev['mac_address']
            data["serial_number"] = serial
            url_reset = f"{self.base_url}{self.base_path}{self.api_version}/devices/application/reset"
            url_prov = f"{self.base_url}{self.base_path}{self.api_version}/devices/application/{acid}/provision"
            if 1:
                try:
                    reset_resp = self.post(url=url_reset, json=data)
                except:
                    pass
                try:
                    res = self.post(url=url_prov, json=data)
                except:
                    pass

    def update_dev_acid(self, dev_list, acid, device_name, device_type='', part_number=''):
        """
        assign a list of serial numbers to give application instance
        """
        data = {
        }
        for dev in dev_list:
            time.sleep(.01)
            serial = dev['serial_number']
            data['device_name'] = device_name
            url_update = f"{self.base_url}{self.base_path}{self.api_version}/devices/application/{acid}/device/{serial}"
            try:
                res = self.put(url=url_update, json=data)
                log.info(f"response of update device: {res}")
            except:
                pass

    def history_dev_acid(self, dev_list, acid, device_type='', part_number=''):
        """
        assign a list of serial numbers to give application instance
        """
        for dev in dev_list:
            time.sleep(.01)
            serial = dev['serial_number']
            mac = dev['mac_address']
            url_hist = f"{self.base_url}{self.base_path}{self.api_version}/devices/application/{acid}/device/history" \
                       f"?serial_number={serial}&mac={mac}"
            try:
                hist_resp = self.get(url=url_hist)
            except:
                pass

    def dev_stats_acid(self, dev_list, acid, device_type='', part_number=''):
        """
        assign a list of serial numbers to give application instance
        """
        for dev in dev_list:
            time.sleep(.1)
            url_stats = f"{self.base_url}{self.base_path}{self.api_version}/devices/application/stats" \
                        f"?application_customer_ids={acid}"
            try:
                stats_res = self.get(url=url_stats)
            except:
                pass

    def dev_stats_pcid(self, dev_list, pcid, device_type='', part_number=''):
        """
        assign a list of serial numbers to give application instance
        """
        for dev in dev_list:
            time.sleep(.1)
            url_stats = f"{self.base_url}{self.base_path}{self.api_version}/devices/{pcid}/stats"
            try:
                stats_res = self.get(url=url_stats)
            except:
                pass

    def verify_device_claimed_by_pcid(self, platform_customer_id, device_serial_number):
        """
                Given a plaform_customer_id, check if the serial_number exists in the platform_customer account
                :param pcid: plaform_customer_id
                :param device_serial_number: serial_number of a device
                :param device_mac_address: mac_address of a device
                :param device_part_number: part_number of a device
                :return: True is serial_number is in response, False otherwise
                """
        page_num = 0
        found_device = False
        total_count = 1
        count_per_page = 0

        #Check if serial exists in each page, if not increament page and make another call
        while (total_count > count_per_page) and found_device == False:
            url = f"{self.base_url}{self.base_path}{self.api_version}/devices/{platform_customer_id}?page={page_num}"
            resp = self.get(url=url)
            log.info(resp)
            total_count = resp["pagination"]["total_count"]
            count_per_page = resp["pagination"]["count_per_page"]
            page_num = +1
            devices_list = resp["devices"]
            for device in devices_list:
                if device_serial_number == device["serial_number"]:
                    found_device = True
                    break
        return found_device

    def verify_claim_and_assignment_to_application(self, pcid, device_serial_number, device_mac_address='', device_part_number='', application_customer_id=''):
        """
        Given a plaform_customer_id and serial_number of a device, check if the device can be claimed
        Makes a call to /activate-inventory/app/v1/devices/verify_claim
        :param pcid: plaform_customer_id
        :param device_serial_number: serial_number of a device
        :param device_mac_address: mac_address of a device
        :param device_part_number: part_number of a device
        :param application_customer_id: application_customer_id that the device can be assigned
        :return: API response
        """
        self.session.headers.update({"CCS-Platform-Customer-Id": pcid,
                                     "CCS-Transaction-Id": uuid.uuid1().hex})
        url = f"{self.base_url}/activate-inventory/app/v1/devices/verify_claim"
        log.info(url)
        if device_mac_address:
            data = {
                        "serial_number": device_serial_number,
                        "mac_address": device_mac_address
                    }
        elif device_part_number:
            data = {
                "serial_number": "device_serial_number",
                "part_number": device_part_number
            }
        log.info(data)
        resp = self.post(url=url, json=data, headers=self.session.headers)
        #if device is already provisioned, API response code is 400 which results in exception from GLCP session library
        return resp