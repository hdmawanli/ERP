from flask import Blueprint

bank = Blueprint('bank', __name__)

from app.bank import routes