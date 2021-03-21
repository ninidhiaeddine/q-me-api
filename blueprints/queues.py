import json

from flask import (
    Blueprint, flash, request, session, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
# from models import Queue
import dal  # import data access layer

queues_bp = Blueprint('queues', __name__, url_prefix='/queues')

# TODO: Finish blueprint design:
