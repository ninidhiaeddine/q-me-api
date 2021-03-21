import json

from flask import (
    Blueprint, flash, request, session, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
# from models import OperatingHours
import dal  # import data access layer

operating_hours_bp = Blueprint(
    'operating_hours', __name__, url_prefix='/operating_hours')

# TODO: Finish blueprint design:
