from flask import Blueprint

opening = Blueprint('opening', __name__)

from app.opening import routes