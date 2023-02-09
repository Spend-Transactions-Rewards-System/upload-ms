from flask import Blueprint, request, jsonify
from src.utils.s3 import upload_file_to_s3
from src.utils.mcc import get_mcc_category

rewards = Blueprint(name="rewards", import_name=__name__)


@rewards.route("/upload", methods=(["POST"]))
def batch_file_upload_to_s3():
    file = request.files['file']
    if 'file' not in request.files:
        return jsonify("No file uploaded"), 403
    else:
        try:
            upload_file_to_s3(file)
            return jsonify("file uploaded"), 200
        except:
            return jsonify("unable to upload file"), 500


@rewards.route("/mcc/<int:code>", methods=(["GET"]))
def get_mcc_by_code(code):
    print(code)
    mcc_category = get_mcc_category(code)
    if mcc_category:
        return jsonify({
            "code": code,
            "description": get_mcc_category(code)
        }), 200
    return jsonify("Unable to find MCC"), 403
