# Data Access Layer (Script)

from werkzeug.security import check_password_hash, generate_password_hash
from models import Guest, Establishment, Branch, Queue, Token, CovidInfection

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


def get_branch_by_name(establishment_id, name):
    """
    Returns the target branch
    """
    return Branch.query.filter_by(FK_Establishment=establishment_id, Name=name).first()


def get_branch_by_address(establishment_id, address):
    """
    Returns a list of branches which are of type 'type'
    """
    return Branch.query.filter_by(FK_Establishment=establishment_id, address=address).first()


def get_branch_by_email(establishment_id, email):
    """
    Returns the target branch
    """
    return Branch.query.filter_by(FK_Establishment=establishment_id, Email=email).first()


def get_branch_by_phone_number(establishemnt_id, phone_number):
    """
    Returns the target branch
    """
    return Branch.query.filter_by(FK_Establishment=establishment_id, PhoneNumber=phone_number).first()


def get_branch_by_gps_location(establishment_id, latitude, longitude):
    """
    Returns the target branch
    """
    return Branch.query.filter_by(FK_Establishment=establishment_id, Latitude=latitude, Longitude=longitude).first()


def add_branch(branch):
    """
    Does not return anything
    """
    db.session.add(branch)
    db.session.commit()


def update_branch_by_id(establishment_id, branch_id, branch):
    """
    Returns True if update succeeds; returns False otherwise.
    """
    target_branch = Branch.query.filter_by(
        PK_Branch=branch_id, FK_Establishment=establishment_id).first()

    if target_branch is not None:
        target_branch.update(branch)
        db.session.commit()
        return True
    else:
        return False


def delete_branches(establishment_id):
    """
    Returns True if deletion succeeds; returns False otherwise.
    """
    target_branches = Branch.query.filter_by(
        FK_Establishment=establishment_id).all()

    if target_branches is not None:
        db.session.delete(target_branches)
        db.session.commit()
        return True
    else:
        return False


def delete_branch_by_id(establishment_id, branch_id):
    """
    Returns True if deletion succeeds; returns False otherwise.
    """
    target_branch = Branch.query.filter_by(
        PK_Branch=branch_id, FK_Establishment=establishment_id).first()

    if target_branch is not None:
        db.session.delete(target_branch)
        db.session.commit()
        return True
    else:
        return False


# TODO: Finish designing remaining DAL functions:

# Queues related functions:


def get_queues(branch_id):
    """
    Returns the list of queues
    """
    return Queue.query.filter_by(FK_Branch=branch_id).all()


def get_queue_by_id(queue_id):
    """
    Returns the target queue if found. Returns None otherwise.
    """
    return Queue.query.filter_by(PK_Queue=queue_id).all()


def get_queue_by_name(branch_id, name):
    """
    Returns the target queue
    """
    return Queue.query.filter_by(FK_Branch=branch_id, Name=name).first()


def add_queue(queue):
    """
    Does not return anything
    """
    db.session.add(queue)
    db.session.commit()


def update_queue_by_id(queue_id, queue):
    """
    Returns True if update succeeds; returns False otherwise.
    """
    target_queue = Queue.query.filter_by(PK_Queue=queue_id).first()

    if target_queue is not None:
        target_queue.update(queue)
        db.session.commit()
        return True
    else:
        return False


def delete_queues(branch_id):
    """
    Returns True if deletion succeeds; returns False otherwise.
    """
    target_queues = Queue.query.filter_by(FK_Branch=branch_id).all()

    if target_queues is not None:
        db.session.delete(target_queues)
        db.session.commit()
        return True
    else:
        return False


def delete_queue_by_id(queue_id):
    """
    Returns True if deletion succeeds; returns False otherwise.
    """
    target_queue = Queue.query.filter_by(PK_Queue=queue_id).first()

    if target_queue is not None:
        db.session.delete(target_queue)
        db.session.commit()
        return True
    else:
        return False


def add_qr_to_queue(queue_id, QR_str):
    '''
        takes a string QR code and adds it to the database
    '''
    target_queue = Queue.query.filter_by(PK_Queue=queue_id).first()

    db.session.add_qr(QR_str, queue_id)
    db.session.commit()


def get_QR_queue_by_id(queue_id):
    '''
        takes a queue id and return its QR code as a string
    '''
    target_queue = Queue.query.filter_by(PK_Queue=queue_id).first()
    return target_queue.get_QR(target_queue)


# Tokens related functions:


def get_tokens(queue_id):
    """
    Returns the list of tokens
    """
    return Token.query.filter_by(FK_Queue=queue_id).all()


def get_token_by_id(token_id):
    """
    Returns a token
    """
    return Token.query.filter_by(PK_Token=token_id).all()


def add_token(token):
    """
    Does not return anything
    """
    db.session.add(token)
    db.session.commit()


def update_token_by_id(token_id, token):
    """
    Returns True if update succeeds; returns False otherwise.
    """
    target_token = Token.query.filter_by(PK_Token=token_id).first()

    if target_token is not None:
        target_token.update(token)
        db.session.commit()
        return True
    else:
        return False


def delete_tokens(queue_id):
    """
    Returns True if deletion succeeds; returns False otherwise.
    """
    target_tokens = Token.query.filter_by(FK_Queue=queue_id).all()

    if target_tokens is not None:
        db.session.delete(target_tokens)
        db.session.commit()
        return True
    else:
        return False


def delete_token_by_id(token_id):
    """
    Returns True if deletion succeeds; returns False otherwise.
    """
    target_token = Token.query.filter_by(PK_Token=token_id).all()

    if target_token is not None:
        db.session.delete(target_token)
        db.session.commit()
        return True
    else:
        return False


def get_covid_infections():
    """
    Returns the list of covid_infections
    """
    return CovidInfection.query.all()


# def get_covid_infection_by_id(id):
#     """
#     Returns the target covid_infection if found. Returns None otherwise.
#     """
#     return CovidInfection.query.filter_by(PK_CovidInfection=id).first()


# def add_covid_infection(covid_infection):
#     """
#     Does not return anything
#     """
#     db.session.add(covid_infection)
#     db.session.commit()


# def update_covid_infection_by_id(id, covid_infection):
#     """
#     Returns True if update succeeds; returns False otherwise.
#     """
#     target_covid_infection = CovidInfection.query.filter_by(
#         PK_CovidInfection=id).first()
#     if target_covid_infection is not None:
#         target_covid_infection.update(covid_infection)
#         db.session.commit()
#         return True
#     else:
#         return False


# def delete_covid_infections():
#     """
#     Does not return anything.
#     """
#     CovidInfection.query.delete()
#     db.session.commit()


# def delete_covid_infection_by_id(id):
#     """
#     Returns True if deletion succeeds; returns False otherwise.
#     """
#     target_covid_infection = CovidInfection.query.filter_by(
#         PK_CovidInfection=id).first()
#     if target_covid_infection is not None:
#         db.session.delete(target_covid_infection)
#         db.session.commit()
#         return True
#     else:
#         return False
