import boto3
import os

s3_resource = boto3.resource("s3")
s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv('ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('SECRET_ACCESS_KEY'),
)

buckets = {
    "user": "user-t3-bucket",
    "spend": "spend-t3-bucket"
}


def upload_file_to_s3(file, file_type):
    # Choose a bucket by name
    prefix = "raw"

    # Write a string to a file in S3
    s3_client.upload_fileobj(file, buckets[file_type], f"{prefix}/{file.filename}")


'''
Listing objects in s3 bucket
'''


def list_files_from_s3(file_type):
    # Specify the bucket and folder
    bucket_name = buckets[file_type]
    prefix = "error"

    # Retrieve the objects in the folder
    bucket = s3_resource.Bucket(bucket_name)

    files = [obj.key for obj in bucket.objects.filter(Prefix=prefix)]
    return files


def download_file_from_s3(file_type, file_name):
    # Specify the bucket and folder
    bucket_name = buckets[file_type]
    prefix = "error"

    # Download the file
    bucket = s3_resource.Bucket(bucket_name)
    object_key = prefix + "/" + file_name
    file = bucket.download_file(object_key, file_name)

    return file
