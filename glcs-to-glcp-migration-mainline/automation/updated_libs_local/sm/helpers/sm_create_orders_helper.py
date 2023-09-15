"""
Helper function for New Subscription order App Api Class
"""
import logging
import time

from datetime import datetime
from hpe_glcp_automation_lib.libs.commons.utils.random_gens import RandomGenUtils
from hpe_glcp_automation_lib.libs.sm.app_api.sm_app_api import SubscriptionManagementApp
from hpe_glcp_automation_lib.libs.sm.helpers.sm_payload_constants import SmInputPayload

log = logging.getLogger(__name__)


class NewSubsOrder:
    """
    Helper class for New Subscription order App Api Class
    """

    def __init__(self,
                 end_username,
                 app_api_host,
                 sso_host,
                 aop_client_id,
                 aop_client_secret
                 ):
        """
        Initialize NewSubsOrder class
        :param app_api_host: App api hostname for cluster
        :param sso_host: sso_host
        :param aop_client_id: app client_id
        :param aop_client_secret: app client_secret
        """
        self.end_username = end_username
        self.payload = SmInputPayload()
        self.app_api_host = app_api_host
        self.sso_host = sso_host
        self.aop_client_id = aop_client_id
        self.aop_client_secret = aop_client_secret
        self.order = SubscriptionManagementApp(self.app_api_host,
                                               self.sso_host,
                                               self.aop_client_id,
                                               self.aop_client_secret)

    def create_svc_order(self, order_type=None):
        """
        Create service order, supported order types/payloads currently:
            default - vm_backup
            ZERTO - svc_dis_recovery_zerto
        :param order_type: Type of service order
        :return: license order key
        """
        if order_type == "ZERTO":
            svc_order_data = self.payload.svc_dis_recovery_zerto()
        else:
            svc_order_data = self.payload.vm_bakcup()

        svc_order_data['activate']['contacts'][0]['id'] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=False, digits=True)
        svc_order_data['activate']['contacts'][0]['countryId'] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=False, digits=True)
        svc_order_data['activate']['contacts'][0]['globalId'] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=False, digits=True)
        svc_order_data['activate']['endUserName'] = self.end_username + " Company"
        for i in range(0, len(svc_order_data['activate']["parties"])):
            svc_order_data['activate']["parties"][i]['id'] = RandomGenUtils.random_string_of_chars(
                length=10, lowercase=False, uppercase=False, digits=True)
            svc_order_data['activate']["parties"][i]['countryId'] = RandomGenUtils.random_string_of_chars(
                length=10, lowercase=False, uppercase=False, digits=True)
            svc_order_data['activate']["parties"][i]['globalId'] = RandomGenUtils.random_string_of_chars(
                length=10, lowercase=False, uppercase=False, digits=True)
        svc_order_data['activate']['party']['id'] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=False, digits=True)
        svc_order_data['activate']['party']['countryId'] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=False, digits=True)
        svc_order_data['activate']['party']['globalId'] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=False, digits=True)
        svc_order_data['activate']['po'] = "PONUMCCS_09_170120_" + RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=False, digits=True)
        svc_order_data['contract'] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=False, digits=True)
        svc_order_data['entitlements'][0]['contract'] = svc_order_data['contract']   # contract should be same for order
        svc_order_data['customer']['MDM'] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=False, digits=True)
        svc_order_data['entitlements'][0]['licenses'][0]['id'] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=False, digits=True)
        svc_order_data['entitlements'][0]['quote'] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=False, digits=True)
        svc_order_data['quote'] = svc_order_data['entitlements'][0]['quote']    # quote should be same for order
        try:
            self.order = SubscriptionManagementApp(self.app_api_host, self.sso_host, self.aop_client_id,
                                                   self.aop_client_secret)
            svc_order = self.order.create_subs_order(svc_order_data)
            if svc_order:
                lic_order = self.order.get_subs_order(svc_order_data['quote'])
                lic_order_key = lic_order[0]['entitlements'][0]['licenses'][0]['id']
                return lic_order_key, lic_order[0]['quote']
            else:
                return False
        except Exception as e:
            log.error("Failed to create lic_order_key order with S/N {}".format(e))
            return False

    def create_compute_subs_order(self, order_type=None):
        """
        Create compute iaas order
        :param order_type: Type of compute order
        :return: license order key
        """
        if order_type == "ALLETRA_4K":
            compute_iaas_subs_data = self.payload.subs_compute_alletra_4k()
        else:
            compute_iaas_subs_data = self.payload.subs_compute_iaas()

        compute_iaas_subs_data['quote'] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False)
        compute_iaas_subs_data['entitlements'][0]['quote'] = compute_iaas_subs_data['quote']
        compute_iaas_subs_data['contract'] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False)
        compute_iaas_subs_data['entitlements'][0]['contract'] = compute_iaas_subs_data['contract']
        compute_iaas_subs_data['activate']['endUserName'] = "Test_" + self.end_username + " Company"
        compute_iaas_subs_data['customer']['MDM'] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False)
        compute_iaas_subs_data['activate']['po'] = "PONUMCCS_09_170120_" + compute_iaas_subs_data['customer']['MDM']
        compute_iaas_subs_data['activate']['party']['id'] = compute_iaas_subs_data['customer']['MDM']
        for i in range(0, len(compute_iaas_subs_data['activate']["parties"])):
            compute_iaas_subs_data['activate']["parties"][i]['id'] = compute_iaas_subs_data['customer']['MDM']
        for i in range(0, len(compute_iaas_subs_data['activate']["contacts"])):
            compute_iaas_subs_data['activate']['contacts'][i]['id'] = compute_iaas_subs_data['customer']['MDM']
        compute_iaas_subs_data['entitlements'][0]['licenses'][0]['id'] = RandomGenUtils.random_string_of_chars(
            length=20, lowercase=False, uppercase=False, digits=True)
        try:
            self.order = SubscriptionManagementApp(self.app_api_host, self.sso_host, self.aop_client_id,
                                                   self.aop_client_secret)
            comp_iaas_order = self.order.create_subs_order(compute_iaas_subs_data)
            if comp_iaas_order:
                lic_order = self.order.get_subs_order(compute_iaas_subs_data['quote'])
                lic_order_key = lic_order[0]['entitlements'][0]['licenses'][0]['id']
                return lic_order_key, lic_order[0]['quote']
            else:
                return False
        except Exception as e:
            log.error("Failed to create lic_order_key order: {}, with quote: {}\n. Exception details: {}".format(lic_order_key, lic_order, e))
            return False

    def create_ap_subs_order(self):
        """
        Create Switch 6200 order
        :param order_type: Type of compute order
        :return: license order key
        """
        ap_subs_data = self.payload.subs_data_ap()
        ap_subs_data['quote'] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False)
        ap_subs_data['entitlements'][0]['quote'] = ap_subs_data['quote']
        ap_subs_data['contract'] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False)
        ap_subs_data['entitlements'][0]['contract'] = ap_subs_data['contract']
        ap_subs_data['activate']['endUserName'] = self.end_username + " Company"
        ap_subs_data['customer']['MDM'] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False)
        ap_subs_data['activate']['po'] = "PONUMCCS_09_170120_" + ap_subs_data['customer']['MDM']
        ap_subs_data['activate']['party']['id'] = ap_subs_data['customer']['MDM']
        for i in range(0, len(ap_subs_data['activate']["parties"])):
            ap_subs_data['activate']["parties"][i]['id'] = ap_subs_data['customer']['MDM']
        for i in range(0, len(ap_subs_data['activate']["contacts"])):
            ap_subs_data['activate']['contacts'][i]['id'] = ap_subs_data['customer']['MDM']
        ap_subs_data['entitlements'][0]['licenses'][0]['id'] = RandomGenUtils.random_string_of_chars(
            length=20, lowercase=False, uppercase=False, digits=True)
        try:
            self.order = SubscriptionManagementApp(self.app_api_host, self.sso_host, self.aop_client_id,
                                                   self.aop_client_secret)
            ap_subs_order = self.order.create_subs_order(ap_subs_data)
            if ap_subs_order:
                lic_order = self.order.get_subs_order(ap_subs_data['quote'])
                lic_order_key = lic_order[0]['entitlements'][0]['licenses'][0]['id']
                return lic_order_key, lic_order[0]['quote']
            else:
                return False
        except Exception as e:
            log.error("Failed to create lic_order_key order: {}, with quote: {}\n. Exception details: {}".format(lic_order_key, lic_order, e))
            return False

    def create_sw_subs_order(self, order_type=None):
        """
        Create Switch 6200 order
        :param order_type: Type of compute order
        :return: license order key
        """
        if order_type == "6300":
            sw_6200_subs_data = self.payload.subs_data_sw_6300()
        else:
            sw_6200_subs_data = self.payload.subs_data_sw_6200()

        sw_6200_subs_data['quote'] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False)
        sw_6200_subs_data['entitlements'][0]['quote'] = sw_6200_subs_data['quote']
        sw_6200_subs_data['contract'] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False)
        sw_6200_subs_data['entitlements'][0]['contract'] = sw_6200_subs_data['contract']
        sw_6200_subs_data['activate']['endUserName'] = self.end_username + " Company"
        sw_6200_subs_data['customer']['MDM'] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False)
        sw_6200_subs_data['activate']['po'] = "PONUMCCS_09_170120_" + sw_6200_subs_data['customer']['MDM']
        sw_6200_subs_data['activate']['party']['id'] = sw_6200_subs_data['customer']['MDM']
        for i in range(0, len(sw_6200_subs_data['activate']["parties"])):
            sw_6200_subs_data['activate']["parties"][i]['id'] = sw_6200_subs_data['customer']['MDM']
        for i in range(0, len(sw_6200_subs_data['activate']["contacts"])):
            sw_6200_subs_data['activate']['contacts'][i]['id'] = sw_6200_subs_data['customer']['MDM']
        sw_6200_subs_data['entitlements'][0]['licenses'][0]['id'] = RandomGenUtils.random_string_of_chars(
            length=20, lowercase=False, uppercase=False, digits=True)
        try:
            self.order = SubscriptionManagementApp(self.app_api_host, self.sso_host, self.aop_client_id,
                                                   self.aop_client_secret)
            sw_6200_subs_order = self.order.create_subs_order(sw_6200_subs_data)
            if sw_6200_subs_order:
                lic_order = self.order.get_subs_order(sw_6200_subs_data['quote'])
                lic_order_key = lic_order[0]['entitlements'][0]['licenses'][0]['id']
                return lic_order_key, lic_order[0]['quote']
            else:
                return False
        except Exception as e:
            log.error("Failed to create lic_order_key order: {}, with quote: {}\n. Exception details: {}".format(lic_order_key, lic_order, e))
            return False

    def create_gw_subs_order(self, order_type=None):
        """
        Create Gateway 72xx order
        :param order_type: Type of compute order
        :return: license order key
        """
        if order_type == "72XX":
            gw_72xx_subs_data = self.payload.subs_data_gw_72xx()
        else:
            gw_72xx_subs_data = self.payload.subs_data_gw_70xx()

        gw_72xx_subs_data['quote'] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False)
        gw_72xx_subs_data['entitlements'][0]['quote'] = gw_72xx_subs_data['quote']
        gw_72xx_subs_data['contract'] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False)
        gw_72xx_subs_data['entitlements'][0]['contract'] = gw_72xx_subs_data['contract']
        gw_72xx_subs_data['activate']['endUserName'] = self.end_username + " Company"
        gw_72xx_subs_data['customer']['MDM'] = RandomGenUtils.random_string_of_chars(
            length=10, lowercase=False, uppercase=True, digits=False)
        gw_72xx_subs_data['activate']['po'] = "PONUMCCS_09_170120_" + gw_72xx_subs_data['customer']['MDM']
        gw_72xx_subs_data['activate']['party']['id'] = gw_72xx_subs_data['customer']['MDM']
        for i in range(0, len(gw_72xx_subs_data['activate']["parties"])):
            gw_72xx_subs_data['activate']["parties"][i]['id'] = gw_72xx_subs_data['customer']['MDM']
        for i in range(0, len(gw_72xx_subs_data['activate']["contacts"])):
            gw_72xx_subs_data['activate']['contacts'][i]['id'] = gw_72xx_subs_data['customer']['MDM']
        gw_72xx_subs_data['entitlements'][0]['licenses'][0]['id'] = RandomGenUtils.random_string_of_chars(
            length=20, lowercase=False, uppercase=False, digits=True)
        try:
            self.order = SubscriptionManagementApp(self.app_api_host, self.sso_host, self.aop_client_id,
                                                   self.aop_client_secret)
            gw_72xx_subs_order = self.order.create_subs_order(gw_72xx_subs_data)
            if gw_72xx_subs_order:
                lic_order = self.order.get_subs_order(gw_72xx_subs_data['quote'])
                lic_order_key = lic_order[0]['entitlements'][0]['licenses'][0]['id']
                return lic_order_key, lic_order[0]['quote']
            else:
                return False
        except Exception as e:
            log.error("Failed to create lic_order_key order: {}, with quote: {}\n. Exception details: {}".format(lic_order_key, lic_order, e))
            return False

    def update_subs_order_to_expired(self, quote):
        '''
        Update order end date to current, subscription set to expired
        :param quote: Order type, any order
        :return: license order key
        '''
        lic_order = self.order.get_subs_order(quote)

        lic_order[0]['reason'] = 'Update'
        now = datetime.now()
        lic_order[0]['entitlements'][0]['licenses'][0]['appointments']['subscriptionEnd'] = now.strftime('%d.%m.%Y %H:%M:%S')
        try:
            log.info("\n\nOrder: {}\n\n".format(lic_order))
            time.sleep(5)
            res = self.order.update_subs_order(lic_order[0])
            time.sleep(6)
            if res:
                lic_order_updated = self.order.get_subs_order(quote)
                time.sleep(2)
                lic_order_updated_key = lic_order_updated[0]['entitlements'][0]['licenses'][0]['id']
                return lic_order_updated_key, lic_order_updated[0]['quote']
            else:
                return False
        except Exception as e:
            log.error("Failed to update lic_order, with quote: {}\n. Exception details: {}".format(quote, e))
            return False


    def update_subs_order_to_cancelled(self, quote):
        '''
        Update order to cancelled
        :param quote: Order type, any order
        :return: license order key
        '''
        lic_order = self.order.get_subs_order(quote)

        lic_order[0]['reason'] = 'Cancellation'
        now = datetime.now()
        lic_order[0]['entitlements'][0]['licenses'][0]['appointments']['cancellationDate'] = now.strftime('%d.%m.%Y %H:%M:%S')
        lic_order[0]['entitlements'][0]['licenses'][0]['appointments']['subscriptionEnd'] = \
            lic_order[0]['entitlements'][0]['licenses'][0]['appointments']['cancellationDate']

        try:
            log.info("\n\nOrder: {}\n\n".format(lic_order))
            time.sleep(5)
            res = self.order.update_subs_order(lic_order[0])
            time.sleep(6)
            if res:
                lic_order_updated = self.order.get_subs_order(quote)
                time.sleep(2)
                lic_order_updated_key = lic_order_updated[0]['entitlements'][0]['licenses'][0]['id']
                return lic_order_updated_key, lic_order_updated[0]['quote']
            else:
                return False
        except Exception as e:
            log.error("Failed to update lic_order to Cancellation, with quote: {}\n. Exception details: {}".format(quote, e))
            return False


    def update_qty_subs_order(self, quote, qty):
        '''
                Update order quantity
                :param quote: Order quote
                :param qty: Order quantity
                :return: Order quantity, license order quote
                '''
        lic_order = self.order.get_subs_order(quote)

        lic_order[0]['reason'] = 'Update'
        lic_order[0]['entitlements'][0]['total_qty'] = qty
        lic_order[0]['entitlements'][0]['licenses'][0]['qty'] = qty
        try:
            log.info("\n\nOrder: {}\n\n".format(lic_order))
            time.sleep(2)
            res = self.order.update_subs_order(lic_order[0])
            time.sleep(6)
            if res:
                lic_order_updated = self.order.get_subs_order(quote)
                time.sleep(5)
                lic_order_updated_qty = lic_order_updated[0]['entitlements'][0]['licenses'][0]['qty']

                log.info("Quantity updated: {}".format(lic_order_updated_qty))
                return lic_order_updated_qty, lic_order_updated[0]['quote']
            else:
                return False
        except Exception as e:
            log.error("Failed to update lic_order, with quote: {}\n. Exception details: {}".format(quote, e))
            return False


    def upgrade_subs_tier_ap(self, quote):
        '''
                Upgrade Subscription Tier (foundation to advanced)
                :param quote: Order quote, upgrade Tier from foundation to Advanced
                :return: Order quantity, license order quote
                '''
        lic_order = self.order.get_subs_order(quote)
        time.sleep(2)

        lic_order[0]['reason'] = 'Update'

        for i in range(len(lic_order[0]['entitlements'][0]['product']['attributes'])):
            if (('TIER' == lic_order[0]['entitlements'][0]['product']['attributes'][i]['name']) or
                    ('TIER_AP' == lic_order[0]['entitlements'][0]['product']['attributes'][i]['name'])):
                lic_order[0]['entitlements'][0]['product']['attributes'][i]['value'] = 'AD'
                lic_order[0]['entitlements'][0]['product']['attributes'][i]['valueDisplay'] = 'Advanced'
                log.info("Tier updated: {}".format(lic_order[0]['entitlements'][0]['product']['attributes'][i]))

        try:
            log.info("\n\nOrder: {}\n\n".format(lic_order))
            time.sleep(2)
            res = self.order.update_subs_order(lic_order[0])
            time.sleep(3)
            if res:
                lic_order_updated = self.order.get_subs_order(quote)
                time.sleep(2)

                log.info("Tier upgraded to Advanced.")
                return lic_order_updated[0]['quote']
            else:
                return False
        except Exception as e:
            log.error("Failed to update lic_order, with quote: {}\n. Exception details: {}".format(quote, e))
            return False


    def downgrade_subs_tier_ap(self, quote):
        '''
                Downgrade Subscription Tier (advanced to foundation)
                :param quote: Order quote, downgrade Tier from Advanced to foundation
                :return: Order quantity, license order quote
                '''
        lic_order = self.order.get_subs_order(quote)
        time.sleep(2)

        lic_order[0]['reason'] = 'Update'

        for i in range(len(lic_order[0]['entitlements'][0]['product']['attributes'])):
            if (('TIER' == lic_order[0]['entitlements'][0]['product']['attributes'][i]['name']) or
                    ('TIER_AP' == lic_order[0]['entitlements'][0]['product']['attributes'][i]['name'])):
                lic_order[0]['entitlements'][0]['product']['attributes'][i]['value'] = 'FO'
                lic_order[0]['entitlements'][0]['product']['attributes'][i]['valueDisplay'] = 'Foundation'
                log.info("Tier updated: {}".format(lic_order[0]['entitlements'][0]['product']['attributes'][i]))

        try:
            log.info("\n\nOrder: {}\n\n".format(lic_order))
            time.sleep(2)
            res = self.order.update_subs_order(lic_order[0])
            time.sleep(3)
            if res:
                lic_order_updated = self.order.get_subs_order(quote)
                time.sleep(2)

                log.info("Tier downgraded to Foundation.")
                return lic_order_updated[0]['quote']
            else:
                return False
        except Exception as e:
            log.error("Failed to update lic_order, with quote: {}\n. Exception details: {}".format(quote, e))
            return False
