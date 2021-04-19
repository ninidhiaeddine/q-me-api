import json

from flask import (
    Blueprint, flash, request, session, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from models import CovidInfection
import dal  # import data access layer
import helpers

covid_infections_bp = Blueprint(
    'covid_infections_bp', __name__, url_prefix='/covidinfections')


# GET:

@covid_infections_bp.route('', methods=['GET'])
def get_covid_infections():
    """
    Does not expect any JSON object.

    Returns the following JSON Object if operation is successful:
    {
        "status" : 200,
        "message" : covid_infections_list
    }
    """
    covid_infections_list = dal.get_covid_infections()
    if len(covid_infections_list) > 0:
        return jsonify(
            status=200,
            message=[CovidInfection.serialize()
                     for covid_infection in covid_infections_list]
        )
    else:
        return jsonify(
            status=404,
            message="List of Covid_infections is empty!"
        )


# @covid_infections_bp.route('/<int:id>', methods=['GET'])
# def get_covid_infection_by_id(id):
#     """
#     Does not expect any JSON object.

#     Returns the following JSON Object if operation is successful:
#     {
#         "status" : 200,
#         "message" : covid_infection_with_id
#     }
#     """
#     covid_infection_with_id = dal.get_covid_infection_by_id(id)
#     if covid_infection_with_id is not None:
#         return jsonify(
#             status=200,
#             message=covid_infection_with_id.serialize()
#         )
#     else:
#         return jsonify(
#             status=404,
#             message="Covid_infection with ID={} not found!".format(id)
#         )


# # POST:

# @covid_infections_bp.route('', methods=['POST'])
# def add_covid_infection():
#     """
#     Expects the following JSON Object:
#     {
#         "guest_id" : "guest's ID",
#         "dateTested" : "The day of COVID test in datetime format",
#         "dateRecorded" : "The day of COVID result recorded in datetime format",
#     }

#     Returns the following JSON Object if operation is successful:
#     {
#         "status" : 200,
#         "message" : "Covid_infection Added to Database successfully!"
#     }
#     """

#     # initially, assume that there is no error
#     error = None

#     if not helpers.request_is_valid(request, keys_list=['guest_id', 'dateTested', 'dateRecorded']):
#         error = "Invalid JSON Object."

#     if error is None:
#         # map json object to class object
#         covid_infection = Covid_infection(
#             request.json.get('guest_id'),
#             request.json.get('dateTested'),
#             request.json.get('dateRecorded')
#         )

#         # verify input info
#         is_valid_tuple = covid_infection.is_valid()
#         if is_valid_tuple[0]:
#             if dal.get_covid_infection_by_email(covid_infection.Email) is not None:
#                 error = 'Covid_infection with Email=\'{}\' is already registered.'.format(
#                     covid_infection.Email)
#         else:
#             error = is_valid_tuple[1]

#     # add to database if everything is ok
#     if error is None:
#         dal.add_covid_infection(covid_infection)
#         return jsonify(
#             status=200,
#             message="Covid_infection Added to Database successfully!"
#         )
#     else:
#         return jsonify(
#             status=400,
#             message=error
#         )

# PUT:


# @covid_infections_bp.route('/<int:id>', methods=['PUT'])
# def update_covid_infection_by_id(id):
#     """
#     Expects the following JSON Object:
#     {
#         "name" : "your covid_infection's name here",
#         "type" : 0,
#         "email" : "your email here",
#         "password" : "your password here",
#         "phone_number" : "your phone number here" /* (optional) */
#     }

#     Returns the following JSON Object if operation is successful:
#     {
#         "status" : 200,
#         "message" : "Covid_infection Updated Successfully!"
#     }
#     """

#     initially, assume that there is no error
#     error = None

#     verify expected JSON:
#     if not helpers.request_is_valid(request, keys_list=['name', 'type', 'email', 'password']):
#         error = "Invalid JSON Object."

#     if error is None:
#         map json object to class object
#         covid_infection = Covid_infection(
#             request.json.get('name'),
#             request.json.get('type'),
#             request.json.get('email'),
#             TODO Fix DB Password Hashing Problem
#             generate_password_hash(request.json.get('password'))
#             request.json.get('password'),
#             request.json.get('phone_number')
#         )

#         initially, assume that there is no error
#         error = None

#         verify input info
#         is_valid_tuple = covid_infection.is_valid()
#         if not is_valid_tuple[0]:
#             error = is_valid_tuple[1]

#      update database if everything is ok
#     if error is None:
#         found = dal.update_covid_infection_by_id(id, covid_infection)
#         if found:
#             return jsonify(
#                 status=200,
#                 message="Covid_infection Updated Successfully!"
#             )
#         else:
#             return jsonify(
#                 status=404,
#                 message="Covid_infection with ID={} not found. No changes occured!".format(
#                     id)
#             )
#     else:
#         return jsonify(
#             status=400,
#             message=error
#         )


# DELETE:

# @covid_infections_bp.route('', methods=['DELETE'])
# def delete_covid_infections():
#     """
#     Does not expect any JSON object.

#     Returns the following JSON Object if operation is successful:
#     {
#         "status" : 200,
#         "message" : "All covid_infections have been deleted successfully!"
#     }
#     """
#     dal.delete_covid_infections()
#     return jsonify(
#         status=200,
#         message="All covid_infections have been deleted successfully!"
#     )


# @covid_infections_bp.route('/<int:id>', methods=['DELETE'])
# def delete_covid_infection_by_id(id):
#     """
#     Does not expect any JSON object.

#     Returns the following JSON Object if operation is successful:
#     {
#         "status" : 200,
#         "message" : "All Covid_infections have been deleted successfully!"
#     }
#     """
#     found = dal.delete_covid_infection_by_id(id)
#     if found:
#         return jsonify(
#             status=200,
#             message="Covid_infection with ID={} has been deleted successfully!".format(
#                 id)
#         )
#     else:
#         return jsonify(
#             status=404,
#             message="Covid_infection with ID={} not found. No changes occured!".format(
#                 id)
#         )
