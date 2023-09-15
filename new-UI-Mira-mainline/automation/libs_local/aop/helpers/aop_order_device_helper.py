"""
Helper function for Activate Order Processor App Api
"""
import datetime
import logging
import re

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

        if deviceType not in ["IAP", "SWITCH", "GATEWAY", "STORAGE", "COMPUTE"]:
            raise RuntimeError("Device device_category_IAP must be [\"IAP\", \"SWITCH\", \"GATEWAY\", "
                               "\"STORAGE\", \"COMPUTE\"]")

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

    def create_manufacturing(self, part):
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
        payload['manufacturing_data_list'][0]['parent_device']['eth_mac'] = self.macAddress
        payload['manufacturing_data_list'][0]['parent_device']['mfg_date'] = \
            datetime.datetime.strftime(datetime.datetime.today(), "%Y-%m-%d %H:%M:%S")
        try:
            self.order = ActivateOrder(self.app_api_host, self.sso_host, self.aop_client_id, self.aop_client_secret)
            res = self.order.post_manufacturing_order(payload, self.deviceCategory)
            log.info(res)
            log.info(payload)
            if res['code'] == 201:
                return self.serialNumber, self.macAddress
            else:
                return False

        except Exception as e:
            log.error("Failed to create manufacturing order with S/N {}".format(e))
            return False

    def create_pos_order(self):
        """
        Create point of sales order payload
        :return: boolean
        """
        pos_order_data = self.payload.pos_order_data()
        pos_order_data['point_of_sales_data_list'][0]['obj_key'] = 'AOP_ST_OBJKEY_' + self.serialNumber
        pos_order_data['point_of_sales_data_list'][0]['end_user_name'] = self.end_username
        pos_order_data['point_of_sales_data_list'][0]['invoice_date'] = \
            datetime.datetime.strftime(datetime.datetime.today(), "%Y-%m-%d %H:%M:%S")
        pos_order_data['point_of_sales_data_list'][0]['ship_date'] = \
            datetime.datetime.strftime(datetime.datetime.today(), "%Y-%m-%d %H:%M:%S")
        pos_order_data['point_of_sales_data_list'][0]['serial_number'] = self.serialNumber
        try:
            self.order = ActivateOrder(self.app_api_host, self.sso_host, self.aop_client_id, self.aop_client_secret)
            pos_order = self.order.post_point_of_sales_order(pos_order_data, self.deviceCategory)
            if pos_order['code'] == 201:
                return True
            else:
                return False
        except Exception as e:
            log.error("Failed to create create_pos_order order with S/N {}".format(e))
            return False

    def create_sds_order(self, part):
        """
        Create sales direct order payload
        :param part: Device part number
        :return: boolean
        """
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
        log.info("Received Category:" + self.deviceCategory + " SerialNumber:" + self.serialNumber +
                 " MacAddress:" + self.macAddress + " PartNumber:" + str(part))
        try:
            self.order = ActivateOrder(self.app_api_host, self.sso_host, self.aop_client_id, self.aop_client_secret)
            pos_direct_order = self.order.post_sds_order(sds_order_data, self.deviceCategory)
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
        log.info("Received Category:" + self.deviceCategory + " SerialNumber:" + self.serialNumber +
                 " MacAddress:" + self.macAddress + " PartNumber:" + str(part))
        try:
            self.order = ActivateOrder(self.app_api_host, self.sso_host, self.aop_client_id, self.aop_client_secret)
            self.order.post_lic_order(lic_order_payload, self.deviceCategory)
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

    def create_part_name(self):
        """
        Create part name for device
        :return: part name
        """
        part_data_payload = self.payload.part_data()
        objkey = 'AOP_ST_OBJKEY_' + self.serialNumber
        parent_prt = RandomGenUtils.random_string_of_chars(length=5, lowercase=False, uppercase=True)
        part_data_payload['part_data'][0]['parent_part']['part_number'] = parent_prt
        part_data_payload['part_data'][0]['parent_part']['part_category'] = self.deviceCategory
        part_data_payload['part_data'][0]['parent_part']['part_model'] = 'test_partModel'
        part_data_payload['part_data'][0]['parent_part']['address_use'] = False
        part_data_payload['part_data'][0]['parent_part']['parent_part_number'] = 'IGNORED'
        part_data_payload['part_data'][0]['child_parts'][0]['part_number'] = \
            RandomGenUtils.random_string_of_chars(length=5, lowercase=False, uppercase=True)
        part_data_payload['part_data'][0]['child_parts'][0]['part_category'] = self.deviceCategory
        part_data_payload['part_data'][0]['child_parts'][0]['address_use'] = False
        part_data_payload['part_data'][0]['child_parts'][0]['parent_part_number'] = parent_prt
        try:
            self.order = ActivateOrder(self.app_api_host, self.sso_host, self.aop_client_id, self.aop_client_secret)
            create_part = self.order.create_part_name(part_data_payload, self.deviceCategory, objkey)
            if create_part['code'] == 201:
                return parent_prt
        except Exception as e:
            log.info("Failed to create_part_name order with S/N {}".format(e))
            return False

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
        try:
            self.order = ActivateOrder(self.app_api_host, self.sso_host, self.aop_client_id, self.aop_client_secret)
            create_platform_resp = self.order.create_platform(platform_data_payload)
            if create_platform_resp['code'] == 201:
                return True
        except Exception as e:
            log.info("Failed to create create_platform order with S/N {}".format(e))
            return False
