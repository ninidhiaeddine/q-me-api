import json
import bcrypt
from models import Guest, Establishment, Branch, OTP
import dal  # import data access layer
import helpers
import sms
import random

from flask import (
    Blueprint, flash, request, session, jsonify
)


registration_bp = Blueprint('registration', __name__, url_prefix='/register')


@registration_bp.route('/guests', methods=['POST'])
def register_guest():
    """
    Expects the following JSON Object:
    {
        "name" : "your name here",
        "phone_number" : "your phone number here"
    }

    Returns the following JSON Object if operation is successful:
    {
        "status" : 200,
        "message" : "Guest Added to Database successfully!"
    }
    """

    # initially, assume that there is no error
    error = None

    if not helpers.request_is_valid(request, keys_list=['name', 'phone_number']):
        error = "Invalid JSON Object."

    if error is None:
        # map json object to class object
        guest = Guest(request.json.get('name'),
                      request.json.get('phone_number'))

        # verify input info
        is_valid_tuple = guest.is_valid()
        if is_valid_tuple[0]:
            if dal.get_guest_by_phone_number(guest.PhoneNumber) is not None:
                error = 'Guest with phone number=\'{}\' is already registered.'.format(
                    guest.PhoneNumber)
        else:
            error = is_valid_tuple[1]

        dal.add_guest(guest)

        # generate otp_code
        otp_code = random.randint(1000, 9999)
        # create sms body
        sms_body = 'Hello \'{}\'\nYour verification code is:\'{}\''.format(
            guest.Name, otp_code)
        # send OTP code through sms
        sms.send_sms(guest.PhoneNumber, sms_body)
        # post it on the db
        otp = OTP(guest.PK_Guest, otp_code)
        dal.add_otp(otp)

    else:
        return jsonify(
            status=400,
            message=error
        )


@registration_bp.route('/establishments', methods=['POST'])
def register_establishment():
    """
    Expects the following JSON Object:
    {
        "name" : "your establishment's name here",
        "type" : 0,
        "email" : "your email here",
        "password" : "your password here",
        "phone_number" : "your phone number here" /* (optional) */
    }

    Returns the following JSON Object if operation is successful:
    {
        "status" : 200,
        "message" : "Establishment Added to Database successfully!"
    }
    """

    # initially, assume that there is no error
    error = None

    if not helpers.request_is_valid(request, keys_list=['name', 'type', 'email', 'password']):
        error = "Invalid JSON Object."

    if error is None:
        # Hash password using bcrypt
        hashed = bcrypt.hashpw(request.json.get(
            'password').encode('utf-8'), bcrypt.gensalt())

        # map json object to class object
        establishment = Establishment(
            request.json.get('name'),
            request.json.get('type'),
            request.json.get('email'),
            hashed,
            request.json.get('phone_number')
        )

        # verify input info
        is_valid_tuple = establishment.is_valid()
        if is_valid_tuple[0]:
            if dal.get_establishment_by_email(establishment.Email) is not None:
                error = 'Establishment with Email=\'{}\' is already registered.'.format(
                    establishment.Email)
        else:
            error = is_valid_tuple[1]

    # add to database if everything is ok
    if error is None:
        dal.add_establishment(establishment)
        return jsonify(
            status=200,
            message="Establishment Added to Database successfully!"
        )
    else:
        return jsonify(
            status=400,
            message=error
        )