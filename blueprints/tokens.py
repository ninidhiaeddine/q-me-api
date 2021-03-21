import json

from flask import (
    Blueprint, flash, request, session, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
# from models import Token
import dal  # import data access layer

tokens_bp = Blueprint('tokens', __name__, url_prefix='/tokens')

# TODO: Finish blueprint design:
