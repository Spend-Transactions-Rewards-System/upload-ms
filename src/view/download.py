from flask import Blueprint, request, jsonify, send_file
from src.utils.s3 import download_file_from_s3
from src.utils.db import get_error_file_record
from src.utils.utils import is_valid_url

download = Blueprint(name="download", import_name=__name__)


@download.route("/list", methods=(["GET"]))
def get_error_files():
    limit = request.args.get('limit', default=1000, type=int)
    try:
        tenant = request.form["tenant"]
    except:
        return jsonify(f"Missing tenant field"), 400

    response = get_error_file_record(tenant, limit)

    return jsonify(response), 200


@download.route("/error", methods=(["GET"]))
def download_error_file():
    try:
        url = request.args.get("url")
    except ValueError:
        return jsonify(f"url not found"), 400

    if is_valid_url(url):
        try:
            file_stream, filename = download_file_from_s3(url)
            return send_file(file_stream, as_attachment=True, download_name=filename)
        except:
            return jsonify(f"Error downloading file. Invalid URL"), 400
    else:
        return jsonify(f"Invalid URL"), 400

# http://127.0.0.1:8080/api/v1/download/error?url=https://spend-t3-bucket.s3.ap-southeast-1.amazonaws.com/error/1678195110-spend.csv
