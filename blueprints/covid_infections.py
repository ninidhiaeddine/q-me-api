import json

from flask import (
    Blueprint, flash, request, session, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
# from models import CovidInfection
import dal  # import data access layer

covid_infections_bp = Blueprint(
    'covid_infections', __name__, url_prefix='/covid_infections')

# TODO: Finish blueprint design:
