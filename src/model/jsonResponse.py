from flask import jsonify


class JsonResponse:
    def __init__(self, data, responseCode):
        self.data = data
        self.responseCode = responseCode

    def send_response(self):
        return jsonify({"data": self.data}), self.responseCode
