# Data Access Layer (Script)


from models import Guest, Establishment, Branch, Queue, Token, CovidInfection, OTP

# import database:
from database import db

# importing func for function calls
from sqlalchemy import func


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
    target_guest = Guest.query.filter_by(PK_Guest=id)
    if target_guest is not None:
        target_guest.delete()
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
        PK_Establishment=id)
    if target_establishment is not None:
        target_establishment.delete()
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


def get_branch_by_id(branch_id):
    """
    Returns the target branch if found. Returns None otherwise.
    """
    return Branch.query.filter_by(PK_Branch=branch_id).first()


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
        FK_Establishment=establishment_id)

    if target_branches is not None:
        target_branches.delete()
        db.session.commit()
        return True
    else:
        return False


def delete_branch_by_id(establishment_id, branch_id):
    """
    Returns True if deletion succeeds; returns False otherwise.
    """
    target_branch = Branch.query.filter_by(
        PK_Branch=branch_id, FK_Establishment=establishment_id)

    if target_branch is not None:
        target_branch.delete()
        db.session.commit()
        return True
    else:
        return False


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
    return Queue.query.filter_by(PK_Queue=queue_id).first()


def get_queue_by_name(branch_id, name):
    """
    Returns the target queue if found. Returns None otherwise.
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
    target_queues = Queue.query.filter_by(FK_Branch=branch_id)

    if target_queues is not None:
        target_queues.delete()
        db.session.commit()
        return True
    else:
        return False


def delete_queue_by_id(queue_id):
    """
    Returns True if deletion succeeds; returns False otherwise.
    """
    target_queue = Queue.query.filter_by(PK_Queue=queue_id)

    if target_queue is not None:
        target_queue.delete()
        db.session.commit()
        return True
    else:
        return False


def add_qr_to_queue(queue_id, qr_str):
    """
    Takes a string QR code and adds it to the database.
    """
    target_queue = Queue.query.filter_by(PK_Queue=queue_id).first()

    if target_queue is not None:
        # add qr code to the queue:
        target_queue.add_qr(qr_str)

        # commit the changes:
        db.session.commit()


def get_qr_by_queue_id(queue_id):
    """
    takes a queue id and return its QR code as a string
    """
    target_queue = Queue.query.filter_by(PK_Queue=queue_id).first()
    return target_queue.get_qr(target_queue)

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
    return Token.query.filter_by(PK_Token=token_id).first()


def get_tokens_by_status(queue_id, status):
    """
    Returns the list of tokens with a given status
    """
    return Token.query.filter_by(FK_Queue=queue_id, Status=status)


def get_token(queue_id, guest_id):
    """
    Returns a token with a given queue id and guest id
    """
    return Token.query.filter_by(FK_Queue=queue_id, FK_Guest=guest_id).first()


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
    target_tokens = Token.query.filter_by(FK_Queue=queue_id)

    if target_tokens is not None:
        target_tokens.delete()
        db.session.commit()
        return True
    else:
        return False


def delete_token_by_id(token_id):
    """
    Returns True if deletion succeeds; returns False otherwise.
    """
    target_token = Token.query.filter_by(PK_Token=token_id)

    if target_token is not None:
        target_token.delete()
        db.session.commit()
        return True
    else:
        return False


# def get_covid_infections():
#     """
#     Returns the list of covid_infections
#     """
#     return CovidInfection.query.all()


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


def get_position_in_line(queue_id, guest_id):
    """
    Returns the Positon in Line of a given Guest if found.
    Returns -1 otherwise.
    """
    try:
        # Call on a database SQL function GetPositionInLine(queue_id, guest_id)
        result = db.session.query(
            func.dbo.GetPositionInLine(queue_id, guest_id)).first()
        return result[0]
    except:
        return -1


def get_people_enqueuing_count(queue_id):
    """
    Returns the number of people enqueuing in a given Queue if found.
    Returns -1 otherwise.
    """
    try:
        # Call on a database SQL function GetPeopleEnqueingCount(queue_id, guest_id)
        result = db.session.query(
            func.dbo.GetPeopleEnqueingCount(queue_id)).first()
        return result[0]
    except:
        return -1


def serve_guest(queue_id):
    """
    Executes Db procedure to serve the 1st person in line in a given Queue.

    Returns guest_id (of the served guest) if guest has been served successfully.
    Returns -1 otherwise.
    """

    connection = db.engine.raw_connection()
    sql_query = """DECLARE @ServedGuestId INT
        SET NOCOUNT ON
        EXEC ServeGuest {}, @ServedGuestId OUTPUT
        SELECT @ServedGuestId; """.format(queue_id)

    try:
        cursor = connection.cursor()
        cursor.execute(sql_query)
        result = cursor.fetchone()
        connection.commit()
        return result[0]
    except:
        return -1


def dequeue_guest(queue_id):
    """
    Executes Db procedure to dequeue the person being served in a given Queue.

    Returns guest_id (of the served guest) if guest has been dequeued successfully.
    Returns -1 otherwise.
    """
    connection = db.engine.raw_connection()
    sql_query = """DECLARE @DequeuedGuestId INT
        SET NOCOUNT ON
        EXEC DequeueGuest {}, @DequeuedGuestId OUTPUT
        SELECT @DequeuedGuestId;""".format(queue_id)

    try:
        cursor = connection.cursor()
        cursor.execute(sql_query)
        result = cursor.fetchone()
        connection.commit()
        return result[0]
    except:
        return -1


def close_queue(queue_id):
    """
    Executes Db procedure to close a given Queue.
    Effect: All guests enqueuing in this Queue will be dequeued.

    Returns True if queue has been closed successfully.
    Returns False otherwise.
    """
    connection = db.session.connection()
    sql_query = "EXEC CloseQueue @QueueId = {};".format(queue_id)

    try:
        connection.execute(sql_query)
        return True
    except:
        return False


def add_otp(otp):
    """
    adds OTP object to its table
    """
    db.session.add(otp)
    db.session.commit()


def get_otp_by_guest_id(guest_id):
    """ 
    returns otp of a guest
     """
    return OTP.query.filter_by(FK_Guest=guest_id).first()


def check_otp_dal(guest_id, input_otp):
    """
    Return a bool
    """
    record_otp = get_otp_by_guest_id(guest_id)

    result = record_otp.Value == input_otp
    return result
