from flask import Flask
from src.view.upload import upload
from src.view.download import download
from src.view.healthcheck import healthcheck
from src.model.jsonResponse import JsonResponse
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route("/", methods=(["GET"]))
def app_healthcheck():
    return JsonResponse("Healthy", 200).send_response()

app.register_blueprint(upload, url_prefix="/api/v1/upload")
app.register_blueprint(download, url_prefix="/api/v1/download")
app.register_blueprint(healthcheck, url_prefix="/api/v1")