import json

from flask import (
    Blueprint, flash, request, session, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from models import Guest
import dal  # import data access layer
import helpers

guests_bp = Blueprint('guests', __name__, url_prefix='/guests')


# GET:

@guests_bp.route('', methods=['GET'])
def get_guests():
    """
    Does not expect any JSON object.

    Returns the following JSON Object if operation is successful:
    {
        "status" : 200,
        "message" : guests_list
    }
    """
    guests_list = dal.get_guests()
    if len(guests_list) > 0:
        return jsonify(
            status=200,
            message=[guest.serialize() for guest in guests_list]
        )
    else:
        return jsonify(
            status=404,
            message="List of Guests is empty!"
        )


@guests_bp.route('/<int:id>', methods=['GET'])
def get_guest_by_id(id):
    """
    Does not expect any JSON object.

    Returns the following JSON Object if operation is successful:
    {
        "status" : 200, 
        "message" : guest_with_id
    }
    """
    guest_with_id = dal.get_guest_by_id(id)
    if guest_with_id is not None:
        return jsonify(
            status=200,
            message=guest_with_id.serialize()
        )
    else:
        return jsonify(
            status=404,
            message="Guest with ID={} not found!".format(id)
        )


# POST:

@guests_bp.route('', methods=['POST'])
def add_guest():
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


# PUT:

@guests_bp.route('/<int:id>', methods=['PUT'])
def update_guest_by_id(id):
    """
    Expects the following JSON Object:
    {
        "name" : "your name here",
        "phone_number" : "your phone number here"
    }

    Returns the following JSON Object if operation is successful:
    {
        "status" : 200,
        "message" : "Guest Updated Successfully!"
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
        if not is_valid_tuple[0]:
            error = is_valid_tuple[1]

    # update database if everything is ok
    if error is None:
        found = dal.update_guest_by_id(id, guest)
        if found:
            return jsonify(
                status=200,
                message="Guest Updated Successfully!"
            )
        else:
            return jsonify(
                status=404,
                message="Guest with ID={} not found. No changes occured!".format(
                    id)
            )
    else:
        return jsonify(
            status=400,
            message=error
        )


# DELETE:

@guests_bp.route('', methods=['DELETE'])
def delete_guests():
    """
    Does not expect any JSON object.

    Returns the following JSON Object if operation is successful:
    {
        "status" : 200, 
        "message" : "All guests have been deleted successfully!"
    }
    """
    dal.delete_guests()
    return jsonify(
        status=200,
        message="All guests have been deleted successfully!"
    )


@guests_bp.route('/<int:id>', methods=['DELETE'])
def delete_guest_by_id(id):
    """
    Does not expect any JSON object.

    Returns the following JSON Object if operation is successful:
    {
        "status" : 200, 
        "message" : "All guests have been deleted successfully!"
    }
    """
    found = dal.delete_guest_by_id(id)
    if found:
        return jsonify(
            status=200,
            message="Guest with ID={} has been deleted successfully!".format(
                id)
        )
    else:
        return jsonify(
            status=404,
            message="Guest with ID={} not found. No changes occured!".format(
                id)
        )
