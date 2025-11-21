from flask import Blueprint

quality_control = Blueprint('quality_control', __name__)

from app.quality_control import routes