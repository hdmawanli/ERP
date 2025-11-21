from flask import Blueprint

master_data = Blueprint('master_data', __name__, url_prefix='/master-data')

from app.master_data import routes