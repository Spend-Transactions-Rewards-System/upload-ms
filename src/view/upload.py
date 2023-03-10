from flask import Blueprint, request
from src.utils.s3 import upload_file_to_s3
from src.utils.files import is_valid_file_schema
from src.utils.utils import get_epoch_timestamp
from src.utils.db import update_file_record
from src.model.jsonResponse import JsonResponse

upload = Blueprint(name="upload", import_name=__name__)


# Takes around 3 seconds to upload file to S3 with field validation
@upload.route("/", methods=(["POST"]))
def upload_batch_file_to_s3():
    try:
        file = request.files['file']
        file_type = request.form["type"]
        tenant = request.form["tenant"]
    except:
        return JsonResponse(f"Missing request form parameters", 400).send_response()

    if 'file' not in request.files:
        return JsonResponse(f"No file uploaded", 400).send_response()

    elif file_type not in ('spend', 'user'):
        return JsonResponse(f"Invalid file type", 400).send_response()

    else:
        if is_valid_file_schema(file, file_type):
            try:
                file.filename = f'{get_epoch_timestamp()}-{file.filename}'
                response = upload_file_to_s3(file, file_type, tenant)

                if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                    return JsonResponse(f"Upload success", 200).send_response()
                else:
                    return JsonResponse(f"File uploaded but record not persisted", 500).send_response()

            except:
                return JsonResponse("Unable to upload file", 500).send_response()

        else:
            return JsonResponse("Invalid file format. Please check your file schema.", 400).send_response()


@upload.route("/glue", methods=(["PATCH"]))
def update_file_process_status():
    try:
        data = request.get_json()
        filename = data["filename"]
        numberOfProcessed = data["numberOfProcessed"]
        numberOfRejected = data["numberOfRejected"]
        errorFileURL = data["errorFileURL"]
    except:
        return JsonResponse(f"Invalid request body", 400).send_response()

    completeDateTime = get_epoch_timestamp()

    response = update_file_record(filename, completeDateTime, numberOfProcessed, numberOfRejected, errorFileURL)

    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return JsonResponse(f"Record for file {filename} updated", 200).send_response()
    else:
        return JsonResponse(f"Unable to update record", 500).send_response()


@upload.route("/healthcheck", methods=(["GET"]))
def healthcheck():
    return JsonResponse("Healthy", 200).send_response()
