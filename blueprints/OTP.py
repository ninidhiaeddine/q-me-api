import json
from flask import (
    Blueprint, flash, request, session, jsonify, after_this_request)
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity,
)

import json
import bcrypt
from models import Guest, OTP
import dal  # import data access layer
import helpers
import sms
import random


otp_bp = Blueprint('otp', __name__, url_prefix='/otp')


@otp_bp.route('', methods=['POST'])
def add_otp():
    """
    expects a JSON object"
    {
        "guest_id": "id of guest trying to enter the OTP"
        "otp": "The OTP code"
    }
    """
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    error = None
    # verify JSON
    if not helpers.request_is_valid(request, keys_list=['guest_id', 'otp']):
        error = "Invalid JSON Object."

    if error is None:
        # hash otp
        # hashed_otp_value = bcrypt.hashpw(request.json.get(
        #     'otp').encode('utf-8'), bcrypt.gensalt())
        unhashed_otp_value = request.json.get('otp')

        # map json object to class object
        otp = OTP(
            request.json.get('guest_id'),
            unhashed_otp_value
        )

        # add to db:
        dal.add_otp(otp)

        return jsonify(status=200,
                       message="OTP added sucessfully")
    else:
        return jsonify(status=400,
                       message=error)


@otp_bp.route('/check', methods=['POST'])
def check_otp():
    """
    Expects the follwoing JSON obj:
    {
        "guest_id": "id of guest trying to enter the OTP"
        "otp": "The OTP code input by the guest i.e the OTP we want to verify"
    }
    and returns a boolean if otp codes match
    """
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    result = False
    guest_id = request.json.get("guest_id")
    otp = request.json.get("otp")

    guest = dal.get_guest_by_id(guest_id)

    if dal.check_otp_dal(guest_id, otp):
        result = True
        session.clear()
        session['guest_id'] = guest.PK_Guest

        access_token = create_access_token(
            identity={'phone_number': guest.PhoneNumber}, additional_claims={"is_guest": True})
        return jsonify(message="OTP checked and guest logged in",
                       status=200)
    else:
        return jsonify(result=result,
                       message="Invalid OTP!",
                       status=401)
