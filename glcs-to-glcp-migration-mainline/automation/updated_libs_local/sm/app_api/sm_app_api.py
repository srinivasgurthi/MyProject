"""
Subscription Management app apis
"""
import logging
from hpe_glcp_automation_lib.libs.commons.app_api.app_session import AppSession

log = logging.getLogger()


class SubscriptionManagementApp(AppSession):

    def __init__(self, host, sso_host, client_id, client_secret):
        log.info("Initializing sm_app_api for user api calls")
        super().__init__(host, sso_host, client_id, client_secret)
        self.base_path = "/subscription-management/app"
        self.api_version = "/v1"

    def _get_path(self, path):
        return f"{self.base_url}{self.base_path}{self.api_version}/{path}"

    def create_subs_order(self, data):
        """
        Create subscription order
        :param data : Required for creating order
        returns :Response of API call
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/orders"
        res = self.post(url=url, json=data)
        log.info(f"response of subscription status check: {res}")
        return res

    def get_subs_order(self, quote_number):
        """
        Get subscription order based on quote_number
        :param quote_number : Quote Number
        returns :Response of API call
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/orders/{quote_number}"
        res = self.get(url=url)
        log.info(f"response of subscription status check: {res}")
        return res

    def update_subs_order(self, data):
        """
        Update in existing subscription entitlement details to CCS
        :param data : Required for creating order
        returns :Response of API call
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/orders/"
        res = self.put(url=url, json=data)
        log.info(f"response of subscription status check: {res}")
        return res

    def update_subs_order_appointment(self, data):
        """
        Update in existing subscription appointment details
        :param data : Required for creating order
        returns :Response of API call
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/maintenance/orders/maintenance"
        res = self.put(url=url, json=data)
        log.info(f"response of Update in existing subscription appointment details: {res}")
        return res

    def receive_subs_order_activation_error(self, errorData):
        """
        Inform subscription entitlement error details
        :param errorData : Required for Error data
        returns :Response of API call
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/orders/activation/error"
        res = self.post(url=url, json=errorData)
        log.info(f"response of Inform subscription entitlement error: {res}")
        return res

    def get_sm_app_device_subscription_assignment_based_on_serial(self, serial_no):
        """
        Get device subscription assignment based on serial
        :param serial_no : Serial Number of the device.
        returns :Response of API call
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/subscription/device/{serial_no}"
        res = self.get(url=url)
        log.info(f"response of subscription status check: {res}")
        return res

    def get_sm_app_subscription_stats_acid(self, pcid, acid):
        """
        Get device subscription stas
        :param pcid: required - Platform customer ID
        :param acid : required - Application customer ID
        returns :Response of API call
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/subscription/{pcid}/application/{acid}/stats"
        res = self.get(url=url)
        log.info(f"response of subscription stats for ACID: {res}")
        return res

    def get_device_subscription_assignment_for_application_customer_id(self, pcid, acid, params):
        """
        Device subscription assignment information of an application customer
        :param: subscription_type
        :param: subscription_tier
        :param:tier_type
        :param:subscription_key
        :param:device_serial_numbers
        :param:limit
        :param:offset
        returns :Response of API call
        """
        try:
            url = f"{self.base_url}{self.base_path}{self.api_version}/subscription/{pcid}/application/{acid}/devices"
            log.info(f"{url} {params}")
            res = self.get(url=url, params=params)
            log.info(f"response of Device subscription assignment information of an application customer: {res}")
            return res
        except Exception as e:
            log.info(
                "\nException in while getting Device subscription assignment information of an application customer \n"
                f"{e}")

    def get_sm_app_subscription_stats_pcid_acid_filter(self, pcid, acid, params):
        """
        Get Subscription stats of an application customer
        :param:subscription_type
        :param:subscription_key
        :param:subscription_tiers
        :param:app_name
        returns :Response of API call

        """
        try:
            url = f"{self.base_url}{self.base_path}{self.api_version}/subscription/{pcid}/application/{acid}/stats"
            log.info(f"{url} {params}")
            res = self.get(url=url, params=params)
            log.info(f"response of Get Subscription stats of an application customer: {res}")
            return res
        except Exception as e:
            log.info(f"\nException in while Get Subscription stats of an application customer \n{e}")

    def get_sm_app_subscription_assign_app_instance_by_acid_pcid(self, pcid, acid, params):

        """
        Get Service Subscriptions of a platform customer by application customer
        :param:pcid: required - Platform customer ID
        :param:acid : required - Application customer ID
        :param: subscription_type
        :param: subscription_key
        :param: subscription_tiers
        returns :Response of API call
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/subscription/{pcid}/application/{acid}/service"
        log.info(f"{url} {params}")
        res = self.get(url=url, params=params)
        log.info(f"response of Service Subscriptions of a platform customer by application customer: {res}")
        return res

    def get_sm_app_subscription_stats_pcid(self, pcid):
        """
        Get Subscription stats of a platform customer
        :param:subscription_type
        :param:subscription_key
        :param:subscription_tiers
        :param:app_name
        returns :Response of API call
        """
        try:
            url = f"{self.base_url}{self.base_path}{self.api_version}/subscription/{pcid}/stats"
            log.info(f"{url} ")
            res = self.get(url=url)
            log.info(f"response of Get Subscription stats of a platform customer: {res}")
            return res
        except Exception as e:
            log.info(f"\nException in while Get Subscription stats of a platform customer \n{e}")

    def get_sm_app_subscription_stats_pcid_filter(self, pcid, params):
        """
        Get Subscription stats of a platform customer
        :param:subscription_type
        :param:subscription_key
        :param:subscription_tiers
        :param:app_name
        returns :Response of API call
        """
        try:
            url = f"{self.base_url}{self.base_path}{self.api_version}/subscription/{pcid}/stats"
            log.info(f"{url} {params}")
            res = self.get(url=url, params=params)
            log.info(f"response of Get Subscription stats of a platform customer: {res}")
            return res
        except Exception as e:
            log.info(f"\nException in while Get Subscription stats of a platform customer \n{e}")

    def get_device_subscription_assignment(self, pcid, params):
        """
        Device subscription assignment information of a platform customer
        http://localhost:8080/subscription-management/app/v1/subscription/{platform_customer_id}/devices
        :param:subscription_type
        :param:subscription_key
        :param:limit
        :param:offset
        returns :Response of API call
        """
        try:
            url = f"{self.base_url}{self.base_path}{self.api_version}/subscription/{pcid}/devices"
            log.info(f"{url} {params}")
            res = self.get(url=url, params=params)
            log.info(f"response of Get Subscription stats of a platform customer: {res}")
            return res
        except Exception as e:
            log.info(f"\nException in while Get Subscription stats of a platform customer \n{e}")

    def get_sm_app_subscription_tiers_for_device_type(self, params, **kwargs):
        """
        Get subscription tiers that can be assigned for a device type
        http://localhost:8080/subscription-management/app/v1/subscription/devices/config/tiers
        :param:device_types
        returns :Response of API call
        """
        try:
            url = f"{self.base_url}{self.base_path}{self.api_version}/subscription/devices/config/tiers"
            log.info(f"{url} {params}")
            res = self.get(url=url, params=params, **kwargs)
            log.info(f"response of  Get subscription tiers that can be assigned for a device type: {res}")
            return res
        except Exception as e:
            log.info(f"\nException in while  Get subscription tiers that can be assigned for a device type \n{e}")

    def get_sm_app_service_subscription_assigned_pcid_acid_filter(self, pcid, acid, params):
        """
        Get list of service subscription assigned to application instances for a given application customer and
        :param:platform customer.
        :param:subscription_type
        :param:subscription_key
        :param:sku
        :param:subscription_tiers
        :param:app
        :param:end_date_in_millis
        returns :Response of API call
        """
        try:
            url = f"{self.base_url}{self.base_path}{self.api_version}/subscription/{pcid}/application/{acid}/service"
            log.info(f"{url} {params}")
            res = self.get(url=url, params=params)
            log.info(f"response of Get list of service subscription assigned to application : {res}")
            return res
        except Exception as e:
            log.info(f"\nException in while Get list of service subscription assigned to application  \n{e}")

    def get_sm_app_time_series_trend_device_subscription_assignments(self, pcid, acid, params):
        """
        Get time-series trend for device subscription assignments
        :param:device_types
        :param:start_date_in_millis
        :param:end_date_in_millis
        returns :Response of API call
        """
        try:
            url = f"{self.base_url}{self.base_path}{self.api_version}/subscription/{pcid}/application/{acid}/devices/trend"
            log.info(f"{url} {params}")
            res = self.get(url=url, params=params)
            log.info(f"response of Get list of Get time-series trend for device subscription assignments : {res}")
            return res
        except Exception as e:
            log.info(
                f"\nException in while Get list of Get time-series trend for device subscription assignments \n{e}")

    def get_sm_app_auto_license_pcid_acid(self, pcid, acid):
        """
        Get auto license
        http://localhost:8080/subscription-management/app/v1/subscription/{platform_customer_id}/application/\
        {application_customer_id}/autolicense
        :param:device_types
        :param:start_date_in_millis
        :param:end_date_in_millis
        returns :Response of API call
        """
        try:
            url = f"{self.base_url}{self.base_path}{self.api_version}/subscription/{pcid}/application/{acid}/autolicense"
            log.info(f"{url}")
            res = self.get(url=url)
            log.info(f"response of Get list of Get auto license: {res}")
            return res
        except Exception as e:
            log.info(f"\nException in while Get auto license \n{e}")

    def get_sm_app_subscriptions_based_on_pcid_acid_filter(self, pcid, acid, params):
        """
        Get assigned subscription information of application customer
        :param:subscription_type
        :param:subscription_key
        :param:sku
        :param:subscription_tiers
        :param:app
        :param:end_date_in_millis
        :param:limit
        :param:offset
        returns :Response of API call
        """
        try:
            url = f"{self.base_url}{self.base_path}{self.api_version}/subscription/{pcid}/application/{acid}/"
            log.info(f"{url} {params}")
            res = self.get(url=url, params=params)
            log.info(f"response of Device subscription assignment information of an application customer: {res}")
            return res
        except Exception as e:
            log.info(
                "\nException in while getting Device subscription assignment information of an application customer \n"
                f"{e}")

    def get_sm_app_subscription_info_pcid_filter(self, pcid, params):
        """
        Get subscription information of a platform customer
        :param:subscription_type
        :param:subscription_key
        :param:subscription_key
        :param:subscription_tiers
        :param:end_date_in_millis
        :param:sku
        :param:app
        :param:limit
        :param:offset
        :param:expire_date_cut_off_in_millis
        returns :Response of API call
        """
        try:
            url = f"{self.base_url}{self.base_path}{self.api_version}/subscription/{pcid}"
            log.info(f"{url} {params}")
            res = self.get(url=url, params=params)
            log.info(f"response of Device subscription assignment information of an application customer: {res}")
            return res
        except Exception as e:
            log.info(
                "\nException in while getting Device subscription assignment information of an application customer \n"
                f"{e}")

    def get_sm_app_subscription_info_pcid(self, pcid):
        """
        Get subscription application info
        pcid: required - Platform customer ID
        returns :Response of API call
        """

        url = f"{self.base_url}{self.base_path}{self.api_version}/subscription/{pcid}"
        res = self.get(url=url)
        log.info(f"response of subscription info for PCID: {res}")
        return res

    def get_sm_app_device_subscription_mac(self, mac):
        """
        Get subscription of device by mac
        :param:: required - mac address if device
        returns :Response of API call
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/subscription/device/mac/{mac}"
        res = self.get(url=url)
        log.info(f"response of device subscription using MAC: {res}")
        return res

    def get_sm_app_subscription_devices(self, pcid, acid):
        """
        Get application subscription for devices
        :param:pcid: required - Platform customer ID
        :param:acid : required - Application customer ID
        returns :Response of API call
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/subscription/{pcid}/application/{acid}/devices?limit=500"
        res = self.get(url=url)
        return res

    def subscription_assign(self, pcid, acid, device, license, **kwargs):
        """
        Assign subscription to a device
        :param:pcid: required - Platform customer ID
        :param:acid : required - Application customer ID
        :param:device : device serial numbers
        :param:license: subscription key
        returns :Response of API call
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/subscription/{pcid}/application/{acid}/devices"

        data = []
        license_data = {
            "device_serial": device,
            "subscription_key": license
        }

        data.append(license_data)
        res = self.post(url=url, json=data, **kwargs)
        log.info(f"Response of API request: {res}")
        return res

    def subscription_unassign(self, device_list_lic, pcid, acid, **kwargs):
        """
        Unassign subscription to a device
        :param:pcid: required - Platform customer ID
        :param:acid : required - Application customer ID
        :param:device : device serial numbers
        :param:license: subscription key
        returns :Response of API call
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/subscription/{pcid}/application/{acid}/devices?deviceSerialNumbers={','.join(device_list_lic)}"
        res = self.delete(url=url, **kwargs)
        log.info(f"response of unassign license: {res}")
        return res

    def get_sm_app_subscription_alias_customers(self):
        """
        This Function gets customer aliases
        returns :Response of API call
        """
        add_path = "customers/aliases"
        url = self._get_path(add_path)
        res = self.get(url=url)
        log.info(f"The customer aliases are {res}")
        return res

    def get_sm_app_subscription_information_all_customers(self, params):
        """
        Get subscription information for all customers
        http://localhost:8080/subscription-management/app/v1/subscription/management/subscriptions
        :param:subscription_type
        :param:subscription_key
        :param:limit
        :param:offset
        :param:sku
        :param:end_date_in_millis
        :param:subscription_tier
        :param:app
        :param:device_type
        :param:subscription_key_pattern
        :param:evaluation_type
        :param:activation_start_date_in_millis
        :param:activation_end_date_in_millis
        returns :Response of API call
        """
        try:
            url = f"{self.base_url}{self.base_path}{self.api_version}/subscription/management/subscriptions"
            log.info(f"{url} {params}")
            res = self.get(url=url, params=params)
            log.info(f"response of  Get subscription tiers that can be assigned for a device type: {res}")
            return res
        except Exception as e:
            log.info(f"\nException in while  Get subscription tiers that can be assigned for a device type \n{e}")

    def get_sm_app_device_subscription_assignment_no_filter(self):
        """
        Get device subscription assignment based on serial
        returns :Response of API call
        """
        try:
            url = f"{self.base_url}{self.base_path}{self.api_version}/subscription/device"
            res = self.get(url=url)
            log.info(f"response of subscription status check: {res}")
        except Exception as e:
            log.info(f"\nException in while get_sm_app_device_subscription_assignment_no_filter {e}\n")

    def reassign_subscription(self, pcid, acid, device, license):
        """
        Re-assign Subscription to devices of an application customer
        :param:pcid: required - Platform customer ID
        :param:acid : required - Application customer ID
        :param:license : required - License Key
        returns :Response of API call
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/subscription/{pcid}/application/{acid}/devices"

        data = []
        license_data = {
            "device_serial": device,
            "subscription_key": license
        }

        data.append(license_data)
        res = self.put(url=url, json=data)
        log.info(f"Response of API request: {res}")
        return res

    def extend_subscription(self, pcid, params):
        """
        Extending subscription
        :param:app
        :param:sku
        :param:force_flag
        :param:subscription_tier
        :param:subscription_key
        :param:subscription_type
        :param:increase_quantity_by:Required
        :param:extend_end_seconds:Required
        returns :Response of API call
        """

        url = f"{self.base_url}{self.base_path}{self.api_version}/subscription/{pcid}/management"
        res = self.post(url=url, params=params)
        log.info(f"Response of API request: {res}")
        return res

    def cancel_subscription(self, pcid, params):
        """
        Extending subscription
        :param:app
        :param:sku
        :param:subscription_type
        :param:subscription_tier
        :param:subscription_key
        returns :Response of API call
        """

        url = f"{self.base_url}{self.base_path}{self.api_version}/subscription/{pcid}/management"
        res = self.delete(url=url, params=params)
        log.info(f"Response of API request: {res}")
        return res


    def genarate_vgw_aubscription(self, pcid, subscription_tiers):
        """
        Create VGW specific subscriptions, e.g. VGW2G, VGW4G, VGW500M
        :param:subscription_tiers
        returns :Response of API call
        """
        params = {}
        params["subscription_tiers"] =subscription_tiers
        url = f"{self.base_url}{self.base_path}{self.api_version}/subscription/{pcid}/eval/vgw"
        res = self.post(url=url,params=params )
        log.info(f"Response of API request: {res}")
        return res

    def modify_auto_license_include(self, pcid, acid, device_type, enabled,subscription_tier):
        """
        Modify auto license setting for include customers
        :param:device_type required "AP" "SWITCH" "GATEWAY" "STORAGE" "DHCI_STORAGE" "COMPUTE" "DHCI_COMPUTE" "NW_THIRD_PARTY"
        :param:enabled require boolean
        :param:auto_license_subscription_tier_group required : "FOUNDATION_AP" \
        "ADVANCED_AP" "FOUNDATION_SWITCH" "ADVANCED_SWITCH" \
        "FOUNDATION_GW" "ADVANCED_GW" "STANDARD_COMPUTE" "ENHANCED_COMPUTE"
        returns :Response of API call
        """
        params = {}
        data = {}
        data["device_type"] = device_type
        data["enabled"] = enabled
        data["auto_license_subscription_tier_group"] = subscription_tier

        params["application_customer_id"] =acid
        url = f"{self.base_url}{self.base_path}{self.api_version}/subscription/{pcid}/autolicense/include"
        res = self.post(url=url,params=params, json=data )
        log.info(f"Response of API request: {res}")
        return res

    def modify_auto_license_exclude(self, pcid, acid, device_type, enabled,subscription_tier):
        """
        Modifies the autolicense settings
        :param:device_type required "AP" "SWITCH" "GATEWAY" "STORAGE" "DHCI_STORAGE" "COMPUTE" "DHCI_COMPUTE" "NW_THIRD_PARTY"
        :param:enabled require boolean
        :param: auto_license_subscription_tier_group required : "FOUNDATION_AP" \
        "ADVANCED_AP" "FOUNDATION_SWITCH" "ADVANCED_SWITCH" \
        "FOUNDATION_GW" "ADVANCED_GW" "STANDARD_COMPUTE" "ENHANCED_COMPUTE"
        returns :Response of API call
        """
        params = {}
        data = {}
        data["device_type"] = device_type
        data["enabled"] = enabled
        data["auto_license_subscription_tier_group"] = subscription_tier
        params["application_customer_id"] =acid
        url = f"{self.base_url}{self.base_path}{self.api_version}/subscription/{pcid}/autolicense/exclude"
        res = self.post(url=url,params=params, json=data )
        log.info(f"Response of API request: {res}")
        return res

    def unlicense_devices_including_customers(self, pcid, acid):
        """
        Unlicense devices including customers
        :param:pcid: required - Platform customer ID
        :param:acid : required - Application customer ID
        returns :Response of API call
        """
        params = {}
        params["application_customer_id"] = acid
        url = f"{self.base_url}{self.base_path}{self.api_version}/subscription/{pcid}/devices/include"
        res = self.delete(url=url, params=params)
        log.info(f"Response of API request: {res}")
        return res


    def unlicense_devices_excluding_customers(self, pcid, acid):
        """
        unlicense devices excluding customers
        :param:pcid: required - Platform customer ID
        :param:acid : required - Application customer ID
        returns :Response of API call
        """
        params = {}
        params["application_customer_id"] = acid
        url = f"{self.base_url}{self.base_path}{self.api_version}/subscription/{pcid}/devices/exclude"
        res = self.delete(url=url, params=params)
        log.info(f"Response of API request: {res}")
        return res

    def get_sm_lifecycle_controller(self):
        """
        getStatus v-1-life-cycle-controller
        returns :Response of API call
        """
        url = f"{self.base_url}{self.base_path}{self.api_version}/lifecycle/status"
        res = self.get(url=url)
        log.info(f"Response of lifecycle API request: {res}")
        return res


