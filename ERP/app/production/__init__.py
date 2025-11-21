from flask import Blueprint

production = Blueprint('production', __name__)

from app.production import routes