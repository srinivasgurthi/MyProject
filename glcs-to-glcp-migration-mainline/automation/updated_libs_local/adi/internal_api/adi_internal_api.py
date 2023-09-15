"""
Activate and device inventory internal apis
"""
import logging
import time
import uuid

from hpe_glcp_automation_lib.libs.commons.app_api.app_session import AppSession

log = logging.getLogger(__name__)


class ActivateInventoryInternal():
    """
    ActivateInventory Internal API Class
    """

    def __init__(self, host, sso_host):
        """
        Initialize ActivateInventory class
        :param host: cluster under test app api url
        :param sso_host: sso_host url
        """
        log.info("Initializing adi_app_api for user api calls")
        super().__init__(host, sso_host)
        self.base_path = "/activate-inventory/internal"
        self.api_version = "/v1"

        # deprecated API
        def claim_devices_with_serial_and_entitlement_id(self, platform_id, serial):
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
    
    def create_software_devices(self, pcid, device_type, part_number, serial_number, mac):
        """
         method to claim a serial in a platform customer account using internal api
         platform customer id is in the header of the request
        """
        url = f"{self.base_url}/activate-inventory/internal/v1/activate/softwareDevice"

        headers = {
            "CCS-Transaction-ID": uuid.uuid1().hex,
            "CCS-Platform-Customer-Id": pcid,
            "Content-Type": "application/json",
            }
        
        self.session.headers.update(headers)
        
        data = {
                "action": "register",
                "device": {
                    "device_type": device_type,
                    "serial_number": serial_number,
                    "mac_address": mac,
                    "part_number": part_number,
                    "device_model": device_type
                    },
                    "input_device_config_json": "string",
                    "device_description": "create_description"
                    }
               
        
        log.info(data)
        response = self.post(url = url, json=data, ignore_handle_response=True)
        
        return response
    
    def edit_device_tags_by_pcid(
            self, 
            pcid: str, 
            devices: list, 
            create_tags: list = None, 
            delete_tags: list = None, 
            only_validate: bool = None) -> dict:
        """
        Edit tags for devices belonging to the specified PCID.

        Args:
            pcid (str): The PCID of the platform customer whose devices' tags are being edited.
            devices (list): A list of devices to modify.
            create_tags (list, optional): A list of tags to create. Defaults to None.
            delete_tags (list, optional): A list of tags to delete. Defaults to None.
            only_validate (bool, optional): Only validate the request without actually modifying any tags. Defaults to None.

        Returns:
            dict: The API response.

        """

        # Set the API endpoint URL.
        url = f"{self.base_url}/activate-inventory/internal/v1/devices/tags"

        # Set the headers for the request.
        self.session.headers["CCS-Platform-Customer-Id"] = pcid
        self.session.headers["CCS-Transaction-ID"] = uuid.uuid1().hex
        self.session.headers["only_validate"] = only_validate

        # Build the payload for the request.
        payload = {}
        if devices:
            payload["devices"] = devices
        if create_tags:
            payload["create_tags"] = create_tags
        if delete_tags:
            payload["delete_tags"] = delete_tags

        # Log the payload.
        log.info(payload)

        # Send the request and store the response.
        response = self.put(url=url, json=payload, ignore_handle_response=True)

        # Return the response.
        return response
