from flask import Blueprint, request, jsonify
from src.utils.s3 import upload_file_to_s3
from src.utils.files import is_valid_file_schema
from src.utils.utils import get_epoch_timestamp, get_current_datetime
from src.utils.db import update_file_record

upload = Blueprint(name="upload", import_name=__name__)


# Takes around 3 seconds to upload file to S3 with field validation
@upload.route("/", methods=(["POST"]))
def batch_file_upload_to_s3():
    file = request.files['file']
    file_type = request.form["type"]

    if 'file' not in request.files:
        return jsonify("No file uploaded"), 400
    elif file_type not in ('spend', 'user'):
        return jsonify("Invalid file type"), 400
    else:
        if is_valid_file_schema(file):
            try:
                file.filename = f'{get_epoch_timestamp()}-{file.filename}'
                response = upload_file_to_s3(file, file_type)

                if response:
                    return jsonify("File uploaded"), 200
                else:
                    return jsonify("File uploaded but record not persisted"), 500
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

    completeDateTime = get_current_datetime()

    response = update_file_record(filename, completeDateTime, numberOfProcessed, numberOfRejected, errorFileURL)

    return jsonify(f"Record for file {filename} updated"), 200 if response["ResponseMetadata"]["HTTPStatusCode"] == 200 else jsonify(f"Unable to update record"), 500
