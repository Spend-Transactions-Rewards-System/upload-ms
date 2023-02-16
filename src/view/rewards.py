from flask import Blueprint, request, jsonify
from src.utils.s3 import upload_file_to_s3
from src.utils.files import is_valid_file_schema

rewards = Blueprint(name="rewards", import_name=__name__)


@rewards.route("/upload", methods=(["POST"]))
def batch_file_upload_to_s3():
    file = request.files['file']
    file_type = request.form["type"]

    if 'file' not in request.files:
        return jsonify("No file uploaded"), 400
    else:
        if is_valid_file_schema(file):
            try:
                # upload_file_to_s3(file, file_type)
                return jsonify("File uploaded"), 200
            except:
                return jsonify("Unable to upload file"), 500
        else:
            return jsonify("Invalid file format. Please check your file schema."), 400

# After file upload, will use AWS glue to process points based on:
#   Base Earn Rate
#   Category rewards
#   Campaigns
# Insert data into





def get_transactions_by_user():
    # TODO: Get card_ids of user --> Auth endpoint
    # TODO: Get transactions based on card_ids
    pass
