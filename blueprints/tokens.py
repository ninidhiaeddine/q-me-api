import json

from flask import (
    Blueprint, flash, request, session, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from models import Token
import dal  # import data access layer
import helpers

tokens_bp = Blueprint('tokens', __name__, url_prefix='/establishments')


# GET:

@tokens_bp.route('/<int:establishment_id>/branches/<int:branch_id>/queues/<int:queue_id>/tokens', methods=['GET'])
def get_tokens(establishment_id, branch_id, queue_id):
    """
    Does not expect any JSON object.

    Returns the following JSON Object if operation is successful:
    {
        "status" : 200,
        "message" : tokens_list
    }
    """
    tokens_list = dal.get_tokens(queue_id)
    if len(tokens_list) > 0:
        return jsonify(
            status=200,
            message=[token.serialize() for token in tokens_list]
        )
    else:
        return jsonify(
            status=404,
            message="List of Tokens is empty!"
        )


@tokens_bp.route('/<int:establishment_id>/branches/<int:branch_id>/queues/<int:queue_id>/tokens/<int:token_id>', methods=['GET'])
def get_token_by_id(establishment_id, branch_id, queue_id, token_id):
    """
    Does not expect any JSON object.

    Returns the following JSON Object if operation is successful:
    {
        "status" : 200, 
        "message" : token_with_id
    }
    """
    token_with_id = dal.get_token_by_id(token_id)
    if token_with_id is not None:
        return jsonify(
            status=200,
            message=token_with_id.serialize()
        )
    else:
        return jsonify(
            status=404,
            message="Token with ID={} not found!".format(id)
        )


# POST:

@tokens_bp.route('/<int:establishment_id>/branches/<int:branch_id>/queues/<int:queue_id>/tokens', methods=['POST'])
def add_token(establishment_id, branch_id, queue_id):
    """
    Expects the following JSON Object:
    {
        "guest_id": int: Guest_id,
        "Status": int,
        "DateAndTime":"",
        "PositionInLine": int
    }

    '''Status:
    0 : waiting (default)
    1 : Being serviced
    -1 : done
    every other value returns an error  
    '''

    Returns the following JSON Object if operation is successful:
    {
        "status" : 200,
        "message" : "Token Added to Database successfully!"
    }
    """

    # initially, assume that there is no error
    error = None

    # verify expected JSON:
    if not helpers.request_is_valid(request, keys_list=["guest_id", "Status", "PositionInLine"]):
        error = "Invalid JSON Object."

    if error is None:
        # map json object to class object
        token = Token(
            request.json.get('guest_id'),
            queue_id,
            request.json.get('Status'),
            request.json.get('DateAndTime'),
            request.json.get('PositionInLine'),
        )

        # verify input info
        is_valid_tuple = token.is_valid()
        if is_valid_tuple[0]:
            # Verify Referential Integrity
            if dal.get_queue_by_id(queue_id) is None:
                error = 'Queue with ID={} does not exist. Impossible to add this token.'.format(
                    queue_id)
        else:
            error = is_valid_tuple[1]

    # add to database if everything is ok
    if error is None:
        dal.add_token(token)
        return jsonify(
            status=200,
            message="Token Added to Database successfully!"
        )
    else:
        return jsonify(
            status=400,
            message=error
        )


#PUT

@tokens_bp.route('/<int:establishment_id>/branches/<int:branch_id>/queues/<int:queue_id>/tokens/<int:token_id>', methods=['PUT'])
def update_token_by_id(establishment_id, branch_id, queue_id, token_id):

    """
    {
        "guest_id": int: Guest_id,
        "Status": int,
        "DateAndTime":"Date and time",
        "PositionInLine": int
    }

    Returns the following JSON Object if operation is successful:
    {
        "status" : 200,
        "message" : "Token Updated Successfully!"
    }
    """

    # initially, assume that there is no error
    error = None

    # verify expected JSON:
    if not helpers.request_is_valid(request, keys_list=["guest_id", "Status", "PositionInLine"]):
        error = "Invalid JSON Object."

    if error is None:
        # map json object to class object
        token = Token(
            request.json.get('guest_id'),
            queue_id,
            request.json.get('Status'),
            request.json.get('DateAndTime'),
            request.json.get('PositionInLine'),
        )

        # verify input info
        is_valid_tuple = token.is_valid()
        if not is_valid_tuple[0]:
            error = is_valid_tuple[1]

    # update database if everything is ok
    if error is None:
        found = dal.update_token_by_id(establishment_id, branch_id, token_id, token)
        if found:
            return jsonify(
                status=200,
                message="Token Updated Successfully!"
            )
        else:
            return jsonify(
                status=404,
                message="Token with ID={} not found. No changes occured!".format(
                    id)
            )
    else:
        return jsonify(
            status=400,
            message=error
        )


# DELETE:

@tokens_bp.route('/<int:establishment_id>/branches/<int:branch_id>/queues/<int:queue_id>/tokens', methods=['DELETE'])
def delete_tokens(establishment_id, branch_id, queue_id):
    """
    Does not expect any JSON object.

    Returns the following JSON Object if operation is successful:
    {
        "status" : 200, 
        "message" : "All tokens have been deleted successfully!"
    }
    """
    dal.delete_tokens(queue_id)
    return jsonify(
        status=200,
        message="All tokens with Queue id={} have been deleted successfully!".format(
            queue_id)
    )



@tokens_bp.route('/<int:establishment_id>/tokens/<int:branch_id>/queues/<int:queue_id>/tokens/<int:token_id>', methods=['DELETE'])
def delete_token_by_id(establishment_id, branch_id, queue_id, token_id):
    """
    Does not expect any JSON object.

    Returns the following JSON Object if operation is successful:
    {
        "status" : 200, 
        "message" : "Token with Id={} have been deleted successfully!"
    }
    """
    found = dal.delete_token_by_id(token_id)
    if found:
        return jsonify(
            status=200,
            message="Token with ID={} has been deleted successfully!".format(
                token_id)
        )
    else:
        return jsonify(
            status=404,
            message="Token with ID={} not found. No changes occured!".format(
                token_id)
        )


