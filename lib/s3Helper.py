import boto3
from botocore.client import Config


class S3Helper:
    def __init__(self, bucket, region="eu-west-2") -> None:
        super().__init__()
        self.bucket = bucket
        self.region = region
        self.s3_client = boto3.client('s3', config=Config(signature_version='s3v4', s3={'addressing_style': 'path'}),
                                      region_name=self.region)

    def put_object(self, key, body, content_type):
        self.s3_client.put_object(Body=body, Bucket=self.bucket, Key=key, ContentType=content_type)
