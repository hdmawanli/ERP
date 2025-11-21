from flask import Blueprint

arap = Blueprint('arap', __name__)

from app.arap import routes