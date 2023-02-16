from flask import Blueprint, request, jsonify
from src.model.merchant import Merchant
from src.utils.db import db

merchant = Blueprint(name="merchant", import_name=__name__)


@merchant.route("/", methods=(["POST"]))
def insert_merchant():
    try:
        data = request.get_json(force=True)
        merchant_name = data["merchant"]
        mcc = data["mcc"]
        category = data["category"]
    except:
        return jsonify("Invalid/Missing request contents"), 400
    
    try:
        # Search for merchant of same name and mcc, if exists already, return
        merchant = Merchant.query.filter_by(merchant=merchant_name, mcc=mcc).first()
        if mcc:
            return jsonify({"message": "merchant already exists"}), 200

        # Create merchant
        merchant = Merchant(name = merchant_name, mcc = mcc, category=category)
        db.session.add(merchant)
        db.session.commit()

        return jsonify({"message": f"Merchant {merchant.name} has been created"}), 201
    except:
        return jsonify({"message": f"Servers offline"}), 500