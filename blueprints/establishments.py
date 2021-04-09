import json

from flask import (
    Blueprint, flash, request, session, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from models import Establishment
import dal  # import data access layer
import helpers

establishments_bp = Blueprint(
    'establishments_bp', __name__, url_prefix='/establishments')


# GET:

@establishments_bp.route('', methods=['GET'])
def get_establishments():
    """
    Does not expect any JSON object.

    Returns the following JSON Object if operation is successful:
    {
        "status" : 200,
        "message" : establishments_list
    }
    """
    establishments_list = dal.get_establishments()
    if len(establishments_list) > 0:
        return jsonify(
            status=200,
            message=[establishment.serialize()
                     for establishment in establishments_list]
        )
    else:
        return jsonify(
            status=404,
            message="List of Establishments is empty!"
        )


@establishments_bp.route('/<int:id>', methods=['GET'])
def get_establishment_by_id(id):
    """
    Does not expect any JSON object.

    Returns the following JSON Object if operation is successful:
    {
        "status" : 200,
        "message" : establishment_with_id
    }
    """
    establishment_with_id = dal.get_establishment_by_id(id)
    if establishment_with_id is not None:
        return jsonify(
            status=200,
            message=establishment_with_id.serialize()
        )
    else:
        return jsonify(
            status=404,
            message="Establishment with ID={} not found!".format(id)
        )


# POST:

@establishments_bp.route('', methods=['POST'])
def add_establishment():
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

    # verify expected JSON:
    if not helpers.request_is_valid(request, keys_list=['name', 'type', 'email', 'password']):
        error = "Invalid JSON Object."

    if error is None:
        # map json object to class object
        establishment = Establishment(
            request.json.get('name'),
            request.json.get('type'),
            request.json.get('email'),
            request.json.get('password'),
            request.json.get('phone_number')
        )

        # verify input info
        is_valid_tuple = establishment.is_valid()
        if is_valid_tuple[0]:
            if dal.get_establishment_by_name(establishment.Name) is not None:
                error = 'Establishment \'{}\' is already registered.'.format(
                    establishment.Name)
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

# PUT:


@establishments_bp.route('/<int:id>', methods=['PUT'])
def update_establishment_by_id(id):
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
        "message" : "Establishment Updated Successfully!"
    }
    """

    # initially, assume that there is no error
    error = None

    # verify expected JSON:
    if not helpers.request_is_valid(request, keys_list=['name', 'type', 'email', 'password']):
        error = "Invalid JSON Object."

    if error is None:
        # map json object to class object
        establishment = Establishment(
            request.json.get('name'),
            request.json.get('type'),
            request.json.get('email'),
            request.json.get('password'),
            request.json.get('phone_number')
        )

        # initially, assume that there is no error
        error = None

        # verify input info
        is_valid_tuple = establishment.is_valid()
        if not is_valid_tuple[0]:
            error = is_valid_tuple[1]

     # update database if everything is ok
    if error is None:
        found = dal.update_establishment_by_id(id, establishment)
        if found:
            return jsonify(
                status=200,
                message="Establishment Updated Successfully!"
            )
        else:
            return jsonify(
                status=404,
                message="Establishment with ID={} not found. No changes occured!".format(
                    id)
            )
    else:
        return jsonify(
            status=400,
            message=error
        )


# DELETE:

@establishments_bp.route('', methods=['DELETE'])
def delete_establishments():
    """
    Does not expect any JSON object.

    Returns the following JSON Object if operation is successful:
    {
        "status" : 200, 
        "message" : "All establishments have been deleted successfully!"
    }
    """
    dal.delete_establishments()
    return jsonify(
        status=200,
        message="All establishments have been deleted successfully!"
    )


@establishments_bp.route('/<int:id>', methods=['DELETE'])
def delete_establishment_by_id(id):
    """
    Does not expect any JSON object.

    Returns the following JSON Object if operation is successful:
    {
        "status" : 200, 
        "message" : "All Establishments have been deleted successfully!"
    }
    """
    found = dal.delete_establishment_by_id(id)
    if found:
        return jsonify(
            status=200,
            message="Establishment with ID={} has been deleted successfully!".format(
                id)
        )
    else:
        return jsonify(
            status=404,
            message="Establishment with ID={} not found. No changes occured!".format(
                id)
        )
