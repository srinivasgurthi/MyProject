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

    def get_devices_by_pcid(self, platform_customer_id='', limit=None, page=None, archived_only: bool = None):
        url = f"{self.base_url}{self.base_path}{self.api_version}/devices/{platform_customer_id}"
        if limit:
            opt = "?limit=" + str(limit) + "&page=" + str(page)
            url = f"{self.base_url}{self.base_path}{self.api_version}/devices/{platform_customer_id}{opt}"
        log.info(url)
        if archived_only:
            url = f"{url}?archive_visibility=ARCHIVED_ONLY"
            log.info(url)
        resp = self.get(url=url, ignore_handle_response=True)
        return resp

    def get_devices_by_pcid_acid(self, platform_customer_id='', application_customer_id='', limit=None, page=None):
        url = f"{self.base_url}{self.base_path}{self.api_version}/devices/{platform_customer_id}" \
              f"/application/{application_customer_id}"
        if limit:
            url = f"{url}?limit={limit}&page={page}"
        log.info(url)
        resp = self.get(url=url, ignore_handle_response=True)
        return resp

    def get_devices_by_acid(self, application_customer_id='', limit=None, page=None):
        url = f"{self.base_url}{self.base_path}{self.api_version}/devices/application/{application_customer_id}"
        if limit:
            url = f"{url}?limit={limit}&page={page}"
        log.info(url)
        resp = self.get(url=url)
        log.info(resp)
        return resp

    def get_devices_by_app_inst_id(self, application_instance_id=''):
        url = f"{self.base_url}{self.base_path}{self.api_version}/application-instances/{application_instance_id}"
        log.info(url)
        resp = self.get(url=url, ignore_handle_response=True)
        log.info(resp)
        return resp

    def get_prov_status_by_app_inst_id(self, application_customer_id=''):
        url = f"{self.base_url}{self.base_path}{self.api_version}/devices/application/{application_customer_id}/provision"
        return self.get(url=url, ignore_handle_response=True)


    def claim_device_app_api(self, device_category,
                             serial,
                             platform_id,
                             username,
                             mac=None,
                             part_num=None,
                             entitlement_id=None,
                             application_customer_id = None):
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
                ],
                "application_customer_id": application_customer_id

            }
        elif device_category == "STORAGE":
            data = {
                "devices": [
                    {
                        "serial_number": serial,
                        "entitlement_id": entitlement_id,
                        "app_category": device_category
                    }
                ],
                "application_customer_id": application_customer_id

            }
        elif device_category == "COMPUTE":
            data = {
                "devices": [
                    {
                        "serial_number": serial,
                        "part_number": part_num,
                        "app_category": device_category
                    }
                ],
                "application_customer_id": application_customer_id

            }
        url = f"{self.base_url}/activate-inventory/app/v1/devices/claim"
        resp = self.post(url=url, json=data, headers=self.session.headers, ignore_handle_response=True)
        log.info(resp)
        return resp

    def get_devices_history(self, serial_list, app_cid):
        """
        Get the device history
        """
        for dev in serial_list:
            time.sleep(.01)
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
            resp = self.get(url=url, ignore_handle_response= True)
            
            return resp

    def provision_dev_acid(self, dev_list, acid,
                           device_type=None,
                           part_number=None,
                           platform_customer_id = None,
                           username=None):   
        """
        assign a list of serial numbers to give application instance
        """
        self.session.headers.update({"CCS-Platform-Customer-Id": platform_customer_id,
                                     "CCS-Username": username})
        log.info(self.session.headers)
        url_prov = f"{self.base_url}{self.base_path}{self.api_version}/devices/application/{acid}/provision"
        data = {
        }
        for dev in dev_list:
            time.sleep(.01)
            serial = dev['serial_number']
            mac = dev['mac_address']
            data["serial_number"] = serial
            res = self.post(url=url_prov, json=data, ignore_handle_response=True)
        return res

    def update_dev_acid(self, dev_list, acid, device_name, device_type='', part_number=''):
        """
        Update device's acid # TODO Changes
        """
        data = {
        }
        for dev in dev_list:
            time.sleep(.01)
            serial = dev['serial_number']
            data['device_name'] = device_name
            url_update = f"{self.base_url}{self.base_path}{self.api_version}/devices/application/{acid}/device/{serial}"
            res = self.put(url=url_update, json=data, ignore_handle_response=True)
            log.info(f"response of update device: {res.text}")
            return res

    def history_dev_acid(self, dev_list, acid, device_type='', part_number=''):
        """
        Get the history of the device using acid
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
        return hist_resp

    def get_device_stats_for_list_of_application_customers(self, dev, acid_list, device_type='', part_number=''):
        """
        assign a list of serial numbers to give application instance
        """
        url_stats = f"{self.base_url}{self.base_path}{self.api_version}/devices/application/stats" \
                    f"?application_customer_ids={acid_list}"
        stats_res = self.get(url=url_stats, ignore_handle_response=True)
        log.info(stats_res)
        return stats_res

    def get_device_stats_of_a_platform_customer(self, pcid):
        """
        Get device stats for a Platform Customer
        """
        url_stats = f"{self.base_url}{self.base_path}{self.api_version}/devices/{pcid}/stats"
        stats_res = self.get(url=url_stats, ignore_handle_response=True)
        return stats_res

    def verify_device_claimed_by_pcid(self, platform_customer_id, device_serial_number)-> bool:
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
            # log.info(resp)
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
        data = {
                        "serial_number": device_serial_number
                    }
        if device_mac_address:
            data = {
                        "serial_number": device_serial_number,
                        "mac_address": device_mac_address
                    }
        elif device_part_number:
            data = {
                "serial_number": device_serial_number,
                "part_number": device_part_number
            }
        log.info(data)
        resp = self.post(url=url, json=data, headers=self.session.headers, ignore_handle_response=True)
        #if device is already provisioned, API response code is 400 which results in exception from GLCP session library
        return resp
    
    def update_archive_status(self, pcid, devices):
        """
        Given a platform customer ID and list pf devices, archive them.
        Make a call to /activate-inventory/app/v1/devices/archive
        :param pcid: plaform_customer_id
        :param devices: list of devices e.g. {"devices": [{"serial_number": serial_number,"archive": boolean}]}
        """
        self.session.headers.update({"CCS-Platform-Customer-Id": pcid})
        url = f"{self.base_url}/activate-inventory/app/v1/devices/archive"
        log.info(url)
        log.info(devices)
        resp = self.patch(url, json = devices, ignore_handle_response=True)
        return resp
    
        
    def create_virtual_device(self, application_customer_id,
                      part_number,
                      platform_customer_id=None,
                      username=None,
                      device_type = None):
        """
        Create a new device.

        :param application_customer_id: The customer ID of the application.
        :param part_number: The part number of the device.
        :param platform_customer_id: The customer ID of the platform. Defaults to None.
        :param username: The username to use. Defaults to None.
        :param device_type: The type of the device. Defaults to None.
        :return: The response from the API call.
        """
        headers = {
            "CCS-Transaction-ID": uuid.uuid1().hex,
            "Content-Type": "application/json",
            }
        if not platform_customer_id:
            headers["CCS-Platform-Customer-Id"] = platform_customer_id
        if not username:
            headers["CCS-Username"] = username

        self.session.headers.update(headers)
        url = f"{self.base_url}/activate-inventory/app/v1/devices/application/{application_customer_id}/device"
        payload = {
            "device_type": device_type,
            "part_number": part_number
        }
        response = self.post(url=url, json=payload, ignore_handle_response=True)
        log.info(f"This is the whole response after creating the device: {response.json()}")

        log.info(f'This is the serial number of newly created the device:  {response.json()["serial_number"]}')

        return response


    def unprovision_device_from_application(self, device: dict, platform_customer_id: str = None, username: str = None) -> dict:
        """
        Unprovision a device from an application.

        Args:
            device (dict): A dictionary containing the device details.
            platform_customer_id (str, optional): The ID of the platform customer. Defaults to None.
            username (str, optional): The username associated with the request. Defaults to None.

        Returns:
            dict: A dictionary containing the response from the API.

        """
        # Set headers for the request
        self.session.headers.update({
            "CCS-Platform-Customer-Id": platform_customer_id,
            "CCS-Username": username,
            "CCS-Transaction-Id": uuid.uuid1().hex
        })

        # Build the URL
        url = f"{self.base_url}/activate-inventory/app/v1/devices/application/unprovision"

        # Make the POST request and get the response
        response = self.post(url=url, json=device, ignore_handle_response=True)

        # Log the response and return it
        log.info(response.text)
        return response