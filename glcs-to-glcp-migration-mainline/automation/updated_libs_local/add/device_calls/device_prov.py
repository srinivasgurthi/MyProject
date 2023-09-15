"""
Activate Device Direct Provisioning API Library
"""
import io
import os
import socket
import logging
import requests
from os import path
if os.getenv("POD_NAMESPACE") is not None:
    import M2Crypto, hashlib
    import M2Crypto.BIO
log = logging.getLogger(__name__)

class NetworkStorageComputeDeviceProvisionHelper(object):
    """
    Network, Storage, Compute, Device Provision Class
    """

    def __init__(self, CCS_DEVICE_URL, serial_number, part_number,
                 device_type, certs, hpe_device_url=None, aruba_device_url=None, activate_v2_device_url=None,
                 mac_address=None):
        """
        :param CCS_DEVICE_URL: Cluster under test device provisioning URL
        :param serial_number: Serial number of the device
        :param part_number: Part number of the device
        :param device_type: Device type: IAP, SWITCH, GATEWAY, COMPUTE, STORAGE
        :param certs: Certificate
        :param hpe_device_url: hpe device url, public DNS for storage/compute device to call
        using provisioning call
        :param aruba_device_url: aruba device url public DNS for device to call
        using provisioning call
        """
        CLUSTER_PORT = str(443)
        self.CCS_DEVICE_URL = CCS_DEVICE_URL
        self.serial_number = serial_number
        self.part_number = part_number
        self.device_type = device_type
        self.certs = certs
        self.hpe_device_url = hpe_device_url
        self.aruba_device_url = aruba_device_url
        self.activate_v2_device_url= activate_v2_device_url
        self.mac_address = mac_address
        self.CLUSTER_PORT = CLUSTER_PORT
        self.device_ca_file = False

    def resolve_device_hostname_to_IP(self):
        """
        Resolves DNS name for CCS_DEVICE_URL to IP address
        :return: IP address resolves to CCS_DEVICE_URL
        """
        try:
            device_endpoint_ip = socket.gethostbyname(self.CCS_DEVICE_URL)
            log.info("\nDevice endpoint IP : {}".format(device_endpoint_ip))
            return device_endpoint_ip
        except Exception as e:
            log.error("\nUnable to get Hostname and IP!\n".format(e))

    def make_entry_in_pods_hosts_file(self, device_endpoint_ip, device_endpoint_url):
        """
        add Hostname and IP to /etc/hosts file
        :param device_endpoint_ip: CCS_DEVICE_URL
        :param device_endpoint_url: hpe_device_url or aruba_device_url
        """
        try:
            with open('/etc/hosts', 'a') as f:
                f.write("\n{} {}".format(device_endpoint_ip, device_endpoint_url))
                f.close()
            with open('/etc/hosts', 'r')as f:
                hosts_file = f.read()
                log.info("IP : {}".format(hosts_file))
                f.close()
        except Exception as e:
            log.error("\nUnable to add Hostname and IP to /etc/hosts file!\n".format(e))

    def make_device_provision_request(self):
        """
        make device provision request for Storage and Compute device
        :return: provision response for provision request
        """
        cluster_device_endpoint_ip = self.resolve_device_hostname_to_IP()
        method = 'get'
        headers = {}
        api_path = None
        if "STORAGE" in self.device_type:
            api_path = 'storage-provision'
            headers["X-Type"] = "provision-update"
            headers["x-mode"] = "STORAGE"
            headers["x-oem-tag"] = "Nimble"
            headers["x-forwarded-for"] = "2.3.4.5"
            headers["X-ap-info"] = self.serial_number + "," + "None" + "," + self.part_number
            headers["Content-Type"] = "application/json"
        if "COMPUTE" in self.device_type:
            api_path = "compute-provision"
            headers["X-Type"] = "provision-update"
            headers["x-mode"] = "Compute"
            headers['x-subscription-key'] = 'ABCDEFGHIJ0123456789'
            headers["X-ap-info"] = self.serial_number + "," + "None" + "," + self.part_number
            headers["Content-Type"] = "application/json"
        test_params = {"path_params": [], "request_headers": headers, "request_body": {},
                       "cert": self.certs}
        self.make_entry_in_pods_hosts_file(device_endpoint_ip=cluster_device_endpoint_ip,
                                          device_endpoint_url=self.hpe_device_url)
        self.DEVICE_PROVISION_URL = "https://{}:{}".format(self.hpe_device_url, self.CLUSTER_PORT)
        log.info("\nRESOLVED IP FOR DEVICE ENDPOINT AND MADE ENTRY IN ETC/HOSTS FILE FOR POD\n")
        if 'triton' in self.CCS_DEVICE_URL:
            return True
        response = getattr(self, method.lower())(api_path, headers=headers, cert=test_params['cert']['cert'],
                                                 key=test_params['cert']['key'], ca_cert=test_params['cert']['ca_cert'])
        logging.info(
            '\nresponse from server for final provision: {} \nheaders: {} \nstatus_code: {}'.format(response.text, response.headers, response.status_code))
        return response

    def get(self, api_path, cert="", key="", ca_cert=False, headers={}):
        """
        Make get api_request
        :param api_path: for storage and compute device type
        :param cert: path to cert
        :param key: path to key
        :param ca_cert: cert_validation
        :param headers: request headers
        :return: True if 'X-Status-Code' is success in response
        """
        device_ca_file = False
        if device_ca_file:
            device_ca_file = ca_cert
        log.info("\nProcessing GET on URL - {} with headers {}\n".format(path.join(self.DEVICE_PROVISION_URL, api_path), headers))
        response = requests.get(path.join(self.DEVICE_PROVISION_URL, api_path), cert=(cert, key), headers=headers, verify=device_ca_file)
        return response

    def iap_add_call_fn(self):
        """
        make device provision request for IAP, Switch or Gateway device
        :return: provision response for provision request
        """
        cluster_device_endpoint_ip = self.resolve_device_hostname_to_IP()
        self.make_entry_in_pods_hosts_file(device_endpoint_ip=cluster_device_endpoint_ip,
                                          device_endpoint_url=self.aruba_device_url)
        act_url = "https://" + self.aruba_device_url + ":" + self.CLUSTER_PORT + "/provision"
        fw = '8.5.0.5-8.5.0.5_73491'
        headers = dict()
        headers['Content-Length'] = str(0)
        headers['X-Type'] = 'provision-update'
        if self.device_type == "GATEWAY":
            headers['X-Mode'] = "CONTROLLER"
        else:
            headers['X-Mode'] = self.device_type
        headers['X-Oem-Tag'] = 'Aruba'
        headers['X-Current-Version'] = fw
        headers['X-Organization'] = None
        ap_info = self.serial_number + ',' + self.mac_address + ',' + self.part_number
        headers['X-Ap-Info'] = ap_info
        headers['Connection'] = 'Keep-Alive'
        resp = requests.post(act_url, verify=False, headers=headers)
        session = resp.headers.get('X-Session-Id')
        challenge = resp.headers.get('X-Challenge')
        challenge1 = challenge.encode('utf-8')
        log.info('request from server for challenge {} {} {}'.format(resp.status_code, resp.headers, session))
        pkey = M2Crypto.RSA.load_key(self.certs['key'])
        Signature = pkey.sign(hashlib.sha1(challenge1).digest())
        k = io.open((self.certs['cert']), mode="r", encoding="utf-8")
        data1 = k.read().encode('utf-8')
        data2 = Signature
        data = data1 + '\n'.encode() + data2
        length = len(data)
        headers = dict()
        headers['x-req-ver-key'] = str(pkey)
        headers['content-type'] = 'text/plain;charset=utf-8'
        headers['content-length'] = str(length)
        headers['X-Type'] = 'provision-update'
        if self.device_type == "GATEWAY":
            headers['X-Mode'] = "CONTROLLER"
        else:
            headers['X-Mode'] = self.device_type
        headers['X-Oem-Tag'] = 'Aruba'
        headers['X-Current-Version'] = fw
        headers['X-Ap-Info'] = ap_info
        headers['X-Session-Id'] = session
        headers['X-Challenge'] = challenge
        headers['X-Challenge-Hash'] = 'SHA-1'
        headers['Connection'] = 'close'
        logging.info('Response from client for challenge {} {}'.format(headers, session))
        resp = requests.post(act_url, verify=False, headers=headers, data=data)
        logging.info(
            'response from server for final provision {} {} {}'.format(resp.headers, resp.status_code, session))
        return resp

    def add_call_firmware(self, endpoint, x_type, fw_version):
        """

        make device firmware request for IAP, Controller or Gateway device
         :param endpoint: endpoint for device types
         :param x_type: provision-update for provision request, firmware-check for firmware request
         :param fw_version: firmware version
         :return: firmware response for firmware request
        """
        cluster_device_endpoint_ip = self.resolve_device_hostname_to_IP()
        self.make_entry_in_pods_hosts_file(device_endpoint_ip=cluster_device_endpoint_ip,
                                          device_endpoint_url=self.aruba_device_url)
        act_url = "https://" + self.aruba_device_url + ":" + self.CLUSTER_PORT + endpoint
        fw = fw_version
        headers = dict()
        headers['Content-Length'] = str(0)
        headers['X-Type'] = x_type
        if self.device_type == "GATEWAY":
            headers['X-Mode'] = "CONTROLLER"
        else:
            headers['X-Mode'] = self.device_type
        if x_type == "firmware-upgrade":
            headers['X-Desired-Version'] = fw_version
        headers['X-Oem-Tag'] = 'Aruba'
        headers['X-Current-Version'] = fw
        headers['X-Organization'] = None
        ap_info = self.serial_number + ',' + self.mac_address + ',' + self.part_number
        headers['X-Ap-Info'] = ap_info
        headers['Connection'] = 'Keep-Alive'
        logging.info('Processing POST on URL - {}, with headers - headers {}\n'.format(act_url, headers))
        resp = requests.post(act_url, verify=False, headers=headers)
        session = resp.headers.get('X-Session-Id')
        challenge = resp.headers.get('X-Challenge')
        challenge1 = challenge.encode('utf-8')
        log.info('response from server for challenge {} {} {}'.format(resp.status_code, resp.headers, session))
        pkey = M2Crypto.RSA.load_key(self.certs['key'])
        Signature = pkey.sign(hashlib.sha1(challenge1).digest())
        k = io.open((self.certs['cert']), mode="r", encoding="utf-8")
        data1 = k.read().encode('utf-8')
        data2 = Signature
        data = data1 + '\n'.encode() + data2
        length = len(data)
        headers = dict()
        headers['x-req-ver-key'] = str(pkey)
        headers['content-type'] = 'text/plain;charset=utf-8'
        headers['content-length'] = str(length)
        headers['X-Type'] = x_type
        if self.device_type == "GATEWAY":
            headers['X-Mode'] = "CONTROLLER"
        else:
            headers['X-Mode'] = self.device_type
        if x_type == "firmware-upgrade":
            headers['X-Desired-Version'] = fw_version
        headers['X-Oem-Tag'] = 'Aruba'
        headers['X-Current-Version'] = fw
        headers['X-Ap-Info'] = ap_info
        headers['X-Session-Id'] = session
        headers['X-Challenge'] = challenge
        headers['X-Challenge-Hash'] = 'SHA-1'
        headers['Connection'] = 'close'
        logging.info('SENDING RESPONSE BACK TO SERVER FROM CLIENT WITH  headers {} and session {}'.format(headers, session))
        resp = requests.post(act_url, verify=False, headers=headers, data=data)
        logging.info(
            '\nresponse from server for final provision: {} \nheaders: {} \nstatus_code: {} session: {}'.format(resp.text, resp.headers, resp.status_code, session))
        return resp

    def make_switch_provision_request(self, api_path, x_type):
        """
        Make device provision / firmware request for Switch device
        :param api_path: endpoint for switch device types
        :param x_type: provision-update for provision request, firmware-check for firmware request
        :return: True if 'X-Status-Code' is returned in response
        """
        cluster_device_endpoint_ip = self.resolve_device_hostname_to_IP()
        method = 'post'
        headers = {}
        endpoint = api_path
        headers["X-Type"] = x_type
        headers["X-Mode"] = "SWITCH"
        headers["X-Oem-Tag"] = "Aruba"
        headers["X-Forwarded-For"] = "2.3.4.5"
        headers['X-ssl-client-s-dn'] = 'central.com'
        headers['X-Forwarded-Host'] = 'devices-v2.arubanetworks.com'
        headers['X-ssl-client-verify'] = 'SUCCESS'
        headers["X-Ap-Info"] = self.serial_number + "," + self.mac_address + "," + self.part_number
        headers["Content-Type"] = "application/json"

        test_params = {"path_params": [], "request_headers": headers, "request_body": {},
                       "cert": self.certs}
        self.make_entry_in_pods_hosts_file(device_endpoint_ip=cluster_device_endpoint_ip,
                                           device_endpoint_url=self.activate_v2_device_url)
        self.DEVICE_PROVISION_URL = "https://{}:{}".format(self.activate_v2_device_url, self.CLUSTER_PORT)
        log.info("\nRESOLVED IP FOR DEVICE ENDPOINT AND MADE ENTRY IN ETC/HOSTS FILE FOR POD\n")
        if 'triton' in self.CCS_DEVICE_URL:
            return True
        response = getattr(self, method.lower())(endpoint, headers=headers, cert=test_params['cert']['cert'],
                                                 key=test_params['cert']['key'], ca_cert=test_params['cert']['ca_cert'])

        log.info("\n\nAPI RESPONSE :  status: %s, response_text: %s\n\n" % (response.status_code, response.text))
        log.info("\nAPI RESPONSE HEADERS:  {}\n".format(response.headers))

        return response

    def post(self, endpoint, cert="", key="", ca_cert=False, headers={}):
        """
            Make get api_request
            :param api_path: for switch device type
            :param cert: path to cert
            :param key: path to key
            :param ca_cert: cert_validation
            :param headers: request headers
            :return: response
        """
        if self.device_ca_file:
            self.device_ca_file = ca_cert
        log.info("\nProcessing POST on URL - {}, with headers - {} \n".format(
            path.join(self.DEVICE_PROVISION_URL, endpoint), headers))
        response = requests.post(path.join(self.DEVICE_PROVISION_URL, endpoint), cert=(cert, key), headers=headers,
                                 verify=self.device_ca_file)
        return response