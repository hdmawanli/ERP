from flask import Blueprint

assembly = Blueprint('assembly', __name__)

from app.assembly import routes