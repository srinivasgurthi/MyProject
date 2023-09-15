"""
Activate and device inventory app apis
"""
import time
import uuid
import logging
log = logging.getLogger(__name__)
import uuid
import time
from hpe_glcp_automation_lib.libs.authn.app_api.appsession import AppSession

class ActivateInventory(AppSession):
    def __init__(self, host, sso_host, client_id, client_secret):
        self.base_url = host
        super(ActivateInventory, self).__init__(host, sso_host, client_id, client_secret)
        self.get_token()

    def get_devices_by_pcid(self, platform_customer_id='', limit=None, page=None):
        url = f"{self.base_url}/activate-inventory/app/v1/devices/" + platform_customer_id
        if limit:
            opt = "?limit=" + str(limit) + "&page=" + str(page)
            url = f"{self.base_url}/activate-inventory/app/v1/devices/" + platform_customer_id + opt
        log.info(url)
        resp = self.get(url=url)
        log.info(resp)
        return resp

    def get_devices_by_pcid_acid(self, platform_customer_id='', application_customer_id='', limit=None, page=None):
        url = f"{self.base_url}/activate-inventory/app/v1/devices/" + platform_customer_id + "/application/" + application_customer_id
        if limit:
            opt = "?limit=" + str(limit) + "&page=" + str(page)
            url = f"{self.base_url}/activate-inventory/app/v1/devices/" + platform_customer_id + "/application/" + application_customer_id + opt
        log.info(url)
        resp = self.get(url=url)
        log.info(resp)
        return resp

    
    def get_devices_by_acid(self, application_customer_id='', limit=None, page=None):
        url = f"{self.base_url}/activate-inventory/app/v1/devices/application/" + application_customer_id
        if limit:
            opt = "?limit=" + str(limit) + "&page=" + str(page)
            url = f"{self.base_url}/activate-inventory/app/v1/devices/application/" + application_customer_id + opt
        log.info(url)
        resp = self.get(url=url)
        log.info(resp)
        return resp

    
    def get_devices_list_by_acid(self, application_customer_id='', limit=None, page=None):
        url = f"{self.base_url}/activate-inventory/app/v1/devices/application/" + application_customer_id
        data = {}
        if limit:
            opt = "?limit=" + str(limit) + "&page=" + str(page)
            url = f"{self.base_url}/activate-inventory/app/v1/devices/application/" + application_customer_id + opt
        log.info(url)
        resp = self.get(url=url, json=data)
        log.info(resp)
        return resp

    def get_device_stats_by_acid(self, application_customer_id=''):
        cus = {}
        cus["application_customer_id"] = application_customer_id
        dev_st = {"device_type": "AP", "provisioned": 0}
        cus["device_counts"] = [dev_st]
        cus["total_devices"] = 0
        data = [cus]
        url = f"{self.base_url}/activate-inventory/app/v1/devices/application/stats"
        application_customer_ids = [application_customer_id]
        data = {}
        data['application_customer_ids'] = application_customer_ids
        log.info(url)
        resp = self.get(url=url, json=data)
        log.info(resp)
        return resp

    
    def get_devices_by_app_inst_id(self, application_instance_id=''):
        url = f"{self.base_url}/activate-inventory/app/v1/application-instances/" + application_instance_id
        log.info(url)
        resp = self.get(url=url)
        log.info(resp)
        return resp

    
    def get_prov_status_by_app_inst_id(self, application_customer_id=''):
        url = f"{self.base_url}/activate-inventory/app/v1/devices/application/" + application_customer_id + "/provision"
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
            data = {
                "pagination": {
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
            url = f"{self.base_url}/activate-inventory/app/v1/devices/application/" + app_cid + "/device/history" + param
            # url = f"{self.base_url}/activate-inventory/app/v1/devices/application/" + app_cid +"/device/history"
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
            url_reset = f"{self.base_url}/activate-inventory/app/v1/devices/application/reset"
            url_prov = f"{self.base_url}/activate-inventory/app/v1/devices/application/" + acid + "/provision"
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
            url_update = f"{self.base_url}/activate-inventory/app/v1/devices/application/" + acid + "/device/" + serial
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
            url_hist = f"{self.base_url}/activate-inventory/app/v1/devices/application/" + acid + "/device/history" \
                       + "?serial_number=" + serial + "&mac=" + mac
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
            url_stats = f"{self.base_url}/activate-inventory/app/v1/devices/application/stats?application_customer_ids=" \
                        + acid
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
            url_stats = f"{self.base_url}/activate-inventory/app/v1/devices/" + pcid + "/stats"
            try:
                stats_res = self.get(url=url_stats)
            except:
                pass
