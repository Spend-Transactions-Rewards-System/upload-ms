import boto3
import os
from src.utils.utils import get_epoch_timestamp, buckets
from dynamodb_json import json_util
from collections import defaultdict

dynamodb = boto3.resource(
    service_name="dynamodb",
    region_name=os.getenv("REGION"),
    aws_access_key_id=os.getenv("ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY")
)

dynamodb_client = boto3.client(
    service_name="dynamodb",
    region_name=os.getenv("REGION"),
    aws_access_key_id=os.getenv("ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY")
)

table = dynamodb.Table("upload")

PARTITION_KEY_VALUE = "filename"
SORT_KEY_VALUE = "tenant"

GSI = "filename-uploadTimestamp-index"


def insert_file_record(file, file_url, file_type, tenant):
    payload = {
        PARTITION_KEY_VALUE: f"{file.filename}",
        "uploadTimestamp": get_epoch_timestamp(),
        "tenant": tenant,
        "type": file_type,
        "completeTimestamp": 0,
        "numberOfProcessed": 0,
        "numberOfRejected": 0,
        "url": {
            "raw": f"{file_url}",
            "error": "",
        }
    }
    response = table.put_item(Item=payload)
    return response


# Update file record with completeTimestamp, numberOfProcessed, numberOfRejected and error file URL
def update_file_record(tenant, filename, completeTimestamp, numberOfProcessed, numberOfRejected, errorFileURL):
    response = table.update_item(
        Key={
            "tenant": tenant,
            "filename": filename
        },
        UpdateExpression="set completeTimestamp = :val1, numberOfProcessed = :val2, numberOfRejected = :val3, #link.#err = :val4",
        ExpressionAttributeValues={
            ":val1": completeTimestamp,
            ":val2": numberOfProcessed,
            ":val3": numberOfRejected,
            ":val4": errorFileURL,
        },
        ExpressionAttributeNames={
            "#link": "url",
            "#err": "error"
        },
        ReturnValues="UPDATED_NEW"
    )
    return response


# get file records of tenant
def get_error_file_record(tenant, limit):
    item_dict = []
    for file_type in buckets.keys():
        response = table.query(
            KeyConditionExpression='tenant = :tenant',
            FilterExpression='#filetype = :type AND #link.#err <> :empty_string',
            ExpressionAttributeValues={
                ':tenant': {'S': tenant},
                ':type': {'S': file_type},
                ':empty_string': {'S': ''}
            },
            ExpressionAttributeNames={
                "#link": "url",
                "#err": "error",
                "#filetype": "type"
            },
            ScanIndexForward=False,
            Limit=limit
        )
        item_dict.extend(json_util.loads(json_util.dumps(response["Items"])))
    return item_dict

# search by tenant, descending order by epoch timestamp, limit 10
