import json

from flask import (
    Blueprint, flash, request, session, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from models import Queue
import dal  # import data access layer
import qr   # import qr code generator
import helpers

queues_bp = Blueprint('queues', __name__, url_prefix='/establishments')


# GET:

@queues_bp.route('/<int:establishment_id>/branches/<int:branch_id>/queues', methods=['GET'])
def get_queues(establishment_id, branch_id):
    """
    Does not expect any JSON object.

    Returns the following JSON Object if operation is successful:
    {
        "status" : 200,
        "message" : queues_list
    }
    """
    queues_list = dal.get_queues(branch_id)
    if len(queues_list) > 0:
        return jsonify(
            status=200,
            message=[queue.serialize() for queue in queues_list]
        )
    else:
        return jsonify(
            status=404,
            message="List of queues for branch with the ID = {} under Establishment ID = {} is empty!".format(
                branch_id, establishment_id)
        )


@queues_bp.route('/<int:establishment_id>/branches/<int:branch_id>/queues/<int:queue_id>', methods=['GET'])
def get_queue_by_id(establishment_id, branch_id, queue_id):
    """
    Does not expect any JSON object.

    Returns the following JSON Object if operation is successful:
    {
        "status" : 200, 
        "message" : branch_with_id
    }
    """
    queue_with_id = dal.get_queue_by_id(queue_id)
    if queue_with_id is not None:
        return jsonify(
            status=200,
            message=queue_with_id.serialize()
        )
    else:
        return jsonify(
            status=404,
            message="Queue with ID={} not found!".format(queue_id)
        )


# POST:

@queues_bp.route('/<int:establishment_id>/branches/<int:branch_id>/queues', methods=['POST'])
def add_queue(establishment_id, branch_id):
    """
    Expects the following JSON Object:
    {
        "name" : "the name of the queue (the service)",
        "approximate_time_of_service" : "the approximate time of service"
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
    if not helpers.request_is_valid(request, keys_list=['name', 'approximate_time_of_service']):
        error = "Invalid JSON Object."

    if error is None:
        # map json object to class object
        queue = Queue(
            branch_id,
            request.json.get('name'),
            request.json.get('approximate_time_of_service'),
        )

        # verify input info
        is_valid_tuple = queue.is_valid()
        if is_valid_tuple[0]:
            # Verify Referential Integrity
            if dal.get_branch_by_id(establishment_id, branch_id) is None:
                error = 'Branch with ID={} does not exist. Impossible to add this queue.'.format(
                    branch_id)
        else:
            error = is_valid_tuple[1]

    # add to database if everything is ok
    if error is None:
        dal.add_queue(queue)
        return jsonify(
            status=200,
            message="Queue Added to Database successfully!"
        )
    else:
        return jsonify(
            status=400,
            message=error
        )


# #PUT:

@queues_bp.route('/<int:establishment_id>/branches/<int:branch_id>/queues/<int:queue_id>', methods=['PUT'])
def update_queue_by_id(establishment_id, branch_id, queue_id):
    """
    {
        "name" : "the name of the queue (the service)",
        "approximate_time_of_service" : "the approximate time of service"
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
    if not helpers.request_is_valid(request, keys_list=["name", "approximate_time_of_service"]):
        error = "Invalid JSON Object."

    if error is None:
        # map json object to class object
        queue = Queue(
            branch_id,
            request.json.get('name'),
            request.json.get('approximate_time_of_service'),
        )

        # verify input info
        is_valid_tuple = queue.is_valid()
        if not is_valid_tuple[0]:
            error = is_valid_tuple[1]

    # update database if everything is ok
    if error is None:
        found = dal.update_queue_by_id(queue_id, queue)
        if found:
            return jsonify(
                status=200,
                message="Queue Updated Successfully!"
            )
        else:
            return jsonify(
                status=404,
                message="Queue with ID={} not found. No changes occured!".format(
                    id)
            )
    else:
        return jsonify(
            status=400,
            message=error
        )


# DELETE:

@queues_bp.route('/<int:establishment_id>/branches/<int:branch_id>/queues', methods=['DELETE'])
def delete_queues(establishment_id, branch_id):
    """
    Does not expect any JSON object.

    Returns the following JSON Object if operation is successful:
    {
        "status" : 200, 
        "message" : "All queues have been deleted successfully!"
    }
    """
    dal.delete_queues(branch_id)
    return jsonify(
        status=200,
        message="All queues with Branch id={} have been deleted successfully!".format(
            branch_id)
    )


@queues_bp.route('/<int:establishment_id>/branches/<int:branch_id>/queues/<int:queue_id>', methods=['DELETE'])
def delete_queue_by_id(establishment_id, branch_id, queue_id):
    """
    Does not expect any JSON object.

    Returns the following JSON Object if operation is successful:
    {
        "status" : 200, 
        "message" : "Queue with Id={} have been deleted successfully!"
    }
    """
    found = dal.delete_queue_by_id(queue_id)
    if found:
        return jsonify(
            status=200,
            message="Queue with ID={} has been deleted successfully!".format(
                queue_id)
        )
    else:
        return jsonify(
            status=404,
            message="Queue with ID={} not found. No changes occured!".format(
                queue_id)
        )


# Special endpoint:

@queues_bp.route('/<int:establishment_id>/branches/<int:branch_id>/queues/<int:queue_id>/qr', methods=['POST'])
def generate_qr_for_queue(establishment_id, branch_id, queue_id):
    """
    Does not expect any JSON object.

    Returns the following JSON Object if operation is successful:
    {
        "status" : 200, 
        "message" : "QR Code has been generated and added  successfully!"
    }
    """

    found = dal.get_queue_by_id(queue_id)
    if found:
        # generate QR Code:
        qr_code = qr.generate_qr_for_queue(
            establishment_id, branch_id, queue_id)

        # convert QR code to string:
        qr_str = qr.qr_to_str(qr_code)

        # add qr code string to db:
        dal.add_qr_to_queue(queue_id, qr_str)

        return jsonify(
            status=200,
            message="QR Code for Queue with ID={} has been generated and stored successfully!".format(
                queue_id)
        )
    else:
        return jsonify(
            status=404,
            message="Queue with ID={} not found. No changes occured!".format(
                queue_id)
        )

# Removed get_qr_for_queue() since we can retrun the Queue object which contains the QR code inside of it.

# @queues_bp.route('/<int:establishment_id>/branches/<int:branch_id>/queues/<int:queue_id>/qr', methods=['GET'])
# def get_qr_for_queue(establishment_id, branch_id, queue_id):
#     """
#     Does not expect any JSON object.

#     Returns the following JSON Object if operation is successful:
#     {
#         "status" : 200,
#         "message" : qr_for_id
#     }
#     """
#     found = dal.get_queue_by_id(queue_id)
#     if found:
#         qr_for_id = dal.get_qr_by_queue_id(queue_id)

#         return jsonify(
#             status=200,
#             message=qr_for_id
#         )
#     else:
#         return jsonify(
#             status=404,
#             message="Queue with ID={} not found.".format(queue_id)
#         )
