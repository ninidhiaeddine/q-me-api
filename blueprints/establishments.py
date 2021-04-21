import json

from flask import (
    Blueprint, flash, request, session, jsonify, after_this_request
)
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

import bcrypt
from models import Establishment
import dal  # import data access layer
import helpers

establishments_bp = Blueprint(
    'establishments_bp', __name__, url_prefix='/establishments')


# GET:

@establishments_bp.route('', methods=['GET'])
@jwt_required()
def get_establishments():
    """
    Does not expect any JSON object.

    Returns the following JSON Object if operation is successful:
    {
        "status" : 200,
        "message" : establishments_list
    }
    """
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

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
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

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
# Moved to register.py

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
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

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
            # TODO Fix DB Password Hashing Problem
            # generate_password_hash(request.json.get('password'))
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
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

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
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

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
