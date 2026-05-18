import os
import boto3
from botocore.exceptions import ClientError
from urllib.parse import urlparse
import logging

logger = logging.getLogger("Clinica-LENS-Storage")

class StorageBackend:
    """
    Enterprise Object Storage interface for Clinica-LENS.
    Abstracts S3-compatible endpoints (AWS S3, MinIO) for stateless API/Worker communication.
    """
    def __init__(self):
        self.endpoint_url = os.getenv("S3_ENDPOINT_URL")
        self.access_key = os.getenv("S3_ACCESS_KEY", "minioadmin")
        self.secret_key = os.getenv("S3_SECRET_KEY", "minioadmin")
        self.bucket_name = os.getenv("S3_BUCKET_NAME", "clinica-lens-data")
        
        self.s3_client = boto3.client(
            's3',
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key
        )
        self._ensure_bucket()

    def _ensure_bucket(self):
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404':
                try:
                    self.s3_client.create_bucket(Bucket=self.bucket_name)
                    logger.info(f"Created S3 bucket: {self.bucket_name}")
                except Exception as ex:
                    logger.warning(f"Could not create bucket (it might already exist or credentials lack permissions): {ex}")

    def upload_file(self, file_obj, object_name):
        """Uploads a file-like object to S3 and returns the s3:// URI."""
        try:
            self.s3_client.upload_fileobj(file_obj, self.bucket_name, object_name)
            s3_uri = f"s3://{self.bucket_name}/{object_name}"
            logger.info(f"Successfully uploaded {object_name} to S3.")
            return s3_uri
        except ClientError as e:
            logger.error(f"Failed to upload to S3: {e}")
            raise

    def download_file(self, s3_uri, download_path):
        """Downloads an object from an s3:// URI to a local path."""
        try:
            parsed = urlparse(s3_uri)
            bucket = parsed.netloc
            key = parsed.path.lstrip('/')
            
            self.s3_client.download_file(bucket, key, download_path)
            logger.info(f"Successfully downloaded {s3_uri} to {download_path}.")
            return download_path
        except ClientError as e:
            logger.error(f"Failed to download from S3: {e}")
            raise
