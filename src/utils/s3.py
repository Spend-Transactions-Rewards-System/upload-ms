import boto3
import os
from datetime import datetime
from src.utils.db import insert_file_record
from src.utils.utils import get_bucket_name

s3_resource = boto3.resource(
    "s3",
    aws_access_key_id=os.getenv('ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('SECRET_ACCESS_KEY')
)
s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv('ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('SECRET_ACCESS_KEY'),
)


def upload_file_to_s3(file, file_type, tenant):
    # Choose a bucket by name
    prefix = "raw"
    bucket_name = get_bucket_name(file_type)

    s3_client.upload_fileobj(file, bucket_name, f"{prefix}/{file.filename}")

    file_url = f"https://{bucket_name}.s3.{os.getenv('REGION')}.amazonaws.com/{prefix}/{file.filename}"

    response = insert_file_record(file, file_url, file_type, tenant)

    return response


def download_file_from_s3(url):
    url_arr = url.split('/')
    bucket_name, filename = url_arr[2].split(".")[0], f"error-{url_arr[4]}"
    s3_key = '/'.join(url_arr[3:])

    s3_object = s3_client.get_object(Bucket=bucket_name, Key=s3_key)
    file_stream = s3_object['Body']

    return file_stream, filename
