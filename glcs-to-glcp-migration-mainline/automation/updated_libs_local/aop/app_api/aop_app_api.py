"""
Activate Order Processor App Api
"""
import logging
from hpe_glcp_automation_lib.libs.commons.app_api.app_session import AppSession
import time

log = logging.getLogger(__name__)


class ActivateOrder(AppSession):
    """
    Activate Order Processor App Api Class
    """

    def __init__(self, host, sso_host, client_id, client_secret):
        """
        Initialize ActivateOrder class
        :param host: cluster under test app api url
        :param sso_host: sso_host url
        :param client_id: app api client_id
        :param client_secret: app api client secret
        """
        log.info("Initializing aop_app_api for user api calls")
        super().__init__(host, sso_host, client_id, client_secret)
        self.base_path = "/activate-order"
        self.api_version = "/v1"

    def post_manufacturing_order(self, payload, device_category):
        """
        Manufacture devices
        :param payload: payload for manufacturing devices
        :param device_category: "COMPUTE" "NETWORK" "STORAGE"
        :return: JSON body
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/manufacturing/{device_category}"
        log.info(f"Going to POST manufacturing order line data...url: {url}, data{payload}")
        res = self.post(url=url, json=payload)
        log.info(res)
        return res

    def post_point_of_sales_order(self, payload, device_category):
        """
        Create point of sales order for devices
        :param payload: payload for point of sales order for devices
        :param device_category: "COMPUTE" "NETWORK" "STORAGE"
        :return: JSON body
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/sales/pos/{device_category}"
        log.info(f"Going to POST point of sales order data...url: {url}, data{payload}")
        res = self.post(url=url, json=payload)
        log.info(res)
        return res

    def post_sds_order(self, payload, device_category):
        """
        Create sales direct order for devices
        :param payload: payload for sales direct order for devices
        :param device_category: "COMPUTE" "NETWORK" "STORAGE"
        :return: JSON body
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/sales/direct/{device_category}"
        log.info(f"Going to POST sale direct order line data...url: {url}, data{payload}")
        res = self.post(url=url, json=payload)
        log.info(res)
        return res

    def post_lic_order(self, payload, device_category):
        """
        Create License order for devices
        :param payload: payload for License order for devices
        :param device_category: "COMPUTE" "NETWORK" "STORAGE"
        :return: JSON body
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/license/{device_category}"
        log.info(f"Going to POST manufacturing order line data...url: {url}, data{payload}")
        res = self.post(url=url, json=payload)
        log.info(res)
        return res

    def get_lic_order(self, device_category, objKey, get_status_code=False):
        """
        get License order for device
        :param device_category: "COMPUTE" "NETWORK" "STORAGE"
        :param objKey: unique objKey for the device
        :return: JSON body, status code
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/license/{device_category}/{objKey}"
        status_code, res  = self.get(url=url, tuple_response=True)
        log.info(res)
        if not get_status_code:
            return res
        else:
            return status_code, res

    def create_part_name(self, payload, device_category, objKey,delay=True):
        """
        Create part name for device
        :param payload: payload for part name for device
        :param device_category: "COMPUTE" "NETWORK" "STORAGE"
        :param objKey: unique objKey for the device
        :return: JSON body
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/part/{device_category}/{objKey}"
        res = self.post(url=url, json=payload)
        if delay:
            time.sleep(2)
        log.info(res)
        return res

    def get_part_name(self, device_category, objKey, get_status_code=False):
        """
        get part name for device
        :param device_category: "COMPUTE" "NETWORK" "STORAGE"
        :param objKey: unique objKey for the device
        :return: JSON body, status code
        """

        url = f"{self.base_url}{self.base_path}{self.api_version}/part/{device_category}/{objKey}"
        status_code, res = self.get(url=url, tuple_response=True)
        log.info(res)
        if not get_status_code:
            return res
        else:
            return status_code, res

    def create_platform(self, payload):
        """
        Create platform for device
        :param payload: payload for part name for device
        :return: JSON body
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/platform"
        res = self.post(url=url, json=payload)
        log.info(res)
        return res

    def get_platform(self, device_category, objKey, get_status_code=False):
        """
        get platform for device
        :param device_category: "COMPUTE" "NETWORK" "STORAGE"
        :param objKey: unique objKey for the device
        :return: JSON body, status code
        """

        url = f"{self.base_url}{self.base_path}{self.api_version}/platform/{device_category}/{objKey}"
        status_code, res = self.get(url=url, tuple_response=True)
        log.info(res)
        if not get_status_code:
            return res
        else:
            return status_code, res

    def update_mfr(self, payload, device_category, objKey):
        """
        Update existing manufacutring order
        :param payload: payload for update manufacuring order
        :param device_category: "COMPUTE" "NETWORK" "STORAGE"
        :param objKey: unique objKey for the device
        :return: JSON body
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/manufacturing/{device_category}/{objKey}"
        res = self.put(url=url, json=payload)
        log.info(res)
        return res

    def update_new_child(self, payload, device_category, objKey):
        """
        Update new child order for existing device order
        :param payload: payload for new child order for existing device order
        :param device_category: "COMPUTE" "NETWORK" "STORAGE"
        :param objKey: unique objKey for the device
        :return: JSON body
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/manufacturing/{device_category}/{objKey}/addChild"
        res = self.put(url=url, json=payload)
        log.info(res)
        return res

    def get_mfr_order_eth_mac(self, device_category, ethMac):
        """
        get manufacturing order by ethernet mac address
        :param device_category: "COMPUTE" "NETWORK" "STORAGE"
        :param ethMac: ethmac for the device
        :return: JSON body
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/manufacturing/{device_category}/ethMac/{ethMac}"
        res = self.get(url=url)
        log.info(res)
        return res

    def get_mfr_order_serial_number(self, device_category, Serial):
        """
        get manufacturing order by serial number
        :param device_category: "COMPUTE" "NETWORK" "STORAGE"
        :param serial: serial number for the device
        :return: JSON body
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/manufacturing/{device_category}/serial/{Serial}"
        res = self.get(url=url)
        log.info(res)
        return res

    def get_mfr_order_obj_key(self, device_category, objKey):
        """
        get manufacturing order by objKey
        :param device_category: "COMPUTE" "NETWORK" "STORAGE"
        :param serial: objKey for the device
        :return: JSON body
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/manufacturing/{device_category}/{objKey}"
        res = self.get(url=url)
        log.info(res)
        return res

    def get_device_configuration(self, location):
        """
        Get Device Configuration status for given key
        :param location: location of device
        :return: JSON body
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/device/config/status/{location}"
        res = self.get(url=url)
        log.info(res)
        return res

    def get_device_root_device_object(self, rootObjectKey):
        """
        get root device object
        :param rootObjectKey:object Key
        :return: JSON body
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/device/config/{rootObjectKey}"
        res = self.get(url=url)
        log.info(res)
        return res

    def create_new_device_configuration(self, payload):
        """
        Process new Device Configuration
        :param payload: payload for device
        :return: JSON body
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/device/config"
        res = self.post(url=url, json=payload)
        log.info(res)
        return res

    def get_sales_direct_order(self, device_category, objkey):
        """
        get sales direct order for devices
        :param device_category: "COMPUTE" "NETWORK" "STORAGE"
        :objkey unique obj key
        :return: JSON body
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/sales/direct/{device_category}/{objkey}"
        res = self.get(url=url)
        log.info(res)
        return res

    def get_point_of_sales_order(self, device_category, objkey):
        """
        Get point of sales order detas
        :param device_category: "COMPUTE" "NETWORK" "STORAGE"
        :param objkey unique obj key
        :return: JSON body
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/sales/pos/{device_category}/{objkey}"
        res = self.get(url=url)
        log.info(res)
        return res

    def update_sales_direct_order(self, payload, device_category, objkey):
        """
        Updates sales direct order for devices
        :param payload: payload for sales direct order for devices
        :param device_category: "COMPUTE" "NETWORK" "STORAGE"
        :param objkey unique obj key
        :return: JSON body
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/sales/direct/{device_category}/{objkey}"
        res = self.put(url=url, json=payload)
        log.info(res)
        return res

    def update_point_of_sales_order(self, payload, device_category, objkey):
        """
        Create point of sales order for devices
        :param payload: payload for point of sales order for devices
        :param device_category: "COMPUTE" "NETWORK" "STORAGE"
        :param objkey unique obj key
        :return: JSON body
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/sales/pos/{device_category}/{objkey}"
        res = self.put(url=url, json=payload)
        log.info(res)
        return res

    def create_sales_direct_order(self, payload, device_category):
        """
        Create sales direct order for devices
        :param payload: payload for sales direct order for devices
        :param device_category: "COMPUTE" "NETWORK" "STORAGE"
        :return: JSON body
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/sales/direct/{device_category}"
        res = self.post(url=url, json=payload)
        log.info(res)
        return res

    def create_point_of_sales_order(self, payload, device_category):
        """
        Create point of sales order for devices
        :param payload: payload for point of sales order for devices
        :param device_category: "COMPUTE" "NETWORK" "STORAGE"
        :return: JSON body
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/sales/pos/{device_category}"
        res = self.post(url=url, json=payload)
        log.info(res)
        return res

    def create_license_order(self, payload, device_category):
        """
        Create License order for devices
        :param payload: payload for License order for devices
        :param device_category: "COMPUTE" "NETWORK" "STORAGE"
        :return: JSON body
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/license/{device_category}"
        res = self.post(url=url, json=payload)
        log.info(res)
        return res

    def get_license_order(self, device_category, objKey):
        """
        get License order for device
        :param device_category: "COMPUTE" "NETWORK" "STORAGE"
        :param objKey: unique objKey for the device
        :return: JSON body
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/license/{device_category}/{objKey}"
        res = self.get(url=url)
        log.info(res)
        return res

    def update_license_order(self, device_category, objKey, payload):
        """
        update License order for device
        :param device_category: "COMPUTE" "NETWORK" "STORAGE"
        :param objKey: unique objKey for the device
        :param payload: payload for License order for devices

        :return: JSON body
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/license/{device_category}/{objKey}"
        res = self.put(url=url, json=payload)
        log.info(res)
        return res

    def update_part_number(self, category, number, payload):
        """
         update part list by using category and number
         :param path parameter : number part Required
         :param device_category: "COMPUTE" "NETWORK" "STORAGE"
         :param name: unique Part name
         :return: JSON body
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/part/{category}/{number}"
        res = self.put(url=url, json=payload)
        log.info(res)
        return res

    def get_all_matching_part(self, number, category=None, page=None, limit=None):
        """
         Get part list by using page number, size of page and part number
         :param path parameter : number  Required
         :param device_category: "COMPUTE" "NETWORK" "STORAGE"
         :param name: unique Part name
         :return: JSON body
        """
        params = {}
        if category:
            params[category] = category
        if page:
            params[page] = page
        if page:
            params[limit] = limit

        url = f"{self.base_url}{self.base_path}{self.api_version}/part/{number}"
        res = self.get(url=url, params=params)
        log.info(res)
        return res

    # def update_platform(self, mode, name, payload):
    #     """
    #      update platform for device
    #     :param payload: payload for part name for device
    #     :param mode  required "BLE" "COMPUTE" "LICENSE" "NETWORK" "STORAGE" "UNKNOWN"
    #     :param name required Platform name
    #     :return: JSON body
    #     """
    #     url = f"{self.base_url}{self.base_path}{self.api_version}/platform/{mode}/{name}"
    #     res = self.put(url=url, json=payload)
    #     log.info(res)
    #     return res

    def update_platform(self, payload, device_category, objKey, get_status_code=False):
        """
        Update the existing platform
        :param payload: payload for part name for device
        :param device_category
        :param objKey: Platform name
        :return: JSON body, status code
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/platform/{device_category}/{objKey}"
        status_code, res = self.put(url=url, tuple_response=True, json=payload)
        log.info(res)
        if not get_status_code:
            return res
        else:
            return status_code, res
