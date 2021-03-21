# Data Access Layer (Script)

from werkzeug.security import check_password_hash, generate_password_hash
from models import Guest, Establishment, Branch

# import database:
from database import db


# Guests related functions:


def get_guests():
    """
    Returns the list of guests
    """
    return Guest.query.all()


def get_guest_by_id(id):
    """
    Returns the target guest if found. Returns None otherwise.
    """
    return Guest.query.filter_by(PK_Guest=id).first()


def get_guest_by_name(name):
    """
    Returns the target guest
    """
    return Guest.query.filter_by(Name=name).first()


def get_guest_by_phone_number(phone_number):
    """
    Returns the target guest
    """
    return Guest.query.filter_by(PhoneNumber=phone_number).first()


def add_guest(guest):
    """
    Does not return anything
    """
    db.session.add(guest)
    db.session.commit()


def update_guest_by_id(id, guest):
    """
    Returns True if update succeeds; returns False otherwise.
    """
    target_guest = Guest.query.filter_by(PK_Guest=id).first()
    if target_guest is not None:
        target_guest.update(guest)
        db.session.commit()
        return True
    else:
        return False


def delete_guests():
    """
    Does not return anything.
    """
    Guest.query.delete()
    db.session.commit()


def delete_guest_by_id(id):
    """
    Returns True if deletion succeeds; returns False otherwise.
    """
    target_guest = Guest.query.filter_by(PK_Guest=id).first()
    if target_guest is not None:
        db.session.delete(target_guest)
        db.session.commit()
        return True
    else:
        return False


# Establishments related functions:


def get_establishments():
    """
    Returns the list of establishments
    """
    return Establishment.query.all()


def get_establishment_by_id(id):
    """
    Returns the target establishment if found. Returns None otherwise.
    """
    return Establishment.query.filter_by(PK_Establishment=id).first()


def get_establishment_by_name(name):
    """
    Returns the target establishment
    """
    return Establishment.query.filter_by(Name=name).first()


def get_establishments_by_type(type):
    """
    Returns a list of establishments which are of type 'type'
    """
    return Establishment.query.filter_by(Type=type).all()


def get_establishment_by_email(email):
    """
    Returns the target establishment
    """
    return Establishment.query.filter_by(Email=email).first()


def get_establishment_by_phone_number(phone_number):
    """
    Returns the target establishment
    """
    return Establishment.query.filter_by(PhoneNumber=phone_number).first()


def add_establishment(establishment):
    """
    Does not return anything
    """
    db.session.add(establishment)
    db.session.commit()


def update_establishment_by_id(id, establishment):
    """
    Returns True if update succeeds; returns False otherwise.
    """
    target_establishment = Establishment.query.filter_by(
        PK_Establishment=id).first()
    if target_establishment is not None:
        target_establishment.update(establishment)
        db.session.commit()
        return True
    else:
        return False


def delete_establishments():
    """
    Does not return anything.
    """
    Establishment.query.delete()
    db.session.commit()


def delete_establishment_by_id(id):
    """
    Returns True if deletion succeeds; returns False otherwise.
    """
    target_establishment = Establishment.query.filter_by(
        PK_Establishment=id).first()
    if target_establishment is not None:
        db.session.delete(target_establishment)
        db.session.commit()
        return True
    else:
        return False


# Branches related functions:


def get_branches(establishment_id):
    """
    Returns the list of branches
    """
    return Branch.query.filter_by(FK_Establishment=establishment_id).all()


def get_branch_by_id(establishment_id, branch_id):
    """
    Returns the target branch if found. Returns None otherwise.
    """
    return Branch.query.filter_by(FK_Establishment=establishment_id, PK_Branch=branch_id).first()


def get_branch_by_name(name):
    """
    Returns the target branch
    """
    return Branch.query.filter_by(Name=name).first()


def get_branch_by_address(address):
    """
    Returns a list of branches which are of type 'type'
    """
    return Branch.query.filter_by(address=address).first()


def get_branch_by_email(email):
    """
    Returns the target branch
    """
    return Branch.query.filter_by(Email=email).first()


def get_branch_by_phone_number(phone_number):
    """
    Returns the target branch
    """
    return Branch.query.filter_by(PhoneNumber=phone_number).first()


def get_branch_by_gps_location(gps_location):
    """
    Returns the target branch
    """
    return Branch.query.filter_by(GpsLocation=gps_location).first()


def add_branch(branch):
    """
    Does not return anything
    """
    db.session.add(branch)
    db.session.commit()


def update_branch_by_id(id, branch):
    """
    Returns True if update succeeds; returns False otherwise.
    """
    target_branch = Branch.query.filter_by(
        PK_Branch=id).first()
    if target_branch is not None:
        target_branch.update(branch)
        db.session.commit()
        return True
    else:
        return False


def delete_branches():
    """
    Does not return anything.
    """
    Branch.query.delete()
    db.session.commit()


def delete_branch_by_id(id):
    """
    Returns True if deletion succeeds; returns False otherwise.
    """
    target_branch = Branch.query.filter_by(
        PK_Branch=id).first()
    if target_branch is not None:
        db.session.delete(target_branch)
        db.session.commit()
        return True
    else:
        return False


# TODO: Finish designin remaining DAL functions:
