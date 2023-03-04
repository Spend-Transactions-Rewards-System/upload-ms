from flask import Flask
from src.view.upload import upload
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.register_blueprint(upload, url_prefix="/api/v1/upload")
