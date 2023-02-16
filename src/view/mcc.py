from flask import Blueprint, request, jsonify
from sqlalchemy import insert
from src.model.mcc import MCC
from src.utils.db import db
from src.utils.mcc import MCC_LIST

mcc = Blueprint(name="mcc", import_name=__name__)


@mcc.route("/<int:code>", methods=(["GET"]))
def get_mcc_by_code(code):
    # TODO
    return jsonify("Unable to find MCC"), 400


@mcc.route("/insert", methods=(["POST"]))
def insert_mcc():
    mccs = [{"mcc": k, "description": v} for k, v in MCC_LIST.items()]
    result = db.session.execute(insert(MCC).returning(MCC), mccs)  # bulk insert
    db.session.commit()
    if result:
        return jsonify("MCCs inserted"), 200
    else:
        return jsonify("Unable to insert MCCs"), 500
