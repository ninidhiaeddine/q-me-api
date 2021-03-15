# Data Access Layer (Script)

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from models import Guest, Establishment, Branch


db = SQLAlchemy()

# Guests related functions:


def get_guests():
    sql_query = 'SELECT * FROM Guests'
    result = db.engine.execute(sql_query).fetchall()

    guests = []
    for row in result:
        guest = Guest(
            row['Id'],
            row['Name'],
            row['PhoneNumber']
        )
        guests.append(guest)
    return guests


def get_guest_by_id(id):
    sql_query = 'SELECT * FROM Guests WHERE Id = {}'.format(id)
    result = db.engine.execute(sql_query).fetchone()

    if result is not None:
        guest = Guest(
            result['Id'],
            result['Name'],
            result['PhoneNumber']
        )
        return guest
    else:
        return None


def get_guest_by_name(name):
    sql_query = 'SELECT * FROM Guests WHERE Name = \'{}\''.format(name)
    result = db.engine.execute(sql_query).fetchone()

    if result is not None:
        guest = Guest(
            result['Id'],
            result['Name'],
            result['PhoneNumber']
        )
        return guest
    else:
        return None


def get_guest_by_phone_number(phone_number):
    sql_query = 'SELECT * FROM Guests WHERE PhoneNumber = \'{}\''.format(
        phone_number)
    result = db.engine.execute(sql_query).fetchone()

    if result is not None:
        guest = Guest(
            result['Id'],
            result['Name'],
            result['PhoneNumber']
        )
        return guest
    else:
        return None


def add_guest(guest):
    # the field 'id' doesn't matter when adding:
    sql_query = 'INSERT INTO Guests (Name, PhoneNumber) VALUES (\'{}\', \'{}\')'.format(
        guest.name, guest.phone_number)
    db.engine.execute(sql_query)
    db.session.commit()


# Establishments related functions:


def get_establishments():
    sql_query = 'SELECT * FROM Establishments'
    result = db.engine.execute(sql_query).fetchall()

    establishments = []
    for row in result:
        establishment = Establishment(
            row['Id'],
            row['Name'],
            row['Type'],
            row['Email'],
            row['Password']
        )
        establishments.append(establishment)
    return establishments


def get_establishment_by_id(id):
    sql_query = 'SELECT * FROM Establishments WHERE Id = {}'.format(id)
    result = db.engine.execute(sql_query).fetchone()

    if result is not None:
        establishment = Establishment(
            result['Id'],
            result['Name'],
            result['Type'],
            result['Email'],
            result['Password']
        )
        return establishment
    else:
        return None


def get_establishment_by_name(name):
    sql_query = 'SELECT * FROM Establishments WHERE Name = \'{}\''.format(name)
    result = db.engine.execute(sql_query).fetchone()

    if result is not None:
        establishment = Establishment(
            result['Id'],
            result['Name'],
            result['Type'],
            result['Email'],
            result['Password']
        )
        return establishment
    else:
        return None


def get_establishments_by_type(type):
    sql_query = 'SELECT * FROM Establishments WHERE Type = {}'.format(type)
    result = db.engine.execute(sql_query).fetchall()

    establishments = []
    for row in result:
        establishment = Establishment(
            row['Id'],
            row['Name'],
            row['Type'],
            row['Email'],
            row['Password']
        )
        establishments.append(establishment)
    return establishments


def get_establishment_by_email(email):
    sql_query = 'SELECT * FROM Establishments WHERE Email = \'{}\''.format(
        email)
    result = db.engine.execute(sql_query).fetchone()

    if result is not None:
        establishment = Establishment(
            result['Id'],
            result['Name'],
            result['Type'],
            result['Email'],
            result['Password']
        )
        return establishment
    else:
        return None


def add_establishment(establishment):
    # the field 'id' doesn't matter when adding:
    sql_query = 'INSERT INTO Establishments (Name, Type, Email, Password) VALUES (\'{}\', {}, \'{}\', \'{}\')'.format(
        establishment.name,
        establishment.type,
        establishment.email,
        generate_password_hash(establishment.password)
    )
    db.engine.execute(sql_query)
    db.session.commit()


# Branches related functions:


def get_branches():
    sql_query = 'SELECT * FROM Branches'
    result = db.engine.execute(sql_query).fetchall()

    branches = []
    for row in result:
        branch = Branch(
            row['Id'],
            row['EstablishmentId'],
            row['Address']
        )
        branches.append(branch)
    return branches


def get_branch_by_id(id):
    sql_query = 'SELECT * FROM Branches WHERE Id = {}'.format(id)
    result = db.engine.execute(sql_query).fetchone()

    if result is not None:
        branch = Branch(
            row['Id'],
            row['EstablishmentId'],
            row['Address']
        )
        return branch
    else:
        return None


def get_branches_by_establishment_id(establishment_id):
    sql_query = 'SELECT * FROM Branches WHERE EstablishmentId = {}'.format(
        establishment_id)
    result = db.engine.execute(sql_query).fetchall()

    branches = []
    for row in result:
        branch = Branch(
            row['Id'],
            row['EstablishmentId'],
            row['Address']
        )
        branches.append(branch)
    return branches


def get_branch_by_address(address):
    sql_query = 'SELECT * FROM Branches WHERE Address = \'{}\''.format(address)
    result = db.engine.execute(sql_query).fetchone()

    if result is not None:
        branch = Branch(
            row['Id'],
            row['EstablishmentId'],
            row['Address']
        )
        return branch
    else:
        return None


def add_branch(branch):
    # the field 'id' doesn't matter when adding:
    sql_query = 'INSERT INTO Branches (EstablishmentId, Address) VALUES ({}, \'{}\')'.format(
        branch.establishment_id,
        branch.address
    )
    db.engine.execute(sql_query)
    db.session.commit()
