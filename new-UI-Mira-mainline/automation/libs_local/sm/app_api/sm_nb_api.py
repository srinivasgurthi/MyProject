'''
Subscription Management NBAPI apis
Please refer Document

'''
import logging

from hpe_glcp_automation_lib.libs.commons.app_api.app_session import AppSession

log = logging.getLogger()


class SubscriptionManagementNBAPI(AppSession):

    def __init__(self, host, sso_host, client_id, client_secret):
        self.base_url = host
        super(SubscriptionManagementNBAPI, self).__init__(host, sso_host, client_id, client_secret)
        self.get_token()
        self.base_path = "/subscription-management/app/"
        self.api_version = "v1/"
        self.nbapi_url = "central/"
        self.nbapi_base_url = f"{self.base_url}{self.base_path}{self.api_version}{self.nbapi_url}"

    def sm_nbapi_standalone_post_Assign_licenses_all_devices(self, application_customer_id, services):
        '''
        Standalone customer API:- Assign licenses to all devices.
        Note: This API should not be used for more than 20 device_serial_numbers at a time
        application_customer_id : Mandatory
        services: List Mandatory
        '''

        data = {}
        data["services"] = services
        params = {"application_customer_id": application_customer_id}
        end_point = "subscriptions/devices/all"
        url = f"{self.nbapi_base_url}{end_point}"
        res = self.post(url=url, json=data, params=params)
        log.info(f"Response of restAPI call : {res}")
        return res

    def sm_nbapi_standalone_delete_unassign_licenses_all_devices(self, application_customer_id, services):
        '''
        Standalone customer API:- Un-assign licenses to all devices for given service
        Note:- This API is not applicable for MSP customer
        application_customer_id : Mandatory
        services: List Mandatory
        '''

        data = {}
        data["services"] = services
        params = {"application_customer_id": application_customer_id}
        end_point = "subscriptions/devices/all"
        url = f"{self.nbapi_base_url}{end_point}"
        res = self.delete(url=url, json=data, params=params)
        log.info(f"Response of restAPI call : {res}")
        return res

    def sm_nbapi_standalone_post_assign_subscription_device(self, platform_customer_id, application_customer_id,
                                                            services, serials):
        '''
        This API is used to assign subscriptions to device by specifying its serial.
        platform_customer_id: Mandatory
        application_customer_id : Mandatory
        services = List of services : Mandatory
        serials : list of serials : Mandatory
        '''

        data = {}
        data["services"] = services
        data["serials"] = serials
        params = {"application_customer_id": application_customer_id, "platform_customer_id": platform_customer_id}

        end_point = "subscriptions/devices/all"
        url = f"{self.nbapi_base_url}{end_point}"
        res = self.post(url=url, json=data, params=params)
        log.info(f"Response of restAPI call : {res}")
        return res

    def sm_nbapi_MSP_post_assign_subscription_device(self, application_customer_id, \
                                                     services, \
                                                     include_customers=[], \
                                                     exclude_customers=[]):
        '''
        MSP API:- Assign licenses to all the devices owned by tenant customers
        include_customers: if provided, licenses to  customers present in include_customers list
        exclude_customers: if provided, licenses to msp/tenant customers except the customers present in exclude_customers list.
        services : subscriptions to be assigned
        '''

        data = {}
        data["services"] = services
        data["include_customers"] = include_customers
        data["exclude_customers"] = exclude_customers
        params = {"application_customer_id": application_customer_id}

        end_point = "msp/subscriptions/devices/all"
        url = f"{self.nbapi_base_url}{end_point}"
        res = self.post(url=url, json=data, params=params)
        log.info(f"Response of restAPI call : {res}")
        return res

    def sm_nbapi_MSP_delete_unassign_subscription_device(self, application_customer_id, \
                                                         services, \
                                                         include_customers=[], \
                                                         exclude_customers=[]):
        '''
        MSP API:- Remove service licenses to all the devices owned by tenants and MSP.
        include_customers: if provided, licenses to  customers present in include_customers list
        exclude_customers: if provided, licenses to msp/tenant customers except the customers present in exclude_customers list.
        services : subscriptions to be assigned
        '''
        data = {}
        data["services"] = services
        data["include_customers"] = include_customers
        data["exclude_customers"] = exclude_customers
        params = {"application_customer_id": application_customer_id}

        end_point = "msp/subscriptions/devices/all"
        url = f"{self.nbapi_base_url}{end_point}"
        res = self.delete(url=url, json=data, params=params)
        log.info(f"Response of restAPI call : {res}")
        return res

    def sm_nbapi_MSP_get_services_auto_enabled(self, application_customer_id, tenant_application_customer_id):
        '''
        This API is used to get services which are auto enabled for MSP
        platform_customer_id: Mandatory
        application_customer_id : Mandatory
        '''

        params = {"application_customer_id": application_customer_id, \
                  "tenant_application_customer_id": tenant_application_customer_id}

        end_point = "msp/customer/settings/autolicense"
        url = f"{self.nbapi_base_url}{end_point}"
        res = self.get(url=url, params=params)
        log.info(f"Response of restAPI call : {res}")
        return res

    def sm_nbapi_MSP_post_enable_auto_license(self, application_customer_id, \
                                              services, \
                                              include_customers=[], \
                                              exclude_customers=[]):
        '''
        MSP API:- Enable auto license settings and assign services to all devices owned by tenant customers.
        include_customers: if provided, licenses to  customers present in include_customers list
        exclude_customers: if provided, licenses to msp/tenant customers except the customers present in exclude_customers list.
        services : subscriptions to be assigned
        '''

        data = {}
        data["services"] = services
        data["include_customers"] = include_customers
        data["exclude_customers"] = exclude_customers
        params = {"application_customer_id": application_customer_id}

        end_point = "msp/customer/settings/autolicense"
        url = f"{self.nbapi_base_url}{end_point}"
        res = self.post(url=url, json=data, params=params)
        log.info(f"Response of restAPI call : {res}")
        return res

    def sm_nbapi_MSP_delete_remove_auto_license(self, application_customer_id, \
                                                services, \
                                                include_customers=[], \
                                                exclude_customers=[]):
        '''
        MSP API:- Remove service licenses to all the devices owned by tenants and MSP.
        include_customers: if provided, licenses to  customers present in include_customers list
        exclude_customers: if provided, licenses to msp/tenant customers except the customers present in exclude_customers list.
        services : subscriptions to be assigned
        '''
        data = {}
        data["services"] = services
        data["include_customers"] = include_customers
        data["exclude_customers"] = exclude_customers
        params = {"application_customer_id": application_customer_id}

        end_point = "msp/customer/settings/autolicense"
        url = f"{self.nbapi_base_url}{end_point}"
        res = self.delete(url=url, json=data, params=params)
        log.info(f"Response of restAPI call : {res}")
        return res

    def sm_nbapi_get_service_auto_enabled(self, application_customer_id):
        '''
        This API is used to get services which are auto enabled for  stand alone customer
        application_customer_id : Required
        '''

        params = {"application_customer_id": application_customer_id}
        end_point = "customer/settings/autolicense"
        url = f"{self.nbapi_base_url}{end_point}"
        res = self.get(url=url, params=params)
        log.info(f"Response of restAPI call : {res}")
        return res

    def sm_nbapi_standalone_post_assign_autolicense(self, application_customer_id, \
                                                    services):
        '''
        Standalone Customer API:- Assign licenses to all devices and enable auto licensing for given services
        services :required list
        '''

        data = {}
        data["services"] = services
        params = {"application_customer_id": application_customer_id}
        end_point = "customer/settings/autolicense"
        url = f"{self.nbapi_base_url}{end_point}"
        res = self.post(url=url, json=data, params=params)
        log.info(f"Response of restAPI call : {res}")
        return res

    def sm_nbapi_standalone_delete_disable_autolicense(self, \
                                                       application_customer_id, \
                                                       services):
        '''
        Standalone Customer API:- Assign licenses to all devices and enable auto licensing for given services
        services : List
        '''

        data = {}
        data["services"] = services
        params = {"application_customer_id": application_customer_id}

        end_point = "customer/settings/autolicense"
        url = f"{self.nbapi_base_url}{end_point}"
        res = self.delete(url=url, json=data, params=params)
        log.info(f"Response of restAPI call : {res}")
        return res

    def sm_nbapi_subscription_get_assigned_subscriptions(self, application_customer_id, \
                                                         limit=10, \
                                                         offset=10, \
                                                         license_type="foundation_ap"):
        '''
        Subscription data assigned to application customer
        application_customer_id : Mandatory
        limit: page limit
        offset : page offset
        license_type: License type

        '''

        params = {"application_customer_id": application_customer_id, \
                  "limit": limit, \
                  "offset": offset, \
                  "license_type": license_type}

        end_point = "subscriptions"
        url = f"{self.nbapi_base_url}{end_point}"
        res = self.get(url=url, params=params)
        log.info(f"Response of restAPI call : {res}")
        return res

    def sm_nbapi_subscription_get_stats_application_customer(self, platform_customer_id, \
                                                             application_customer_id, \
                                                             license_type="", \
                                                             service=[], \
                                                             app_only_stats=False):
        '''
        Subscription stats for an application customer
        license_type : Optional
        service : optional list
        app_only_stats: optional : False
        '''
        params = {"license_type": license_type, \
                  "service": service, \
                  "app_only_stats": app_only_stats}

        end_point = f'subscription/{platform_customer_id}/application/{application_customer_id}/stats'
        url = f"{self.nbapi_base_url}{end_point}"
        res = self.get(url=url, params=params)
        log.info(f"Response of restAPI call : {res}")
        return res

    def sm_nbapi_get_subscription_enabled(self, platform_customer_id, \
                                          application_customer_id):
        '''
        Get enabled/assigned subscription tiers for a customer
        platform_customer_id: Mandatory
        application_customer_id : Mandatory
        '''
        params = {"platform_customer_id": platform_customer_id, \
                  "application_customer_id": application_customer_id}
        end_point = f'services/enabled'
        url = f"{self.nbapi_base_url}{end_point}"
        res = self.get(url=url, params=params)
        log.info(f"Response of restAPI call : {res}")
        return res

    def sm_nbapi_get_service_config_license_types_device(self, device_type=None, \
                                                         service_category=None):
        '''
        Get supported license types for assignment for a device type
        device_type : optional : exapmple gateway, vgw, iap, switch, \
        controller, cap, boc, all_ap, all_controller, others, mas
        service_category:optional example  dm, network, platform, sdwan, non_dm, dm, vgw_500m etc
        '''
        end_point = f'services/config'
        params = {"device_type": device_type, \
                  "service_category": service_category}
        url = f"{self.nbapi_base_url}{end_point}"
        res = self.get(url=url, params=params)
        log.info(f"Response of restAPI call : {res}")
        return res

    def sm_nbapi_get_service_license_token_availability(self, platform_customer_id, \
                                                        application_customer_id,
                                                        service=[]):
        '''
            Get services and corresponding license token availability status. \
            If True, license tokens are more than device count else less than device count.
            service: Required list
            platform_customer_id: Required
            application_customer_id: Required
        '''

        end_point = f'autolicensing/services/{service}/status'
        params = {"platform_customer_id": platform_customer_id, \
                  "application_customer_id": application_customer_id}
        url = f"{self.nbapi_base_url}{end_point}"
        res = self.get(url=url, params=params)
        log.info(f"Response of restAPI call : {res}")
        return res

    def sm_nbapi_delete_unassign_subscription_devices_application_customer(self, platform_customer_id, \
                                                                           application_customer_id, \
                                                                           services, \
                                                                           serials):
        '''
        Device subscription un-assignment for an application customer
        services: Mandatory (List)
        serials: Mandatory (List)
        platform_customer_id: Mandatory
        application_customer_id : Mandatory

        '''

        data = {}
        data["services"] = services
        data["serials"] = serials
        params = {"application_customer_id": application_customer_id, "platform_customer_id": platform_customer_id}
        end_point = "subscription/{platform_customer_id}/application/{application_customer_id}/devices"
        url = f"{self.nbapi_base_url}{end_point}"
        res = self.delete(url=url, json=data, params=params)
        log.info(f"Response of restAPI call : {res}")
        return res
