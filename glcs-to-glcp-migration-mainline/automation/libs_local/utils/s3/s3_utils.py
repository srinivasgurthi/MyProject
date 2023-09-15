import boto3
import botocore
from boto3.s3.transfer import TransferConfig

## 1024 * 25 upload size
SIZE_UPLOAD = 25600
MAX_THREAD_CONCURRENCY = 10


class S3Utils(object):
    def __init__(
        self,
        bucket_name,
        aws_access_key_id="",
        aws_secret_access_key="",
        region_name=None,
    ):
        """Bucket (str) -- The name of the bucket to access
        aws credentials will read it from .aws dir if not set
        """
        self.session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )
        self.s3conn = self.session.resource("s3")
        self.bucket_name = bucket_name

    def download_file(self, key, target_filepath):
        """target_filepath (str) -- The path to the file to download to.
        Key (str) -- The name of the key to download from
        """
        try:
            print(self.bucket_name)
            self.s3conn.Bucket(self.bucket_name).download_file(key, target_filepath)
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "404":
                print(
                    "The key %s does not exist in the bucket %s"
                    % (key, self.bucket_name)
                )
            else:
                raise
        return target_filepath

    def upload_file(self, file_path, target_filepath, ExtraArgs=None):
        """
        upload file to S3 bucket
        :param file_path:
        :param target_filepath:
        :param ExtraArgs:
        :return:
        """
        self.s3conn.meta.client.upload_file(
            file_path, self.bucket_name, target_filepath, ExtraArgs=ExtraArgs
        )

    def multi_part_upload_with_s3(
        self,
        file_path,
        target_filepath,
        max_concurrency=None,
        multipart_threshold=None,
        multipart_chunksize=None,
        use_threads=None,
    ):
        """
            upload file to s3 in multipart
        :param file_path: actual file path which needs to be uploaded.
        :param target_filepath: target file path for S3 bucket
        :param max_concurrency: Number of threads running in parallel, Default to 10
        :param multipart_threshold: Default 1024*25
        :param multipart_chunksize: Default 1024*25
        :param use_threads: Default to True
        :return:
        """
        if max_concurrency is None:
            max_concurrency = MAX_THREAD_CONCURRENCY
        if multipart_threshold is None:
            multipart_threshold = SIZE_UPLOAD
        if multipart_chunksize is None:
            multipart_chunksize = SIZE_UPLOAD
        if use_threads is None:
            use_threads = True

        config = TransferConfig(
            multipart_threshold=multipart_threshold,
            max_concurrency=max_concurrency,
            multipart_chunksize=multipart_chunksize,
            use_threads=use_threads,
        )
        self.s3conn.meta.client.upload_file(
            file_path, self.bucket_name, target_filepath, Config=config
        )