"""
Payloads templates for Activate Order Processor App Api
"""
import logging
from logging import DEBUG

from hpe_glcp_automation_lib.libs.commons.utils.random_gens import RandomGenUtils

log = logging.getLogger(__name__)

class AopInputPayload(object):
    pod_namespace: str = ""
    log_level = DEBUG

    def mfr_payload_data(self):
        log.info("loading")
        '''
        parent_serial_number is not required, nor present in documentation
        device_type is deprecated field.
        '''
        mfr_payload = {
            'manufacturing_data_list': [
                {
                    'parent_device': {
                        'obj_key': "obj_key",
                        'serial_number': "serial_number",
                        'part_number': "part_number",
                        'part_category': "part_category",
                        'eth_mac': "eth_mac",
                        'mfg_date': "mfg_date",
                        'device_type': "device_type"
                    }
                }
            ]
        }
        return mfr_payload

    def pos_order_data(self):
        pos_order_payload = {
            'point_of_sales_data_list': [
                {
                    "obj_key": "AOP_ST_OBJKEY_",
                    "pos_id": "AOP_ST_posID_",
                    "invoice_date": "2021-02-25 01:54:52",
                    "ship_date": "2021-02-25 01:54:52",
                    "reseller_name": "AOP_ST_reseller",
                    "end_user_name": "AOP_ST_end_user",
                    "part_number": "PLACEHOLDER",
                    "quantity": 1,
                    "ext_cost": 10000,
                    "invoice_no": "AOP_ST_invoice_",
                    "order_no": "AOP_ST_order_",
                    "line_no": 1,
                    "line_type": "IN",
                    "distributor_po_no": "AOP_ST_distributor_po_no_",
                    "serial_number": "AOPST",
                    "us_zip": "95001",
                    "source": "AOP_ST_source",
                    "emdm_party": {
                        "id": "string",
                        "function": "AG",
                        "country_id": "string",
                        "global_id": "string"
                    },
                    "emdm_party_list": [
                        {
                            "id": "string",
                            "function": "AG",
                            "country_id": "string",
                            "global_id": "string"
                        }
                    ]
                }
            ]
        }
        return pos_order_payload

    def sds_order_data(self):
        sds_order_payload = {
            'sales_direct_shipment_data_list': [
                {
                    'obj_key': "obj_key",
                    "sono": "sono",
                    'part_number': "part_number",
                    'part_description': 'PLACEHOLDER',
                    'serial_number': "serial_number",
                    "sold_to": "AOP_ST_Customer",
                    "sold_to_name": "AOP_ST_Customer_sold_to_name",
                    "sold_to_email": "AOP_ST_Customer@email.com",
                    "ship_to": "AOP_ST_Customer_ship_to",
                    "ship_to_name": "AOP_ST_Customer_ship_to_name",
                    "ship_to_email": "AOP_ST_Customer_ship@email.com",
                    "end_user": "AOP_ST_Customer",
                    "end_user_name": "AOP_ST_end_user",
                    "end_user_email": "AOP_ST_end_user@email.com",
                    "reseller": "AOP_ST_reseller",
                    "reseller_name": "AOP_ST_reseller_name",
                    "reseller_email": "AOP_ST_reseller@email.com",
                    'purchase_order_date': '2021-02-25 01:54:52',
                    "order_class": "NON-BRIM",
                    'customer_po': 'PLACEHOLDERFFZAH',
                    'ship_date': '2021-02-25 01:54:52',
                    "emdm_party": {
                        "id": "string",
                        "function": "AG",
                        "country_id": "string",
                        "global_id": "string"
                    },
                    "emdm_party_list": [
                        {
                            "id": "string",
                            "function": "AG",
                            "country_id": "string",
                            "global_id": "string"
                        }
                    ]
                }
            ]
        }
        return sds_order_payload

    def lic_order_data(self):
        lic_order_payload = {
            "obj_key": "AOP_ST_OBJKEY_",
            "reason": "Creation",
            "quote": "AOPSTQ",
            "entitlements": [
                {
                    "line_item": "AOPSTLI",
                    "licenses": [
                        {
                            "subscription_key": "AOPSTSUBKEY",
                            "device_serial_number": "PLACEHOLDER",
                            "qty": "999",
                            "available_qty": "10.50",
                            "capacity": "2000GB",
                            "appointments": {
                                "term": "10DAYS",
                                "subscription_start": "2021-02-23 20:48:30",
                                "subscription_end": "2024-02-23 20:48:30",
                                "delayed_activation": "2021-03-23 20:48:30"
                            }
                        }
                    ],
                    "product": {
                        "sku": "AOP_ST_PART_NO",
                        "description": "AOP_ST_SKU_DESCRIPTION_STRING --------------------------------------"
                    }
                }
            ],
            "activate": {
                "sono": "AOPSTSONO",
                "sold_to": "AOP_ST_Customer",
                "sold_to_name": "AOP_ST_Customer_sold_to_name",
                "sold_to_email": "AOP_ST_Customer@email.com",
                "ship_to": "AOP_ST_Customer_ship_to",
                "ship_to_name": "AOP_ST_Customer_ship_to_name",
                "ship_to_email": "AOP_ST_Customer_ship@email.com",
                "end_user": "AOP_ST_Customer",
                "end_user_name": "AOP_ST_end_user",
                "end_user_email": "AOP_ST_end_user@email.com",
                "reseller": "AOP_ST_reseller",
                "reseller_name": "AOP_ST_reseller_name",
                "reseller_email": "AOP_ST_reseller@email.com",
                "po": "AOP_ST_PO_",
                "order_class": "NON-BRIM",
                "party": {
                    "id": "AOP_STPID",
                    "country_id": "AOP_STCID",
                    "global_id": "AOP_STGID"
                }
            }
        }
        return lic_order_payload

    def platform_data(self):
        platform_data_payload = {
            "platform_list": [
                {
                    "name": "platform_name",
                    "mode": "Device_type",
                    "xref": "aop_st_xref",
                    "description": "aop_st_platform_desc"
                }
            ]
        }
        return platform_data_payload

    def part_data(self):
        part_data_payload = {
            "part_data": [{
                "parent_part": {
                    "part_number": "PRT_Part_Num",
                    "part_category": "Dev_Category",
                    "part_model": "test_partModel",
                    "description": "testPartDescription",
                    "address_use": False,
                    "parent_part_number": "IGNORED"
                },
                "child_parts": [{
                    "part_number": "CHLD_Part_Num",
                    "part_category": "Dev_Category",
                    "part_model": "test_child_partModel",
                    "description": "testChildPartDescription",
                    "address_use": False,
                    "parent_part_number": "PRT_Part_Num"
                }]
            }]
        }
        return part_data_payload


class AOPDeviceConstants(object):
    def __init__(self):
        log.info("Initialize AOPDeviceConstants")

    def new_mfr_device_constants(self):
        rand_string_details = {"length": 5, "lowercase": False, "uppercase": True, "digits": True}
        new_device_constants = {
            'IAP_serial': "STIAP" + RandomGenUtils.random_string_of_chars(**rand_string_details),
            'SWITCH_serial': "STSWI" + RandomGenUtils.random_string_of_chars(**rand_string_details),
            'GATEWAY_serial': "STGWA" + RandomGenUtils.random_string_of_chars(**rand_string_details),
            'STORAGE_serial': "BA_" + RandomGenUtils.random_string_of_chars(**rand_string_details),
            "COMPUTE_serial": "COM_" + RandomGenUtils.random_string_of_chars(**rand_string_details),
            'NETWORK_serial': "NET_" + RandomGenUtils.random_string_of_chars(**rand_string_details),
            'IAP_mac': RandomGenUtils.generate_random_MAC_address(),
            'SWITCH_mac': RandomGenUtils.generate_random_MAC_address(),
            'GATEWAY_mac': RandomGenUtils.generate_random_MAC_address(),
            'STORAGE_mac': RandomGenUtils.generate_random_MAC_address(),
            'COMPUTE_mac': RandomGenUtils.generate_random_MAC_address(),
            'NETWORK_mac': RandomGenUtils.generate_random_MAC_address(),
            'MAC_REGEX': "^([0-9a-fA-F]{2})(:[0-9a-fA-F]{2}){5}$",
            'SERIAL_NUMBER_LENGTH': 20,
            'device_category_nw': 'NETWORK',
            'device_category_compute': 'COMPUTE',
            'device_category_storage': 'STORAGE',
            'device_category_IAP': 'IAP',
            'device_category_SWITCH': 'SWITCH',
            'device_category_GATEWAY': 'GATEWAY',
            'DEFAULT_PART_MAP': {
                "SWITCH": "JL255A",
                "IAP": "JW242AR",
                "GATEWAY": "7005-RW"
            }
        }
        return new_device_constants
