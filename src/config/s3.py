from io import BytesIO
from pathlib import Path
import typing

import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from botocore.response import StreamingBody

class S3BucketService:
    """Service to manage interactive with s3 store."""

    def __init__(
        self,
        bucket_name: str,
        endpoint: str,
        access_key: str,
        secret_key: str,
    ) -> None:
        """Setup for connect with store."""
        self.bucket_name = bucket_name
        self.endpoint = endpoint
        self.access_key = access_key
        self.secret_key = secret_key

    def create_s3_client(self) -> boto3.client:
        """Create s3 client."""
        client = boto3.client(
            "s3",
            endpoint_url=self.endpoint,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            config=Config(signature_version="s3v4"),
        )
        return client

    def upload_file_object(
        self,
        prefix: str,
        source_file_name: str,
        content: Union[str, bytes],
    ) -> str:
        """Upload file object in store."""
        client = self.create_s3_client()
        destination_path = str(Path(prefix, source_file_name))

        if not isinstance(content, bytes):
            content = content.encode("utf-8")

        buffer = BytesIO(content)

        client.upload_fileobj(buffer, self.bucket_name, destination_path)

        # Return file object path
        return str(
            Path(
                self.endpoint,
                self.bucket_name,
                prefix,
                source_file_name,
            ),
        )

    def delete_file_object(self, prefix: str, source_file_name: str) -> None:
        """Delete file object."""
        client = self.create_s3_client()
        path_to_file = str(Path(prefix, source_file_name))
        client.delete_object(Bucket=self.bucket_name, Key=path_to_file)