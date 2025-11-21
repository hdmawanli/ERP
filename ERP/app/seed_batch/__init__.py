from flask import Blueprint

seed_batch = Blueprint('seed_batch', __name__)

from app.seed_batch import routes