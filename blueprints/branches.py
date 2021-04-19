import json

from flask import (
    Blueprint, flash, request, session, jsonify
)
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

from models import Branch
import dal  # import data access layer
import helpers
import bcrypt
import custom_decorator

branches_bp = Blueprint('branches', __name__, url_prefix='/establishments')


# GET:

@branches_bp.route('/<int:establishment_id>/branches', methods=['GET'])
@custom_decorator.establishment_required()
def get_branches(establishment_id):
    """
    Does not expect any JSON object.

    Returns the following JSON Object if operation is successful:
    {
        "status" : 200,
        "message" : branches_list
    }
    """
    branches_list = dal.get_branches(establishment_id)
    if len(branches_list) > 0:
        return jsonify(
            status=200,
            message=[branch.serialize() for branch in branches_list]
        )
    else:
        return jsonify(
            status=404,
            message="List of Branches is empty!"
        )


@branches_bp.route('/<int:establishment_id>/branches/<int:branch_id>', methods=['GET'])
def get_branch_by_id(establishment_id, branch_id):
    """
    Does not expect any JSON object.

    Returns the following JSON Object if operation is successful:
    {
        "status" : 200, 
        "message" : branch_with_id
    }
    """
    branch_with_id = dal.get_branch_by_id(establishment_id, branch_id)
    if branch_with_id is not None:
        return jsonify(
            status=200,
            message=branch_with_id.serialize()
        )
    else:
        return jsonify(
            status=404,
            message="Branch with ID={} not found!".format(id)
        )


# POST:

@branches_bp.route('/<int:establishment_id>/branches', methods=['POST'])
# @custom_decorator.establishment_required()
def add_branch(establishment_id):
    """
    Expects the following JSON Object:
    {
        "address" : "your address here",
        "email" : "your email here",
        "password" : "your password here",
        "phone_number" : "your phone number here" /* (optional) */,
        "latitude" : "your latitude here" /* (optional) */,
        "longitude" : "your lonitude here" /* (optional) */
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
    if not helpers.request_is_valid(request, keys_list=['address', 'email', 'password']):
        error = "Invalid JSON Object."

    password = bcrypt.hashpw(request.json.get(
        'password').encode('utf-8'), bcrypt.gensalt())

    if error is None:
        # map json object to class object
        branch = Branch(
            establishment_id,
            request.json.get('address'),
            request.json.get('email'),
            password,
            request.json.get('phone_number'),
            request.json.get('latitude'),
            request.json.get('longitude')
        )

        # verify input info
        is_valid_tuple = branch.is_valid()
        if is_valid_tuple[0]:
            # Verify Referential Integrity
            if dal.get_establishment_by_id(establishment_id) is None:
                error = 'Establishment with ID={} does not exist. Impossible to add this branch.'.format(
                    establishment_id)
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


# PUT:

@branches_bp.route('/<int:establishment_id>/branches/<int:branch_id>', methods=['PUT'])
def update_branch_by_id(establishment_id, branch_id):
    # TODO: Fix FK_Establishment dependency
    """
    {
        "address" : "your address here",
        "email" : "your email here",
        "password" : "your password here",
        "phone_number" : "your phone number here" /* (optional) */,
        "latitude" : "your latitude here" /* (optional) */,
        "longitude" : "your lonitude here" /* (optional) */
    }

    Returns the following JSON Object if operation is successful:
    {
        "status" : 200,
        "message" : "Branch Updated Successfully!"
    }
    """

    # initially, assume that there is no error
    error = None

    # verify expected JSON:
    if not helpers.request_is_valid(request, keys_list=['address', 'email', 'password']):
        error = "Invalid JSON Object."

    if error is None:
        # map json object to class object
        branch = Branch(
            establishment_id,
            request.json.get('address'),
            request.json.get('email'),
            request.json.get('password'),
            request.json.get('phone_number'),
            request.json.get('latitude'),
            request.json.get('longitude')
        )

        # verify input info
        is_valid_tuple = branch.is_valid()
        if not is_valid_tuple[0]:
            error = is_valid_tuple[1]

    # update database if everything is ok
    if error is None:
        found = dal.update_branch_by_id(establishment_id, branch_id, branch)
        if found:
            return jsonify(
                status=200,
                message="Branch Updated Successfully!"
            )
        else:
            return jsonify(
                status=404,
                message="Branch with ID={} not found. No changes occured!".format(
                    id)
            )
    else:
        return jsonify(
            status=400,
            message=error
        )


# DELETE:

@branches_bp.route('/<int:establishment_id>/branches', methods=['DELETE'])
def delete_branches(establishment_id):
    """
    Does not expect any JSON object.

    Returns the following JSON Object if operation is successful:
    {
        "status" : 200, 
        "message" : "All branches have been deleted successfully!"
    }
    """
    dal.delete_branches(establishment_id)
    return jsonify(
        status=200,
        message="All branches with EstablishmentId={} have been deleted successfully!".format(
            establishment_id)
    )


@branches_bp.route('/<int:establishment_id>/branches/<int:branch_id>', methods=['DELETE'])
def delete_branch_by_id(establishment_id, branch_id):
    # TODO: Fix FK_Establishment dependency
    """
    Does not expect any JSON object.

    Returns the following JSON Object if operation is successful:
    {
        "status" : 200, 
        "message" : "Branch with Id={} have been deleted successfully!"
    }
    """
    found = dal.delete_branch_by_id(establishment_id, branch_id)
    if found:
        return jsonify(
            status=200,
            message="Branch with ID={} has been deleted successfully!".format(
                branch_id)
        )
    else:
        return jsonify(
            status=404,
            message="Branch with ID={} not found. No changes occured!".format(
                branch_id)
        )
