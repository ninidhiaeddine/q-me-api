import json

from flask import (
    Blueprint, flash, request, session, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from models import Guest, Establishment, Branch
import dal  # import data access layer
import helpers

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/guests', methods=['POST'])
def login_guest():
    """
    Expects the following JSON Object:
    {
        "name" : "your name here",
        "phone_number" : "your phone number here"
    }

    Returns the following JSON Object if operation is successful:
    {
        "status" : 200,
        "message" : "Guest logged in successfully!"
    }
    """

    # initially, assume that there is no error
    error = None

    # verify expected JSON:
    if not helpers.request_is_valid(request, keys_list=['name', 'phone_number']):
        error = "Invalid JSON Object."

    if error is None:
        # map json object to class object
        guest = Guest(
            request.json.get('name'),
            request.json.get('phone_number')
        )

        # verify input info
        is_valid_tuple = guest.is_valid()
        if is_valid_tuple[0]:
            guest_record = dal.get_guest_by_phone_number(guest.PhoneNumber)
            if guest_record is None or guest_record.Name != guest.Name:
                error = 'Incorrect Guest\'s Credentials.'
        else:
            error = is_valid_tuple[1]

    # start new session if everything is ok
    if error is None:
        session.clear()
        session['guest_id'] = guest_record.PK_Guest
        return jsonify(
            status=200,
            message="Guest logged in Successfully!"
        )
    else:
        return jsonify(
            status=400,
            message=error
        )


@auth_bp.route('/establishments', methods=['POST'])
def login_establishment():
    """
    Expects the following JSON Object:
    {
        "email" : "your email here",
        "password" : "your password here"
    }

    Returns the following JSON Object if operation is successful:
    {
        "status" : 200,
        "message" : "Establishment logged in successfully!"
    }
    """

    # initially, assume that there is no error
    error = None

    if not helpers.request_is_valid(request, keys_list=['email', 'password']):
        error = "Invalid JSON Object."

    if error is None:
        # map json object to class object
        establishment = Establishment(
            "N/A",
            0,
            request.json.get('email'),
            request.json.get('password'),
            None
        )

        # verify input info
        is_valid_tuple = establishment.is_valid()
        if is_valid_tuple[0]:
            establishment_record = dal.get_establishment_by_email(
                establishment.Email)
            if (
                establishment_record is None or
                # TODO Fix DB Password Hashing Problem
                # check_password_hash(
                #    establishment_record.Password, establishment.Password) == False
                establishment_record.Password != establishment.Password
            ):
                error = 'Incorrect Establishment\'s Credentials.'
        else:
            error = is_valid_tuple[1]

    # start new session if evertthing is ok
    if error is None:
        session.clear()
        session['establishment_id'] = establishment_record.PK_Establishment
        return jsonify(
            status=200,
            message="Establishment logged in successfully!"
        )
    else:
        return jsonify(
            status=400,
            message=error
        )


@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return jsonify(
        status=200,
        message="Logged out successfully!"
    )
