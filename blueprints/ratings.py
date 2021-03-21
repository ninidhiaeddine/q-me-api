import json

from flask import (
    Blueprint, flash, request, session, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
# from models import Rating
import dal  # import data access layer

ratings_bp = Blueprint('ratings', __name__, url_prefix='/ratings')

# TODO: Finish blueprint design:
