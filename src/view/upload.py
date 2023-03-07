from flask import Blueprint, request, jsonify
from src.utils.s3 import upload_file_to_s3
from src.utils.files import is_valid_file_schema
from src.utils.utils import get_epoch_timestamp, get_current_datetime
from src.utils.db import update_file_record, get_error_file_record

upload = Blueprint(name="upload", import_name=__name__)


# Takes around 3 seconds to upload file to S3 with field validation
@upload.route("/", methods=(["POST"]))
def upload_batch_file_to_s3():
    try:
        file = request.files['file']
        file_type = request.form["type"]
        tenant = request.form["tenant"]
    except:
        return jsonify(f"Missing request params"), 400

    if 'file' not in request.files:
        return jsonify(f"No file uploaded"), 400

    elif file_type not in ('spend', 'user'):
        return jsonify(f"Invalid file type"), 400

    else:
        if is_valid_file_schema(file, file_type):
            try:
                file.filename = f'{get_epoch_timestamp()}-{file.filename}'
                response = upload_file_to_s3(file, file_type, tenant)

                if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                    return jsonify(f"Upload success"), 200
                else:
                    return jsonify(f"File uploaded but record not persisted"), 500

            except:
                return jsonify("Unable to upload file"), 500

        else:
            return jsonify("Invalid file format. Please check your file schema."), 400


@upload.route("/glue", methods=(["PATCH"]))
def update_file_process_status():
    try:
        data = request.get_json()
        filename = data["filename"]
        numberOfProcessed = data["numberOfProcessed"]
        numberOfRejected = data["numberOfRejected"]
        errorFileURL = data["errorFileURL"]
    except:
        return jsonify(f"Invalid request body"), 400

    completeDateTime = get_epoch_timestamp()

    response = update_file_record(filename, completeDateTime, numberOfProcessed, numberOfRejected, errorFileURL)

    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return jsonify(f"Record for file {filename} updated"), 200
    else:
        return jsonify(f"Unable to update record"), 500


@upload.route("/healthcheck", methods=(["GET"]))
def healthcheck():
    return jsonify(f"Healthy"), 200
