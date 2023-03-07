import boto3
import os
from src.utils.utils import get_epoch_timestamp, buckets
from dynamodb_json import json_util
from boto3.dynamodb.conditions import Key
from collections import defaultdict

TABLENAME = "upload"

PARTITION_KEY_VALUE = "tenant"
SORT_KEY_VALUE = "uploadTimestamp"

GSI = "filename-uploadTimestamp-index"
GSI_PARTITION_KEY_VALUE = "filename"
GSI_SORT_KEY_VALUE = "uploadTimestamp"

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

table = dynamodb.Table(TABLENAME)


def insert_file_record(file, file_url, file_type, tenant):
    payload = {
        PARTITION_KEY_VALUE: tenant,
        SORT_KEY_VALUE: get_epoch_timestamp(),
        "filename": f"{file.filename}",
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
def update_file_record(filename, completeTimestamp, numberOfProcessed, numberOfRejected, errorFileURL):
    try:
        file_record = table.query(
            TableName=TABLENAME,
            IndexName=GSI,
            KeyConditionExpression=Key('filename').eq(filename)
        )["Items"][0]
    except IndexError:
        return None

    # Validate if record has been updated before
    if file_record["url"]["error"] != "":
        return None

    response = table.update_item(
        Key={
            PARTITION_KEY_VALUE: file_record["tenant"],
            SORT_KEY_VALUE: file_record["uploadTimestamp"]
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


# get error file records of tenant
def get_error_file_record(tenant, limit):
    response = table.query(
        KeyConditionExpression=Key(PARTITION_KEY_VALUE).eq(tenant),
        FilterExpression='#link.#err <> :empty_string',
        ExpressionAttributeValues={
            ':empty_string': {'S': ''}
        },
        ExpressionAttributeNames={
            "#link": "url",
            "#err": "error",
        },
        ScanIndexForward=False,
        Limit=limit
    )
    return json_util.loads(json_util.dumps(response["Items"]))