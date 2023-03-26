from flask import Blueprint, request, send_file
from src.model.jsonResponse import JsonResponse

healthcheck = Blueprint(name="healthcheck", import_name=__name__)


@healthcheck.route("/", methods=(["GET"]))
def healthcheck_ep():
    return JsonResponse("Healthy", 200).send_response()
