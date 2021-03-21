import json

from flask import (
    Blueprint, flash, request, session, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
# from models import ContactMessage
import dal  # import data access layer

contact_messages_bp = Blueprint(
    'contact_messages', __name__, url_prefix='/contact_messages')

# TODO: Finish blueprint design:
