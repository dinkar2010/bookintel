from flask import Blueprint

intel = Blueprint('intel', __name__)

from app.intel import routes