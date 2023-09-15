import time
import json
import logging
log = logging.getLogger(__name__)
from hpe_glcp_automation_lib.libs.authn.app_api.appsession import AppSession

class ActivateOrder(AppSession):
    def __init__(self, host, sso_host, client_id, client_secret):
        self.base_url = host
        super(ActivateOrder, self).__init__(host, sso_host, client_id, client_secret)
        self.get_token()

    def postManufacturingOrder(self, app_api_url, payload, device_category):
        url = f"{app_api_url}/activate-order/v1/manufacturing/{device_category}"
        log.info(f"Going to POST manufacturing order line data...url: {0}, data{1}".format(url, payload))
        res = self.post(url=url, json=payload)
        log.info(res)
        return res

    def postPointOfSalesOrder(self, app_api_url, payload, device_category):
        url = f"{app_api_url}/activate-order/v1/sales/pos/{device_category}"
        log.info(f"Going to POST point of sales order data...url: {0}, data{1}".format(url, payload))
        res = self.post(url=url, json=payload)
        log.info(res)
        return res

    def postSdsOrder(self, app_api_url, payload, device_category):
        url = f"{app_api_url}/activate-order/v1/sales/direct/{device_category}"
        log.info(f"Going to POST sale direct order line data...url: {0}, data{1}".format(url, payload))
        res = self.post(url=url, json=payload)
        log.info(res)
        return res

    def postLicOrder(self, app_api_url, payload, device_category):
        url = f"{app_api_url}/activate-order/v1/license/{device_category}"
        log.info(f"Going to POST manufacturing order line data...url: {0}, data{1}".format(url, payload))
        res = self.post(url=url, json=payload)
        log.info(res)
        return res

    def getLicOrder(self, app_api_url, device_category, objKey):
        url = f"{app_api_url}/activate-order/v1/license/{device_category}/{objKey}"
        res = self.get(url=url)
        log.info(res)
        return res

    def createPartName(self, app_api_url, payload, device_category, objKey):
        url = f"{app_api_url}/activate-order/v1/part/{device_category}/{objKey}"
        res = self.post(url=url, json=payload)
        log.info(res)
        return res

    def getPartName(self, app_api_url, device_category, objKey):
        url = f"{app_api_url}/activate-order/v1/part/{device_category}/{objKey}"
        res = self.get(url=url)
        log.info(res)
        return res

    def createPlatform(self, app_api_url, payload):
        url = f"{app_api_url}/activate-order/v1/platform"
        res = self.post(url=url, json=payload)
        log.info(res)
        return res

    def getPlatform(self, app_api_url, device_category, objKey):
        url = f"{app_api_url}/activate-order/v1/platform/{device_category}/{objKey}"
        res = self.get(url=url)
        log.info(res)
        return res

    def updateMfr(self, app_api_url, payload, device_category, objKey):
        url = f"{app_api_url}/activate-order/v1/manufacturing/{device_category}/{objKey}"
        res = self.put(url=url, json=payload)
        log.info(res)
        return res

    def updateNewChild(self, app_api_url, payload, device_category, objKey):
        url = f"{app_api_url}/activate-order/v1/manufacturing/{device_category}/{objKey}/addChild"
        res = self.put(url=url, json=payload)
        log.info(res)
        return res

    def getMfrOrderEthMac(self, app_api_url, device_category, ethMac):
        url = f"{app_api_url}/activate-order/v1/manufacturing/{device_category}/ethMac/{ethMac}"
        res = self.get(url=url)
        log.info(res)
        return res

    def getMfrOrderSN(self, app_api_url, device_category, Serial):
        url = f"{app_api_url}/activate-order/v1/manufacturing/{device_category}/serial/{Serial}"
        res = self.get(url=url)
        log.info(res)
        return res

    def getMfrOrderObjKey(self, app_api_url, device_category, objKey):
        url = f"{app_api_url}/activate-order/v1/manufacturing/{device_category}/{objKey}"
        res = self.get(url=url)
        log.info(res)
        return res

