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

class NetworkStorageComputeDeviceProvisionHelper:
    """Used for API helper which can be a common utils across services."""

    def __init__(self, CCS_DEVICE_URL, serial_number, part_number,
                 device_type, certs, hpe_device_url=None, aruba_device_url=None,
                 mac_address=None):
        CLUSTER_PORT = str(443)
        self.CCS_DEVICE_URL = CCS_DEVICE_URL
        self.serial_number = serial_number
        self.part_number = part_number
        self.device_type = device_type
        self.certs = certs
        self.hpe_device_url = hpe_device_url
        self.aruba_device_url = aruba_device_url
        self.mac_address = mac_address
        self.CLUSTER_PORT = CLUSTER_PORT

    def resolve_device_hostname_to_IP(self):
        try:
            device_endpoint_ip = socket.gethostbyname(self.CCS_DEVICE_URL)
            log.info("\nDevice endpoint IP : {}".format(device_endpoint_ip))
            return device_endpoint_ip
        except Exception as e:
            log.error("\nUnable to get Hostname and IP!\n".format(e))

    def make_entry_in_pods_hosts_file(self, device_endpoint_ip, device_endpoint_url):
        """add Hostname and IP to /etc/hosts file"""
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
        if response.headers['X-Status-Code'] == "success":
            return True
        else:
            return False

    def get(self, api_path, cert="", key="", ca_cert=False, headers={}):
        device_ca_file = False
        if device_ca_file:
            device_ca_file = ca_cert
        log.info("\nProcessing GET on URL - {} with headers {}\n".format(path.join(self.DEVICE_PROVISION_URL, api_path), headers))
        response = requests.get(path.join(self.DEVICE_PROVISION_URL, api_path), cert=(cert, key), headers=headers, verify=device_ca_file)
        return response

    def iap_add_call_fn(self):
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
        if resp.headers.get('X-Status-Code') != 'success':
            return False
        return True