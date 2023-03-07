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
    
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return "success"
    else:
        return None


'''
Listing objects in s3 bucket
'''


def list_files_from_s3(file_type):
    # Specify the bucket and folder
    bucket_name = get_bucket_name(file_type)
    prefix = "error"

    # Retrieve the objects in the folder
    bucket = s3_resource.Bucket(bucket_name)

    files = [obj.key for obj in bucket.objects.filter(Prefix=prefix)]
    return files


def download_file_from_s3(file_type, file_name):
    # Specify the bucket and folder
    bucket_name = get_bucket_name(file_type)
    prefix = "error"

    # Download the file
    bucket = s3_resource.Bucket(bucket_name)
    object_key = prefix + "/" + file_name
    file = bucket.download_file(object_key, file_name)

    return file
