import boto3
import os
from src.utils.utils import get_current_datetime

dynamodb = boto3.resource(
    service_name="dynamodb",
    region_name=os.getenv("REGION"),
    aws_access_key_id=os.getenv("ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY")
)

table = dynamodb.Table("upload")

PARTITION_KEY_VALUE = "filename"


def insert_file_record(file, file_url):
    payload = {
        PARTITION_KEY_VALUE: f"{file.filename}",
        "uploadDateTime": get_current_datetime(),
        "completeDateTime": "",
        "numberOfProcessed": 0,
        "numberOfRejected": 0,
        "url": {
            "raw": f"{file_url}",
            "error": "",
        }
    }
    response = table.put_item(Item=payload)
    return response


# Update file record with completeDateTime, numberOfProcessed, numberOfRejected and error file URL
def update_file_record(filename, completeDateTime, numberOfProcessed, numberOfRejected, errorFileURL):
    response = table.update_item(
        Key={
            "filename": filename,
        },
        UpdateExpression="set completeDateTime = :val1, numberOfProcessed = :val2, numberOfRejected = :val3, #link.#err = :val4",
        ExpressionAttributeValues={
            ":val1": completeDateTime,
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


#
