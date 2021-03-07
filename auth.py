import json

from flask import (
    Blueprint, flash, request, session
)
from werkzeug.security import check_password_hash, generate_password_hash
from models import Guest, Establishment, Branch, db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register_guest', methods=['POST'])
def register_guest():
    # map json object to class object
    guest = Guest(**request.json)

    error = None

    # verify input info
    if not guest.name:
        error = 'Guest\'s Name is required.'
    elif not guest.phone_number:
        error = 'Guest\'s Phone Number is required.'
    elif db.engine.execute(
        'SELECT Id FROM Guests WHERE PhoneNumber = ?', (guest.phone_number)
    ).fetchone() is not None:
        error = 'Guest with Phone Number {} is already registered.'.format(
            guest.phone_number)

    # add to database if everything is ok
    if error is None:
        db.engine.execute(
            'INSERT INTO Guests (Name, PhoneNumber) VALUES (?, ?)',
            (guest.name, guest.phone_number)
        )
        db.session.commit()
        return "Added Guest to Database successfully!"
    else:
        return error


@auth_bp.route('/register_establishment', methods=['POST'])
def register_establishment():
    # map json object to class object
    establishment = Establishment(**request.json)

    error = None

    # verify input info
    if not establishment.name:
        error = 'Establishment\'s Name is required.'
    elif not establishment.type:
        error = 'Establishment\'s Type is required.'
    elif not establishment.email:
        error = 'Establishment\'s Email is required.'
    elif not establishment.password:
        error = 'Establishment\'s Password is required.'
    elif db.engine.execute(
        'SELECT Id FROM Establishments WHERE Name = ?', (establishment.name)
    ).fetchone() is not None:
        error = 'Establishment {} is already registered.'.format(
            establishment.name)

    # add to database if everything is ok
    if error is None:
        db.engine.execute(
            'INSERT INTO Establishments (Name, Type, Email, Password) VALUES (?, ?, ?, ?)',
            (establishment.name, establishment.type,
             establishment.email, generate_password_hash(establishment.password))
        )
        db.session.commit()
        return "Added Establishment to Database successfully!"
    else:
        return error


@auth_bp.route('/register_branch', methods=['POST'])
def register_branch():
    # map json object to class object
    branch = Branch(**request.json)

    error = None

    # verify input info
    if not branch.establishment_id:
        error = 'Branch\'s Establishment\'s ID is required.'
    elif not branch.address:
        error = 'Branch\'s Address is required.'

    # add to database if everything is ok
    if error is None:
        db.engine.execute(
            'INSERT INTO Branches (EstablishmentId, Address) VALUES (?, ?, ?, ?)',
            (branch.establishment_id, branch.address.type)
        )
        db.session.commit()
        return "Added Branch to Database successfully!"
    else:
        return error


@auth_bp.route('/login_guest', methods=['POST'])
def login_guest():
    # map json object to class object
    guest = Guest(**request.json)

    error = None

    # fetch the record from the database
    guest_record = db.engine.execute(
        'SELECT * FROM Guests WHERE Name = ?', (guest.name)
    ).fetchone()

    # verify credentials
    if guest_record is None:
        error = 'Incorrect Guest\'s Name.'
    elif guest_record['PhoneNumber'] != guest.phone_number:
        error = 'Incorrect Guest\'s Phone Number.'

    # start new session if evertthing is ok
    if error is None:
        session.clear()
        session['guest_id'] = guest_record['Id']
        return "Guest logged in Successfully!"
    else:
        return error


@auth_bp.route('/login_establishment', methods=['POST'])
def login_establishment():
    # map json object to class object
    establishment_dict = json.load(request.json)
    establishment = Establishment(**establishment_dict)

    error = None

    # fetch the record from the database
    establishment_record = db.engine.execute(
        'SELECT * FROM Establishments WHERE Email = ?', (establishment.email)
    ).fetchone()

    # verify credentials
    if establishment_record is None:
        error = 'Incorrect Establishment\'s Email.'
    elif not check_password_hash(establishment_record['Password'], establishment.password):
        error = 'Incorrect Establishment\'s Password.'

    # start new session if evertthing is ok
    if error is None:
        session.clear()
        session['establishment_id'] = establishment_record['Id']
        return "Establishment logged in successfully!"
    else:
        return error


@auth_bp.route('/logout')
def logout():
    session.clear()
    return "Logged out successfully!"
