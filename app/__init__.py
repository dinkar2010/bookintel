from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

book_intel_db = SQLAlchemy()

app = Flask(__name__)

app.config.from_object(Config)
book_intel_db.init_app(app)

from app.intel import intel
app.register_blueprint(intel)