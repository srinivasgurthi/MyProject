"""
Helper function for Activate Order Processor App Api
"""
import datetime
import logging
import re
import time

from hpe_glcp_automation_lib.libs.aop.app_api.aop_app_api import ActivateOrder
from hpe_glcp_automation_lib.libs.aop.helpers.aop_payload_constants import AopInputPayload
from hpe_glcp_automation_lib.libs.commons.utils.random_gens import RandomGenUtils

log = logging.getLogger(__name__)


class NewDeviceOrder:
    """
    Helper class for Activate Order Processor App Api Class
    """

    def __init__(self,
                 app_api_host,
                 deviceCategory,
                 deviceType,
                 serialNumber,
                 macAddress,
                 cluster,
                 endUsername,
                 sso_host,
                 aop_client_id,
                 aop_client_secret
                 ):
        """
        Initialize NewDeviceOrder class
        :param  app_api_host: App api hostname for cluster
        :param deviceCategory: "COMPUTE" "NETWORK" "STORAGE"
        :param deviceType: IAP, SWITCH, STORAGE, COMPUTE
        :param serialNumber: Device serial number
        :param macAddress: Device mac address
        :param cluster: cluster under test
        :param endUsername: end username same used customer alias for activate inventory
        :param sso_host: sso_host
        :param aop_client_id: aop_client_id
        :param aop_client_secret: aop_client_secret
        """
        if not deviceType:
            raise RuntimeError("Device device_type IAP, or SWITCH, or GATEWAY is required...")

        if deviceType not in ["IAP", "SWITCH", "GATEWAY", "STORAGE", "COMPUTE", "NETWORK"]:
            raise RuntimeError("Device device_category_IAP must be [\"IAP\", \"SWITCH\", \"GATEWAY\", "
                               "\"STORAGE\", \"COMPUTE\", \"NETWORK\"]")

        if not serialNumber:
            raise RuntimeError("Device serial number is required...")

        SERIAL_NUMBER_LENGTH = 20
        if len(serialNumber) > SERIAL_NUMBER_LENGTH:
            raise RuntimeError("Device serial number length should be upto 20 characters...")

        if not macAddress:
            raise RuntimeError("Device mac address is required...")

        MAC_REGEX = "^([0-9a-fA-F]{2})(:[0-9a-fA-F]{2}){5}$"
        if not re.match(MAC_REGEX, macAddress):
            raise RuntimeError(
                "Device mac address is invalid (Expected pattern:\"^([0-9a-fA-F]{2})(:[0-9a-fA-F]{2}){5}$\")")

        self.payload = AopInputPayload()
        self.deviceCategory = deviceCategory
        self.device_type = deviceType
        self.serialNumber = serialNumber
        self.macAddress = macAddress
        self.cluster = cluster
        self.app_api_host = app_api_host
        self.end_username = endUsername
        self.sso_host = sso_host
        self.aop_client_id = aop_client_id
        self.aop_client_secret = aop_client_secret
        self.order = ActivateOrder(self.app_api_host,
                                   self.sso_host,
                                   self.aop_client_id,
                                   self.aop_client_secret)

    def create_manufacturing(self, part, part_category=None):
        """
        Create manufacturing payload and make manufacture call
        :param part: Device part number
        :return: serial number, macaddress
        """

        log.info("Received device_type:" + self.device_type + " SerialNumber:" + self.serialNumber +
                 " MacAddress:" + self.macAddress + " PartNumber:" + str(part))
        payload = self.payload.mfr_payload_data()
        payload['manufacturing_data_list'][0]['parent_device']['obj_key'] = 'AOP_ST_OBJKEY_' + self.serialNumber
        payload['manufacturing_data_list'][0]['parent_device']['serial_number'] = self.serialNumber
        payload['manufacturing_data_list'][0]['parent_device']['part_number'] = part
        payload['manufacturing_data_list'][0]['parent_device']['part_category'] = self.device_type
        payload['manufacturing_data_list'][0]['parent_device']['device_type'] = self.device_type
        if part_category:
            payload['manufacturing_data_list'][0]['parent_device']['part_category'] = part_category

        if part_category:
            valid_device_type = ["ALS", "AP", "BLE", "COMPUTE", "CONTROLLER", "DHCI_COMPUTE", "DHCI_STORAGE",
                                      "EINAR", "EINR", "GATEWAY", "IAP", "LTE_MODEM", "MC", "STORAGE", "SWITCH",
                                      "NW_THIRD_PARTY", "UNKNOWN"]
            if self.device_type not in valid_device_type:
                payload['manufacturing_data_list'][0]['parent_device']['device_type'] = part_category

        payload['manufacturing_data_list'][0]['parent_device']['eth_mac'] = self.macAddress
        payload['manufacturing_data_list'][0]['parent_device']['mfg_date'] = \
            datetime.datetime.strftime(datetime.datetime.today(), "%Y-%m-%d %H:%M:%S")
        log.info("Manufacturing payload %s :",payload)

        try:
            self.order = ActivateOrder(self.app_api_host, self.sso_host, self.aop_client_id, self.aop_client_secret)
            res = self.order.post_manufacturing_order(payload, self.deviceCategory)
            time.sleep(2)
            log.info(res)
            log.info(payload)
            if res['code'] == 201:
                return self.serialNumber, self.macAddress
            else:
                return False

        except Exception as e:
            log.error("Failed to create manufacturing order with S/N {}".format(e))
            return False

    def create_pos_order(self, part=None, check_emdm=None):
        """
        Create point of sales order payload
        part is optional in this call, as few of existing test cases calls in that way
        :return: boolean
        """
        pos_order_data = self.payload.pos_order_data()
        pos_order_data['point_of_sales_data_list'][0]['obj_key'] = 'AOP_ST_OBJKEY_' + self.serialNumber
        pos_order_data['point_of_sales_data_list'][0]['end_user_name'] = self.end_username
        pos_order_data['point_of_sales_data_list'][0]['invoice_date'] = \
            datetime.datetime.strftime(datetime.datetime.today(), "%Y-%m-%d %H:%M:%S")
        pos_order_data['point_of_sales_data_list'][0]['ship_date'] = \
            datetime.datetime.strftime(datetime.datetime.today(), "%Y-%m-%d %H:%M:%S")
        pos_order_data['point_of_sales_data_list'][0]['pos_id'] = 'AOP_ST_posID_' + self.serialNumber
        pos_order_data['point_of_sales_data_list'][0]['serial_number'] = self.serialNumber
        """
        Added below 4 in JSON path - incase of Max Params
        """
        if part:
            pos_order_data['point_of_sales_data_list'][0]['part_number'] = part

        if check_emdm == 'emdm_party':
            log.info(f"Choose {check_emdm} removing emdm party list")
            del pos_order_data['point_of_sales_data_list'][0]['emdm_party_list']

        if check_emdm == 'emdm_party_list':
            log.info(f"Choose {check_emdm} Removing emdm party")
            del pos_order_data['point_of_sales_data_list'][0]['emdm_party']

        log.info("Payload pos: %s",pos_order_data)
        try:
            self.order = ActivateOrder(self.app_api_host, self.sso_host, self.aop_client_id, self.aop_client_secret)
            pos_order = self.order.post_point_of_sales_order(pos_order_data, self.deviceCategory)
            time.sleep(2)
            if pos_order['code'] == 201:
                return True
            else:
                return False
        except Exception as e:
            log.error("Failed to create create_pos_order order with S/N {}".format(e))
            return False

    def create_sds_order(self, part, check_emdm=None):
        """
        Create sales direct order payload
        :param part: Device part number
        :return: boolean
        """
        log.info("Checking emdm type %s", check_emdm)
        sds_order_data = self.payload.sds_order_data()
        sds_order_data['sales_direct_shipment_data_list'][0]['obj_key'] = 'AOP_OBJKEY_ST' + self.serialNumber
        sds_order_data['sales_direct_shipment_data_list'][0]['serial_number'] = self.serialNumber
        sds_order_data['sales_direct_shipment_data_list'][0]['end_user_name'] = self.end_username
        sds_order_data['sales_direct_shipment_data_list'][0]['invoice_date'] = datetime.datetime.strftime(
            datetime.datetime.today(), "%Y-%m-%d %H:%M:%S")
        sds_order_data['sales_direct_shipment_data_list'][0]['ship_date'] = datetime.datetime.strftime(
            datetime.datetime.today(), "%Y-%m-%d %H:%M:%S")
        sds_order_data['sales_direct_shipment_data_list'][0]['purchase_order_date'] = datetime.datetime.strftime(
            datetime.datetime.today(), "%Y-%m-%d %H:%M:%S")
        sds_order_data['sales_direct_shipment_data_list'][0]['part_number'] = part

        if check_emdm == 'emdm_party':
            log.info(f"Choose {check_emdm} removing emdm party list")
            del sds_order_data['sales_direct_shipment_data_list'][0]['emdm_party_list']

        if check_emdm == 'emdm_party_list':
            log.info(f"Choose {check_emdm} Removing emdm party")
            del sds_order_data['sales_direct_shipment_data_list'][0]['emdm_party']

        log.info("Received Category:" + self.deviceCategory + " SerialNumber:" + self.serialNumber +
                 " MacAddress:" + self.macAddress + " PartNumber:" + str(part))

        try:
            self.order = ActivateOrder(self.app_api_host, self.sso_host, self.aop_client_id, self.aop_client_secret)
            log.info("Payload %s", sds_order_data)
            log.info("Device Category %s", self.deviceCategory)
            pos_direct_order = self.order.post_sds_order(sds_order_data, self.deviceCategory)
            time.sleep(2)
            if pos_direct_order['code'] == 201:
                return True
            else:
                return False
        except Exception as e:
            log.error("Failed to create create_sds_order order with S/N {}".format(e))
            return False

    def create_lic_order(self, part):
        """
        Create license order payload and make license order call
        :param part: Device part number
        :return: subscription_key
        """
        lic_order_payload = self.payload.lic_order_data()
        lic_order_payload['obj_key'] = 'AOP_OBJKEY_ST' + self.serialNumber
        lic_order_payload['reason'] = "Creation"
        lic_order_payload['quote'] = \
            RandomGenUtils.random_string_of_chars(length=4, lowercase=False, uppercase=True, digits=True)
        lic_order_payload["entitlements"][0]["line_item"] = \
            RandomGenUtils.random_string_of_chars(length=3, lowercase=False, uppercase=True, digits=True)
        lic_order_payload["entitlements"][0]["licenses"][0]["device_serial_number"] = self.serialNumber
        lic_order_payload["entitlements"][0]["licenses"][0]["subscription_key"] = \
            RandomGenUtils.random_string_of_chars(length=5, lowercase=False, uppercase=True, digits=True)
        lic_order_payload["entitlements"][0]["licenses"][0]["end_user_name"] = self.end_username
        lic_order_payload["activate"]["sono"] = \
            RandomGenUtils.random_string_of_chars(length=5, lowercase=False, uppercase=True, digits=True)
        lic_order_payload["activate"]["po"] = \
            RandomGenUtils.random_string_of_chars(length=5, lowercase=False, uppercase=True, digits=True)
        lic_order_payload["activate"]["end_user_name"] = self.end_username
        lic_order_payload["entitlements"][0]["product"]["sku"] = part

        log.info("Received Category:" + self.deviceCategory + " SerialNumber:" + self.serialNumber +
                 " MacAddress:" + self.macAddress + " PartNumber:" + str(part))
        log.info("license payload : %s",lic_order_payload)
        log.info("Device Category : %s", self.deviceCategory)
        try:
            self.order = ActivateOrder(self.app_api_host, self.sso_host, self.aop_client_id, self.aop_client_secret)
            self.order.post_lic_order(lic_order_payload, self.deviceCategory)
            time.sleep(2)
            get_lic_order_resp = self.order.get_lic_order(self.deviceCategory,
                                                          lic_order_payload['obj_key'])
            if get_lic_order_resp['entitlements'][0]['licenses'][0]['subscription_key'] is not None:
                log.info(get_lic_order_resp)
                return get_lic_order_resp['entitlements'][0]['licenses'][0]['subscription_key']
            else:
                log.error("Failed to create create_lic_order order with S/N {}".format(e))
                return False
        except Exception as e:
            log.info("Failed to create create_lic_order order with S/N {}".format(e))
            return False

    def create_part_name(self, part_category=None, include_child_part=False):
        """
        Create part name for device
        :return: part name
        """

        part_data_payload = self.payload.part_data()
        objkey = 'AOP_ST_OBJKEY_' + self.serialNumber
        parent_prt = RandomGenUtils.random_string_of_chars(length=5, lowercase=False, uppercase=True)
        part_data_payload['part_data'][0]['parent_part']['part_number'] = parent_prt
        part_data_payload['part_data'][0]['parent_part']['part_category'] = self.deviceCategory
        if part_category:
            part_data_payload['part_data'][0]['parent_part']['part_category'] = part_category
        part_data_payload['part_data'][0]['parent_part']['part_model'] = 'test_partModel'
        part_data_payload['part_data'][0]['parent_part']['address_use'] = False
        part_data_payload['part_data'][0]['parent_part']['parent_part_number'] = 'IGNORED'

        if include_child_part:
            log.info("Inside Child part name %s", include_child_part)
            part_data_payload['part_data'][0]['child_parts'][0]['part_number'] = \
                RandomGenUtils.random_string_of_chars(length=5, lowercase=False, uppercase=True)
            part_data_payload['part_data'][0]['child_parts'][0]['part_category'] = self.deviceCategory
            if part_category:
                part_data_payload['part_data'][0]['child_parts'][0]['part_category'] = part_category

            part_data_payload['part_data'][0]['child_parts'][0]['address_use'] = False
            part_data_payload['part_data'][0]['child_parts'][0]['parent_part_number'] = parent_prt
        else:
            del part_data_payload['part_data'][0]['child_parts']

        try:
            log.info("Payload %s ",part_data_payload)
            log.info("Device Category %s ",self.deviceCategory)
            log.info("Platform cbject Key %s ", objkey)
            self.order = ActivateOrder(self.app_api_host, self.sso_host, self.aop_client_id, self.aop_client_secret)
            create_part = self.order.create_part_name(part_data_payload, self.deviceCategory, objkey)
            if create_part['code'] == 201:
                log.info("Parent Part %s", parent_prt)
                return parent_prt
            else:
                return False
        except Exception as e:
            log.info("Failed to create_part_name order with S/N {}".format(e))
            return False


    def get_part_name(self, part):
        """
            Get Part name for device
            :return: boolean, response
        """
        try:
            self.order = ActivateOrder(self.app_api_host, self.sso_host, self.aop_client_id, self.aop_client_secret)
            status_code, get_part_resp = self.order.get_part_name(self.deviceCategory, part, get_status_code=True)
            log.info("get response: %s", get_part_resp)
            if status_code == 200:
                return (True, get_part_resp)
        except Exception as e:
            log.info("Failed to get part number".format(e))
            return (False, None)

    def get_platform(self):
        """
            Get platform for device
            :return: boolean
        """
        objkey = 'AOP_ST_OBJKEY_' + self.serialNumber
        try:
            self.order = ActivateOrder(self.app_api_host, self.sso_host, self.aop_client_id, self.aop_client_secret)
            status_code, get_platform_resp = self.order.get_platform(self.deviceCategory, objkey, get_status_code=True)
            log.info("get response: %s",get_platform_resp)
            if status_code == 200:
                return (True, get_platform_resp)
        except Exception as e:
            log.info("Failed to get platform".format(e))
            return (False, None)

    def create_platform(self):
        """
        Create platform for device
        :return: boolean
        """
        platform_data_payload = self.payload.platform_data()
        platform_data_payload["platform_list"][0]["name"] = 'AOP_ST_OBJKEY_' + self.serialNumber
        platform_data_payload["platform_list"][0]["mode"] = self.device_type
        platform_data_payload["platform_list"][0]["xref"] = "aop_network_baseOS_1"
        platform_data_payload["platform_list"][0]["description"] = "aop_st_platform_add_compute"

        """
        Regex validation to check xref contains only alphanumeric, underscore
        """
        xref_regex = re.compile(r'^\w+$')
        if xref_regex.match(platform_data_payload["platform_list"][0]["xref"]):
            try:
                self.order = ActivateOrder(self.app_api_host, self.sso_host, self.aop_client_id, self.aop_client_secret)
                create_platform_resp = self.order.create_platform(platform_data_payload)
                if create_platform_resp['code'] == 201:
                    return True
            except Exception as e:
                log.info("Failed to create create_platform order with S/N {}".format(e))
                return False
        else:
            log.info("{} Error: Invalid character in xref field".format(platform_data_payload["platform_list"][0]["xref"]))

    def update_platform(self, update_type=''):
        """
            Update platform for device
            :return: boolean, put_platform_resp
        """
        objkey = 'AOP_ST_OBJKEY_' + self.serialNumber
        rand_string_details = {"length": 3, "lowercase": False, "uppercase": True, "digits": True}
        platform_data_payload = self.payload.platform_data()
        platform_data_payload["platform_list"][0]["name"] = objkey
        platform_data_payload["platform_list"][0]["mode"] = self.deviceCategory
        platform_data_payload["platform_list"][0]["xref"] = "aop_network_baseOS_1"
        platform_data_payload["platform_list"][0]["description"] = "aop_st_platform_add_compute"

        if "name" in update_type:
            platform_data_payload["platform_list"][0].update({
                "name": objkey + RandomGenUtils.random_string_of_chars(**rand_string_details)
            })

        if "mode" in update_type:
            platform_data_payload["platform_list"][0].update({
                "mode": "COMPUTE"
            })

        if "xref" in update_type:
            platform_data_payload["platform_list"][0].update({
                "xref": "aop_network_baseOS_1" + RandomGenUtils.random_string_of_chars(**rand_string_details)
            })

        if "code" in update_type:
            platform_data_payload["platform_list"][0].update({
                "code": RandomGenUtils.random_string_of_chars(length=7, lowercase=False, uppercase=False, digits=True)
            })

        if "name_and_mode" in update_type:
            platform_data_payload["platform_list"][0].update({
                "name": objkey + RandomGenUtils.random_string_of_chars(**rand_string_details),
                "mode": "COMPUTE"
            })

        try:
            self.order = ActivateOrder(self.app_api_host, self.sso_host, self.aop_client_id, self.aop_client_secret)
            putpayload = platform_data_payload["platform_list"][0]
            log.info("put payload: %s", putpayload)
            status_code, put_platform_resp = self.order.update_platform(putpayload, self.deviceCategory, objkey, get_status_code=True)
            log.info("put response: %s", put_platform_resp)
            if status_code == 200:
                return (True, put_platform_resp)
        except Exception as e:
            log.info("Failed to update platform details".format(e))
            return (False, None)

    def get_lic_order(self):
        obj_key = 'AOP_OBJKEY_ST' + self.serialNumber
        log.info("Device Category : %s", self.deviceCategory)
        log.info("Object key :%s", obj_key)
        try:
            self.order = ActivateOrder(self.app_api_host, self.sso_host, self.aop_client_id, self.aop_client_secret)
            status_code, get_lic_order_resp = self.order.get_lic_order(self.deviceCategory, obj_key, get_status_code=True)
            if status_code == 200:
                log.info("get license response: %s", get_lic_order_resp)
                return True, get_lic_order_resp
        except Exception as e:
            log.info("Failed to create create_lic_order order with S/N {}".format(e))
            return False, None
