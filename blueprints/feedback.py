import json

from flask import (
    Blueprint, flash, request, session, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
# from models import Feedback
import dal  # import data access layer

feedback_bp = Blueprint('feedback', __name__, url_prefix='/feedback')

# TODO: Finish blueprint design:
