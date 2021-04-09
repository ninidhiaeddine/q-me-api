import json

from flask import (
    Blueprint, flash, request, session, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from models import Guest, Establishment, Branch
import dal  # import data access layer

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register_guest', methods=['POST'])
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

    # verify expected JSON:
    if (
        'name' not in request.json or
        'phone_number' not in request.json
    ):
        error = "Invalid JSON Object."

    if error is None:
        # map json object to class object
        guest = Guest(
            request.json['name'],
            request.json['phone_number']
        )

        # verify input info
        is_valid_tuple = guest.is_valid()
        if is_valid_tuple[0]:
            if dal.get_guest_by_phone_number(guest.PhoneNumber) is not None:
                error = 'Guest with Phone Number \'{}\' is already registered.'.format(
                    guest.phone_number)
        else:
            error = is_valid_tuple[1]

    # add to database if everything is ok
    if error is None:
        dal.add_guest(guest)
        return jsonify(
            status=200,
            message="Guest Added to Database successfully!"
        )
    else:
        return jsonify(
            status=400,
            message=error
        )


@auth_bp.route('/register_establishment', methods=['POST'])
def register_establishment():
    """
    Expects the following JSON Object:
    {
        "name" : "your establishment's name here",
        "type" : 0,
        "email" : "your email here",
        "password" : "your password here"
    }

    Returns the following JSON Object if operation is successful:
    {
        "status" : 200,
        "message" : "Establishment Added to Database successfully!"
    }
    """

    # initially, assume that there is no error
    error = None

    # verify expected JSON:
    if (
        'name' not in request.json or
        'type' not in request.json or
        'email' not in request.json or
        'password' not in request.json
    ):
        error = "Invalid JSON Object."

    if error is None:
        # map json object to class object
        establishment = Establishment(
            None,
            request.json['name'],
            request.json['type'],
            request.json['email'],
            request.json['password']
        )

        # initially, assume that there is no error
        error = None

        # verify input info
        is_valid_tuple = establishment.is_valid()
        if is_valid_tuple[0]:
            if dal.get_establishment_by_name(establishment.name) is not None:
                error = 'Establishment \'{}\' is already registered.'.format(
                    establishment.name)
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


@auth_bp.route('/register_branch', methods=['POST'])
def register_branch():
    """
    Expects the following JSON Object:
    {
        "establishment_id" : your establishment name here,
        "address" : "your branch's address here"
    }

    Returns the following JSON Object if operation is successful:
    {
        "status" : 200,
        "message" : "Branch Added to Database successfully!"
    }
    """

    # initially, assume that there is no error
    error = None

    # verify expected JSON:
    if (
        'establishment_id' not in request.json or
        'address' not in request.json
    ):
        error = "Invalid JSON Object."

    if error is None:
        # map json object to class object
        branch = Branch(
            None,
            request.json['establishment_id'],
            request.json['address']
        )

        # initially, assume that there is no error
        error = None

        # verify input info
        is_valid_tuple = branch.is_valid()
        if is_valid_tuple[0]:
            if dal.get_establishment_by_id(branch.establishment_id) is None:
                error = "The specified EstablishmentId is nonexistent. It violates \'Referential Integrity\'"
        else:
            error = is_valid_tuple[1]

    # add to database if everything is ok
    if error is None:
        dal.add_branch(branch)
        return jsonify(
            status=200,
            message="Branch Added to Database successfully!"
        )
    else:
        return jsonify(
            status=400,
            message=error
        )


@auth_bp.route('/login_guest', methods=['POST'])
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
    if (
        'name' not in request.json or
        'phone_number' not in request.json
    ):
        error = "Invalid JSON Object."

    if error is None:
        # map json object to class object
        guest = Guest(
            None,
            request.json['name'],
            request.json['phone_number']
        )

        # initially, assume that there is no error
        error = None

        # verify input info
        is_valid_tuple = guest.is_valid()
        if is_valid_tuple[0]:
            guest_record = dal.get_guest_by_phone_number(guest.phone_number)
            if guest_record is None or guest_record.name != guest.name:
                error = 'Incorrect Guest\'s Credentials.'
        else:
            error = is_valid_tuple[1]

    # start new session if everything is ok
    if error is None:
        session.clear()
        session['guest_id'] = guest_record.id
        return jsonify(
            status=200,
            message="Guest logged in Successfully!"
        )
    else:
        return jsonify(
            status=400,
            message=error
        )


@auth_bp.route('/login_establishment', methods=['POST'])
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

    # verify expected JSON:
    if (
        'email' not in request.json or
        'password' not in request.json
    ):
        error = "Invalid JSON Object."

    if error is None:
        # map json object to class object
        establishment = Establishment(
            None,
            "N/A",
            0,
            request.json['email'],
            request.json['password']
        )

        # initially, assume that there is no error
        error = None

        # verify input info
        is_valid_tuple = establishment.is_valid()
        if is_valid_tuple[0]:
            establishment_record = dal.get_establishment_by_email(
                establishment.email)
            if (
                establishment_record is None or
                check_password_hash(
                    establishment_record.password, establishment.password) == False
            ):
                error = 'Incorrect Establishment\'s Credentials.'
        else:
            error = is_valid_tuple[1]

    # start new session if evertthing is ok
    if error is None:
        session.clear()
        session['establishment_id'] = establishment_record.id
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
