import base64
import json
import os
import subprocess

from hpe_glcp_automation_lib.libs.utils.s3.s3_utils import S3Utils

def s3_details():
    kube_output_bytes = subprocess.check_output(
        "kubectl get secret -n cloudops automations3secret -o json", shell=True
    )
    kube_output_string = kube_output_bytes.decode("utf-8")
    output_dict = json.loads(kube_output_string)
    bucket_name = base64.b64decode(
        output_dict.get("data", {}).get("bucket_name", "")
    ).decode("utf-8")
    aws_access_key_id = base64.b64decode(
        output_dict.get("data", {}).get("aws_access_key_id", "")
    ).decode("utf-8")
    aws_secret_access_key = base64.b64decode(
        output_dict.get("data", {}).get("aws_secret_access_key", "")
    ).decode("utf-8")
    return bucket_name, aws_access_key_id, aws_secret_access_key

def download_file(s3_file):
    b_name, access_key, secret_key = s3_details()
    bucket_name, aws_access_key_id, aws_secret_access_key, = s3_details()
    s3 = S3Utils(
        bucket_name=b_name,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )
    bucket = s3.s3conn.Bucket(bucket_name)
    for obj in bucket.objects.filter(Prefix=s3_file):
        os.makedirs(os.path.dirname(obj.key), exist_ok=True)
        s3.download_file(obj.key, obj.key)


download_file('sol-auto/creds/login_info_ver-1.json')
download_file('sol-auto/creds/appcat_login_info_ver-1.json')
download_file('sol-auto/creds/acct_mgmt_login_info.json')