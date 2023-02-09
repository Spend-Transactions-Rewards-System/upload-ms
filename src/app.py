from flask import Flask
from src.utils.db import db
from src.view.rewards import rewards
from dotenv import load_dotenv


app = Flask(__name__)

# db.init_app(app)
load_dotenv()

app.register_blueprint(rewards, url_prefix="/rewards")
