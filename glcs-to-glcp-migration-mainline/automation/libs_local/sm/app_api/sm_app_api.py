"""
Subscription Management app apis
"""
import logging
log = logging.getLogger()
from hpe_glcp_automation_lib.libs.authn.app_api.appsession import AppSession

class SubscriptionManagementApp(AppSession):

    def __init__(self, host, sso_host, client_id, client_secret):
        self.base_url = host
        super(SubscriptionManagementApp, self).__init__(host, sso_host, client_id, client_secret)
        self.get_token()
        self.base_path = "subscription-management/"
        self.api_version = "v1/"

    def get_sm_app_device_subscription_assignment_based_on_serial(self, serial_no):
        """
        Get device subscription assignment based on serial
        """
        url = f"{self.base_url}/subscription-management/app/v1/subscription/device/{serial_no}"
        res = self.get(url=url)
        log.info(f"response of subscription status check: {res}")
        return res

    def get_sm_app_subscription_stats_acid(self, pcid, acid):
        url = f"{self.base_url}/subscription-management/app/v1/subscription/{pcid}/application/{acid}/stats"
        res = self.get(url=url)
        log.info(f"response of subscription stats for ACID: {res}")
        return res

    def getDeviceSubscriptionAssignmentForApplicationCustomerId(self, pcid, acid, params):
        """
        Device subscription assignment information of an application customer
        Prams:
        subscription_type
        subscription_tier
        tier_type
        subscription_key
        device_serial_numbers
        limit
        offset
        """
        try:
            url = f"{self.base_url}/subscription-management/app/v1/subscription/{pcid}/application/{acid}/devices"
            log.info(f"{url} {params}")
            res = self.get(url=url, params=params)
            log.info(f"response of Device subscription assignment information of an application customer: {res}")
            return res
        except:
            log.info(
                "\nException in while getting Device subscription assignment information of an application customer \n")

    
    def get_sm_app_subscription_stats_pcid_acid_filter(self, pcid, acid, params):
        """
        Get Subscription stats of an application customer
        subscription_type
        subscription_key
        subscription_tiers
        app_name
        """
        try:
            url = f"{self.base_url}/subscription-management/app/v1/subscription/{pcid}/application/{acid}/stats"
            log.info(f"{url} {params}")
            res = self.get(url=url, params=params)
            log.info(f"response of Get Subscription stats of an application customer: {res}")
            return res
        except:
            log.info("\nException in while Get Subscription stats of an application customer \n")


    def get_sm_app_subscription_stats_pcid(self, pcid):
        """
        Get Subscription stats of a platform customer
        subscription_type
        subscription_key
        subscription_tiers
        app_name
        """
        try:
            url = f"{self.base_url}/subscription-management/app/v1/subscription/{pcid}/stats"
            log.info(f"{url} ")
            res = self.get(url=url)
            log.info(f"response of Get Subscription stats of a platform customer: {res}")
            return res
        except:
            log.info("\nException in while Get Subscription stats of a platform customer \n")


    def get_sm_app_subscription_stats_pcid_filter(self, pcid, params):
        """
        Get Subscription stats of a platform customer
        subscription_type
        subscription_key
        subscription_tiers
        app_name
        """
        try:
            url = f"{self.base_url}/subscription-management/app/v1/subscription/{pcid}/stats"
            log.info(f"{url} {params}")
            res = self.get(url=url, params=params)
            log.info(f"response of Get Subscription stats of a platform customer: {res}")
            return res
        except:
            log.info("\nException in while Get Subscription stats of a platform customer \n")



    def getDeviceSubscriptionAssignment(self, pcid, params):
        """
        Device subscription assignment information of a platform customer
        http://localhost:8080/subscription-management/app/v1/subscription/{platform_customer_id}/devices
        subscription_type
        subscription_key
        limit
        offset
        """
        try:
            url = f"{self.base_url}/subscription-management/app/v1/subscription/{pcid}/devices"
            log.info(f"{url} {params}")
            res = self.get(url=url, params=params)
            log.info(f"response of Get Subscription stats of a platform customer: {res}")
            return res
        except:
            log.info("\nException in while Get Subscription stats of a platform customer \n")


    def get_sm_app_subscription_tiers_for_device_type(self, params):
        """
        Get subscription tiers that can be assigned for a device type
        http://localhost:8080/subscription-management/app/v1/subscription/devices/config/tiers
        device_types
        """
        try:
            url = f"{self.base_url}/subscription-management/app/v1/subscription/devices/config/tiers"
            log.info(f"{url} {params}")
            res = self.get(url=url, params=params)
            log.info(f"response of  Get subscription tiers that can be assigned for a device type: {res}")
            return res
        except:
            log.info("\nException in while  Get subscription tiers that can be assigned for a device type \n")


    def get_sm_app_service_subscription_assigned_pcid_acid_filter(self, pcid, acid, params):
        """
        Get list of service subscription assigned to application instances for a given application customer and platform customer.
        subscription_type
        subscription_key
        sku
        subscription_tiers
        app
        end_date_in_millis
        """
        try:
            url = f"{self.base_url}/subscription-management/app/v1/subscription/{pcid}/application/{acid}/service"
            log.info(f"{url} {params}")
            res = self.get(url=url, params=params)
            log.info(f"response of Get list of service subscription assigned to application : {res}")
            return res
        except:
            log.info("\nException in while Get list of service subscription assigned to application  \n")


    def get_sm_app_time_series_trend_device_subscription_assignments(self, pcid, acid, params):
        """
        Get time-series trend for device subscription assignments
        device_types
        start_date_in_millis
        end_date_in_millis
        """
        try:
            url = f"{self.base_url}/subscription-management/app/v1/subscription/{pcid}/application/{acid}/devices/trend"
            log.info(f"{url} {params}")
            res = self.get(url=url, params=params)
            log.info(f"response of Get list of Get time-series trend for device subscription assignments : {res}")
            return res
        except:
            log.info("\nException in while Get list of Get time-series trend for device subscription assignments \n")


    def get_sm_app_auto_license_pcid_acid(self, pcid, acid):
        """
        Get auto license
        http://localhost:8080/subscription-management/app/v1/subscription/{platform_customer_id}/application/{application_customer_id}/autolicense
        device_types
        start_date_in_millis
        end_date_in_millis
        """
        try:
            url = f"{self.base_url}/subscription-management/app/v1/subscription/{pcid}/application/{acid}/autolicense"
            log.info(f"{url}")
            res = self.get(url=url)
            log.info(f"response of Get list of Get auto license: {res}")
            return res
        except:
            log.info("\nException in while Get auto license \n")

    
    def get_sm_app_subscriptions_based_on_pcid_acid_filter(self, pcid, acid, params):
        """
        Get assigned subscription information of application customer
        Prams:
        subscription_type
        subscription_key
        sku
        subscription_tiers
        app
        end_date_in_millis
        limit
        offset
        """
        try:
            url = f"{self.base_url}/subscription-management/app/v1/subscription/{pcid}/application/{acid}/"
            log.info(f"{url} {params}")
            res = self.get(url=url, params=params)
            log.info(f"response of Device subscription assignment information of an application customer: {res}")
            return res
        except:
            log.info(
                "\nException in while getting Device subscription assignment information of an application customer \n")

    def get_sm_app_subscription_info_pcid_filter(self, pcid, params):
        """
        Get subscription information of a platform customer
        subscription_type
        subscription_key
        subscription_key
        subscription_tiers
        end_date_in_millis
        sku
        app
        limit
        offset
        expire_date_cut_off_in_millis
        """
        try:
            url = f"{self.base_url}/subscription-management/app/v1/subscription/{pcid}"
            log.info(f"{url} {params}")
            res = self.get(url=url, params=params)
            log.info(f"response of Device subscription assignment information of an application customer: {res}")
            return res
        except:
            log.info(
                "\nException in while getting Device subscription assignment information of an application customer \n")

    #def subscription_info_pcid(self, pcid):
    def get_sm_app_subscription_info_pcid(self, pcid):
        url = f"{self.base_url}/subscription-management/app/v1/subscription/{pcid}"
        res = self.get(url=url)
        log.info(f"response of subscription info for PCID: {res}")
        return res

    def get_sm_app_device_subscription_mac(self, mac):
        url = f"{self.base_url}/subscription-management/app/v1/subscription/device/mac/{mac}"
        res = self.get(url=url)
        log.info(f"response of device subscription using MAC: {res}")
        return res

    def get_sm_app_subscription_devices(self, pcid, acid):
        url = f"{self.base_url}/subscription-management/app/v1/subscription/{pcid}/application/{acid}/devices?limit=500"
        res = self.get(url=url)
        return res

    
    def subscription_assign(self, pcid, acid, device,license ):
        url = f"{self.base_url}/subscription-management/app/v1/subscription/{pcid}/application/{acid}/devices"

        data = []
        license_data = {
            "device_serial": device,
            "subscription_key": license
        }

        data.append(license_data)
        res = self.post(url=url, json=data)
        log.info(f"response of assign license: {res}")
        return res

    def subscription_unassign(self, device_list_lic, pcid, acid):
        url = f"{self.base_url}/subscription-management/app/v1/subscription/{pcid}/application/{acid}/devices?deviceSerialNumbers={(',').join(device_list_lic)}"
        res = self.delete(url=url)
        log.info(f"response of unassign license: {res}")
        return res

    def get_sm_app_subscription_alias_customers(self):
        """
        This Function gets customer aliases
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
        subscription_type
        subscription_key
        limit
        offset
        sku
        end_date_in_millis
        subscription_tier
        app
        device_type
        subscription_key_pattern
        evaluation_type
        activation_start_date_in_millis
        activation_end_date_in_millis
        """
        try:
            url = f"{self.base_url}/subscription-management/app/v1/subscription/management/subscriptions"
            log.info(f"{url} {params}")
            res = self.get(url=url, params=params)
            log.info(f"response of  Get subscription tiers that can be assigned for a device type: {res}")
            return res
        except:
            log.info("\nException in while  Get subscription tiers that can be assigned for a device type \n")


    # def subscription_status_check(self, serial_no):
    def get_sm_app_device_subscription_assignment_no_filter(self, serial_no):
        """
        Get device subscription assignment based on serial
        """
        try:
            url = f"{self.base_url}/subscription-management/app/v1/subscription/device"
            res = self.get(url=url)
            log.info(f"response of subscription status check: {res}")
        except Exception as e:
            log.info(f"\nException in while get_sm_app_device_subscription_assignment_no_filter {e}\n")


    def _get_path(self, path):
        return f"{self.base_url}{self.base_path}{self.api_version}{path}"
