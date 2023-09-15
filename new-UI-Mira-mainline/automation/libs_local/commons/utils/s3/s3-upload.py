import base64
import json
import os
import subprocess

from hpe_glcp_automation_lib.libs.commons.utils.s3.s3_utils import S3Utils


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


def s3_path():
    cluster_info_file = "/configmap/data/infra_clusterinfo.json"
    with open(cluster_info_file) as cluster_info:
        cluster_info_json = cluster_info.read()
    cluster_info_dict = json.loads(cluster_info_json)
    return (
        cluster_info_dict.get("clusterinfo", {})
        .get("INPUTENV", {})
        .get("S3PATH", "localhost")
    )


b_name, access_key, secret_key = s3_details()
S3path = s3_path()
if S3path != "localhost":
    s3 = S3Utils(
        bucket_name=b_name,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )

    for root, dirs, files in os.walk("/tmp/results"):
        for name in files:
            file_path = os.path.join(root, name)
            target_file_path = file_path
            if target_file_path.startswith(os.path.join("/tmp/results")):
                target_file_path = target_file_path[
                                   len(os.path.join("/tmp/results")):
                                   ]
            if s3 is not None:
                targ_file = os.path.normpath(
                    S3path + "/allurejson/" + target_file_path
                ).lstrip("/")
                filep = os.path.normpath(file_path)
                s3.upload_file(target_filepath=targ_file, file_path=filep)

    for root, dirs, files in os.walk("/tmpdir/results/testrail"):
        for name in files:
            file_path = os.path.join(root, name)
            print(file_path)
            target_file_path = file_path
            if target_file_path.startswith(os.path.join("/tmpdir/results/testrail")):
                target_file_path = target_file_path[
                                   len(os.path.join("/tmpdir/results/testrail")):
                                   ]
                print(target_file_path)
            if s3 is not None:
                testrail_s3path = "testrail/" + S3path.split('/')[0]
                print("S3Path to upload testrail xml is:" + testrail_s3path)
                targ_file = os.path.normpath(
                    testrail_s3path + target_file_path
                ).lstrip("/")
                print(targ_file)
                filep = os.path.normpath(file_path)
                print(filep)
                s3.upload_file(target_filepath=targ_file, file_path=filep)
