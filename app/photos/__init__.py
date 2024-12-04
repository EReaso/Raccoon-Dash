from flask import Blueprint

bp = Blueprint("photos", __name__)
from app.photos import routes
