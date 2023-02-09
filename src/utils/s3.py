import boto3
import os


'''
Inserting objects into s3 bucket
'''


def upload_file_to_s3(file):
    # Connect to the S3 service
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv('ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('SECRET_ACCESS_KEY'),
    )

    # Choose a bucket by name
    bucket_name = "batch-buckets"
    folder_name = "transaction_data_raw"

    # Write a string to a file in S3
    s3.upload_fileobj(file, bucket_name, f"{folder_name}/{file.filename}")


'''
Listing objects in s3 bucket
'''
# s3 = boto3.resource("s3")

# Choose a bucket by name
# bucket_name = "your-bucket-name"
# bucket = s3.Bucket(bucket_name)

# List the contents of the bucket
# for obj in bucket.objects.all():
#    print(obj.key)
