import json
import logging
import time
log = logging.getLogger(__name__)
from hpe_glcp_automation_lib.libs.authn.user_api.session.ui.uisession import UISession

class UIDoorway(UISession):
    def __init__(self, host, user, password, pcid):
        """
        :param host: CCS UI Hostname
        :param user: Login Credentials - Username
        :param password: Login Credentials - Password
        :param pcid: Platform Customer ID
        :param appid: Application ID
        """
        self.pcid = pcid
        super(UIDoorway, self).__init__(host, user, password)
        UIDoorway.login(self)
        self.load_account(pcid)
        self.accounts = None

    def _get_path(self, path):
        return f"{self.base_path}{self.api_version}{path}"

    def load_account(self, platform_customer_id):
        """
        Load into a Platform Customer Account
        :param platform_customer_id: Platform Customer ID
        :return:
        """
        self.get(f"/authn/v1/session/load-account/{platform_customer_id}")

    def role_assign(self, platform_cust_id, invited_username, role_data):
        """
        Create role in authz
        :param platform_cid: Platform Customer ID
        :param application_id: Application ID
        :role_data: Details of the role to assign
        :return: response_code, response body
        """
        logging.info("Role_assign")
        return self.put(f"/authorization/ui/v1/customers/{platform_cust_id}/users/{invited_username}/roles",
                        data=json.dumps(role_data))

        # logging.info("Role_assign")
        # return self.post(f"/authorization/ui/v1/customers/{platform_cust_id}/assign_roles",
        #     data=json.dumps(role_data)
        # )

    def role_unassign(self, platform_cust_id, user_name, application_id, role_slug):
        """
        Update an role in authz
        :param platform_cid: Platform Customer ID
        :param application_id: Application ID
        :role_data: Details to update for the role
        :return: response_code, response body
        """
        log.info("Role_unassign")

        role_data = {"delete":[{"application_id": application_id, "slug": role_slug}]}
        return self.put(f"/authorization/ui/v1/customers/{platform_cust_id}/users/{user_name}/roles", data=json.dumps(role_data))

    def create_role_for_app(self, application_id, platform_cust_id, role_data):
        logging.info("role_data {}".format(role_data))
        return self.post(f"/authorization/ui/v1/customers/{platform_cust_id}/applications/{application_id}/roles",
                         data=json.dumps(role_data))

    def role_delete(self, platform_cid, application_id, role_slug):
        """
        Delete an role from authz
        :param platform_cid: Platform Customer ID
        :param application_id: Application ID
        :role_slug: Slug for the role to delete
        :return: response_code, response body
        """
        return self.delete(f"/authorization/ui/v1/customers/{platform_cid}/applications/{application_id}/roles/{role_slug}")

    def ccs_get_role(self, platform_cust_id, secondary=None):
        logging.info("Get Role")
        if secondary:
            return self.get_secondary(f"/authorization/ui/v1/customers/{platform_cust_id}/roles")
        else:
            self.get(f"/authorization/ui/v1/customers/{platform_cust_id}/roles")

    def app_get_role(self, platform_cust_id, application_id, secondary=None):
        logging.info("Get Role")
        if secondary:
            return self.get_secondary(f"/authorization/ui/v1/customers/{platform_cust_id}/applications/{application_id}/roles")
        else:
            return self.get(f"/authorization/ui/v1/customers/{platform_cust_id}/applications/{application_id}/roles")

    def add_device_activate_inventory_emdm(self, device_list,dev_cat=None):
        """
        Add device to activate inventory
        :param serial_number: Serial number of device
        :param mac_address: Mac address of device
        :return:
        """
        devlist = []
        if dev_cat:
            for dev in device_list:
                new_dev = {}
                new_dev['mac_address'] = dev['device_1']['eth_mac']
                new_dev['serial_number'] = dev['device_1']['serial_no']
                new_dev['app_category'] = dev_cat
                devlist.append(new_dev)
        devices = {}
        devices['devices']= devlist
        headers = {'Content-type': 'application/json'}
        time.sleep(3)
        result = self.post("/ui-doorway/ui/v1/activate/devices", data=json.dumps(devices), headers=headers)
        log.info("add device inventory result {}".format(result))
        return result

    def verify_add_device_activate_inventory_emdm(self, device_list,dev_cat=None):
        """
        Add device to activate inventory
        :param serial_number: Serial number of device
        :param mac_address: Mac address of device
        :return:
        """
        mac = device_list[0]['device_1']['eth_mac']
        result = self.get("/ui-doorway/ui/v1/activate/devices?mac_address={}".format(mac))
        log.info("Get device inventory result {}".format(result))
        return result

    def add_device_activate_inventory(self, device_list):
        """
        Add device to activate inventory
        :param serial_number: Serial number of device
        :param mac_address: Mac address of device
        :return:
        """
        headers = {'Content-type': 'application/json'}
        result = self.post("/ui-doorway/ui/v1/devices", data=json.dumps(device_list), headers=headers)
        log.info("add device inventory result {}".format(result))
        return result

    def list_devices(self, secondary=None):
        """
        List devices of customer in activate inventory
        :param tenant_pcid: Platform customer id of tenant to list devices
            of a tenant, from an MSP account
        :return: list of devices
        """
        if secondary:
            return self.get_secondary("/ui-doorway/ui/v1/devices")
        else:
            return self.get("/ui-doorway/ui/v1/devices")

    def assign_devices_to_app_in_activate_inventory(self, device_list, appid, application_instance_id):
        """
        Assign devices to app in activate inventory
        :param device_list: list of devices to be unassigned (limit 500)
            Example device_list: [{"serial_number":"APSNMR-01","device_type":"AP","part_number":"NWPRTTR01"}]
        :param app_instance_id: application instance id for device assignment
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
        result = self.post("/ui-doorway/ui/v1/devices/application-instance", data=json.dumps(data), headers=headers)
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
        result = self.delete("/ui-doorway/ui/v1/devices/application-instance", data=json.dumps(data), headers=headers)
        log.info("unassign devices output result {}".format(result))
        return result

    def get_licenses(self, secondary=None):
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
        log.info(f"Executing GET on request URL: /ui-doorway/ui/v1/license/devices")
        if secondary:
            return self.post_secondary("/ui-doorway/ui/v1/license")
        else:
            return self.post("/ui-doorway/ui/v1/license")

    def assign_license_to_devices(self, license_device_tupl_list, device_type, part_number):
        """
        Assign device to respective license
        :param license_device_tupl_list: List of tuple of serial number and subscription key
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

        for index in range(3):
            resp = self.post("/ui-doorway/ui/v1/license/devices", json=data, headers=headers)
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
        result = self.delete(f"/ui-doorway/ui/v1/license/devices?device_serials={(',').join(device_serial_list)}", headers=headers)
        log.info("unassign license output result {}".format(result))
        return result

    def get_device_license(self, secondary=None):
        if secondary:
            return self.get_secondary(f"/ui-doorway/ui/v1/license/devices")
        else:
            return self.get(f"/ui-doorway/ui/v1/license/devices")

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
            return self.get_secondary(f"/ui-doorway/ui/v1/applications/provisions")
        else:
            return self.get(f"/ui-doorway/ui/v1/applications/provisions")

    def get_account_contact(self, secondary=None):
        if secondary:
            return self.get_secondary(f"/accounts/ui/v1/customer/profile/contact")
        else:
            return self.get(f"/accounts/ui/v1/customer/profile/contact")

    def verify_claim_device(self,device):
        """
        :return: Provision Apps details
        """
        data = {'key': sub_key}
        res = self.post(f"/ui-doorway/ui/v1/customers/license", json=data)
        return res

    def apply_subscription_key(self,sub_key):
        """
        :return: Provision Apps details
        """
        data = {'key': sub_key}
        res = self.post(f"/ui-doorway/ui/v1/customers/license", json=data)
        return res

    def provision_application(self, region, appid):
        """
        Create an Application Customer ID for an App
        :param region: CCS Region code
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
        :param iteration: No of times to check
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