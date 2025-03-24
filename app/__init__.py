from flask import Flask
from pymongo import MongoClient
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)

client = MongoClient(app.config['MONGO_URI'])
db = client.get_database()

from app.routes import api, frontend

app.register_blueprint(api.api_bp, url_prefix='/api')
app.register_blueprint(frontend.frontend_bp)
