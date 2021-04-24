import json

from flask import (
    Blueprint, flash, request, session, jsonify, after_this_request
)

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

import bcrypt
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
        "message" : {
            "content": "Guest logged in successfully!",
            "guest_id": (int),
            "access_token": "access_token"
        }
    }
    """
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

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

            if guest_record is None:
                error = 'Guest not registered. Please register before logging in.'
            elif guest_record.Name != guest.Name:
                error = 'Incorrect Guest\'s Credentials.'
        else:
            error = is_valid_tuple[1]

    # start new session if everything is ok
    if error is None:
        session.clear()
        session['guest_id'] = guest_record.PK_Guest
        access_token = create_access_token(
            identity={'phone_number': guest.PhoneNumber}, additional_claims={"is_guest": True})

        return jsonify(
            status=200,
            message={
                "content": "Guest logged in Successfully!",
                "guest_id": guest_record.PK_Guest,
                "access_token": access_token
            }

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
        "message" : {
            "content": "Establishment logged in successfully!",
            "establishment_id": (int),
            "access_token": "access_token"
        }
    }
    """
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    # initially, assume that there is no error
    error = None

    if not helpers.request_is_valid(request, keys_list=['email', 'password']):
        error = "Invalid JSON Object."

    if error is None:
        # map json object to class object
        establishment = Establishment(
            'N/A',
            0,
            request.json.get('email'),
            request.json.get('password'),
            '+'
        )

        # verify input info
        is_valid_tuple = establishment.is_valid()
        if is_valid_tuple[0]:
            establishment_record = dal.get_establishment_by_email(
                establishment.Email)

            if establishment_record is None:
                error = "Establishment not registered. Please register before logging in"
            elif not bcrypt.checkpw(establishment.Password.encode('utf-8'), establishment_record.Password.encode('utf-8')):
                error = 'Incorrect Establishment\'s Credentials.'
        else:
            error = is_valid_tuple[1]

    if error is None:
        session.clear()
        session['establishment_id'] = establishment_record.PK_Establishment
        access_token = create_access_token(
            identity={'email': establishment_record.Email}, additional_claims={"is_establishment": True})

        return jsonify(status=200,
                       message={
                           "content": "Establishment successfully logged in!",
                           "establishment_id": establishment_record.PK_Establishment,
                           "access_token": access_token
                       })
    else:
        return jsonify(
            status=400,
            message=error
        )


@auth_bp.route('/branches', methods=['POST'])
def login_branch():
    """
    Expects the following JSON Object:
    {
        "email" : "your branch email here",
        "password" : "your branch password here"
    }

    Returns the following JSON Object if operation is successful:
    {
        "status" : 200,
        "message" : {
            "content" : "Branch logged in successfully!",
            "branch_id": (int),
            "access_token": "access_token"
        }
    }
    """
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    # initially, assume that there is no error
    error = None

    if not helpers.request_is_valid(request, keys_list=['email', 'password']):
        error = "Invalid JSON Object."

    if error is None:
        # map json object to class object
        branch = Branch(
            -1,
            "N/A",
            request.json.get('email'),
            request.json.get('password')
        )

        # verify input info
        is_valid_tuple = branch.is_valid()
        if is_valid_tuple[0]:
            branch_record = dal.get_branch_by_email(branch.Email)

            if branch_record is None:
                error = "Branch not registered. Please add branch from your establishment before logging in"
            elif not bcrypt.checkpw(branch.Password.encode('utf-8'), branch_record.Password.encode('utf-8')):
                error = 'Incorrect Branch\'s Credentials.'
        else:
            error = is_valid_tuple[1]

    # start new session if everything is ok
    if error is None:
        session.clear()
        session['branch_id'] = branch_record.PK_Branch
        access_token = create_access_token(
            identity={'email': branch_record.Email}, additional_claims={"is_branch": True})

        return jsonify(
            status=200,
            message={
                "content": "Branch logged in Successfully!",
                "branch_id": branch_record.PK_Branch,
                "access_token": access_token
            })
    else:
        return jsonify(
            status=400,
            message=error
        )


@auth_bp.route('/logout', methods=['GET'])
def logout():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    session.clear()
    return jsonify(
        status=200,
        message="Logged out successfully!"
    )
