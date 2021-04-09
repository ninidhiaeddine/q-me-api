import datetime

# import database:
from database import db


# Database Models:


class Guest(db.Model):
    # Column names:
    PK_Guest = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(20), nullable=False)
    PhoneNumber = db.Column(db.String(20), nullable=False)
    RegistrationDate = db.Column(
        db.Date, nullable=False, default=datetime.datetime.utcnow)

    def __init__(self, name, phone_number):
        self.Name = name
        self.PhoneNumber = phone_number

    def serialize(self):
        return {
            'PK_Guest': self.PK_Guest,
            'Name': self.Name,
            'PhoneNumber': self.PhoneNumber,
            'RegistrationDate': self.RegistrationDate
        }

    def update(new_guest):
        self.Name = new_guest.Name
        self.PhoneNumber = new_guest.PhoneNumber

    def is_valid(self):
        """
        Returns a Tuple(is_valid, message)
        """
        message = ""

        # verify fields:
        if type(self.Name) is not str:
            message += "Name is invalid (must be a string) | "
        elif len(self.Name) > 20:
            message += "Name is too long (20 characters max). | "

        if type(self.PhoneNumber) is not str:
            message += "Phone Number is invalid (must be a string). | "
        elif len(self.PhoneNumber) > 20:
            message += "Phone Number is too long (20 characters max). | "
        elif self.PhoneNumber[0] != '+':
            message += "Phone Number is invalid (must start with the \'+\' character). | "

        # finalize returned tuple:
        if message == "":
            is_valid = True
            message = "OK"
        else:
            is_valid = False
            # remove last 3 characters as they have an unnecessary bar in them
            message = message[:-3]

        # return tuple
        return (is_valid, message)


class Establishment(db.Model):
    PK_Establishment = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(20), nullable=False)
    Type = db.Column(db.Integer, nullable=False)
    Email = db.Column(db.String(20), nullable=False)
    Password = db.Column(db.String(20), nullable=False)
    PhoneNumber = db.Column(db.String(20), nullable=True)

    def __init__(self, name, type, email, password, phone_number=None):
        self.Name = name
        self.Type = type
        self.Email = email
        self.Password = password
        self.PhoneNumber = phone_number

    def serialize(self):
        return {
            'PK_Establishment': self.PK_Establishment,
            'Name': self.Name,
            'Type': self.Type,
            'Email': self.Email,
            'Password': self.Password,
            'PhoneNumber': self.PhoneNumber
        }

    def update(new_establishment):
        self.Name = new_establishment.Name
        self.Type = new_establishment.Type
        self.Email = new_establishment.Email
        self.Password = new_establishment.Password
        self.PhoneNumber = new_establishment.PhoneNumber

    def is_valid(self):
        """
        Returns a Tuple(is_valid, message)
        """
        message = ""

        # verify fields:
        if type(self.Name) is not str:
            message += "Name is invalid (must be a string). | "
        elif len(self.Name) > 20:
            message += "Name is too long (20 characters max). | "

        if type(self.Type) is not int:
            message += "Type is invalid (must be an int). | "

        if type(self.Email) is not str:
            message += "Email is invalid (must be a string). | "
        elif len(self.Email) > 20:
            message += "Email is too long (20 characters max). | "

        if type(self.Password) is not str:
            message += "Password is invalid (must be a string). | "

        if self.PhoneNumber is not None:
            if type(self.PhoneNumber) is not str:
                message += "Phone Number is invalid (must be a string). | "
            elif len(self.PhoneNumber) > 20:
                message += "Phone Number is too long (20 characters max). | "
            elif self.PhoneNumber[0] != '+':
                message += "Phone Number is invalid (must start with the \'+\' character). | "

        # finalize returned tuple:
        if message == "":
            is_valid = True
            message = "OK"
        else:
            is_valid = False
            # remove last 3 characters as they have an unnecessary bar in them
            message = message[:-3]

        # return tuple
        return (is_valid, message)


class Branch(db.Model):
    PK_Branch = db.Column(db.Integer, primary_key=True)
    FK_Establishment = db.Column(db.Integer, nullable=False)
    Address = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(20), nullable=False)
    Password = db.Column(db.String(20), nullable=False)
    PhoneNumber = db.Column(db.String(20), nullable=True)
    Latitude = db.Column(db.Float, nullable=True)
    Longitude = db.Column(db.Float, nullable=True)

    def __init__(self, establishment_id, address, email, password, phone_number=None, latitude=None, longitude=None):
        self.FK_Establishment = establishment_id
        self.Address = address
        self.Email = email
        self.Password = password
        self.PhoneNumber = phone_number
        self.Latitude = latitude
        self.Longitude = longitude

    def serialize(self):
        return {
            'PK_Branch': self.PK_Branch,
            'FK_Establishment': self.FK_Establishment,
            'Address': self.Address,
            'Email': self.Email,
            'Password': self.Password,
            'PhoneNumber': self.PhoneNumber,
            'Latitude': self.Latitude,
            'Longitude': self.Longitude
        }

    def update(new_branch):
        self.FK_Establishment = new_branch.FK_Establishment
        self.Address = new_branch.Address
        self.Email = new_branch.Email
        self.Password = new_branch.Password
        self.PhoneNumber = new_branch.PhoneNumber
        self.Latitude = new_branch.Latitude
        self.Longitude = new_branch.Longitude

    def is_valid(self):
        """
        Returns a Tuple(is_valid, message)
        """
        message = ""

        # verify fields:
        if type(self.Address) is not str:
            message += "Address is invalid (must be a string). | "
        elif len(self.Address) > 50:
            message += "Address is too long (50 characters max). | "

        if type(self.Email) is not str:
            message += "Email is invalid (must be a string). | "
        elif len(self.Email) > 20:
            message += "Email is too long (20 characters max). | "

        if type(self.Password) is not str:
            message += "Password is invalid (must be a string). | "

        if self.PhoneNumber is not None:
            if type(self.PhoneNumber) is not str:
                message += "Phone Number is invalid (must be a string). | "
            elif len(self.PhoneNumber) > 20:
                message += "Phone Number is too long (20 characters max). | "
            elif self.PhoneNumber[0] != '+':
                message += "Phone Number is invalid (must start with the \'+\' character). | "

        # TODO: Validate GpsLocation

        # finalize returned tuple:
        if message == "":
            is_valid = True
            message = "OK | Cannot verify \'Referential Integrity\' for Foreign Key \'EstablishmentId\' => Must be verified using DAL."
        else:
            is_valid = False
            # remove last 3 characters as they have an unnecessary bar in them
            message = message[:-3]

        # return tuple
        return (is_valid, message)


# TODO: Test the Queues:


class Queue(db.Model):
    PK_Queue = db.Column(db.Integer, primary_key=True)
    FK_Branch = db.Column(db.Integer, nullable=False)
    Name = db.Column(db.String(20), nullable=False)
    ApproximateTimeOfService = db.Column(db.Float, nullable=False)
    QRcodeEncoded = db.Column(db.String(8000),nullable=True)


    def __init__(self, branch_id, Name, ApproximateTimeOfService):
        self.FK_Branch = branch_id
        self.Name = Name
        self.ApproximateTimeOfService = ApproximateTimeOfService
        self.QRcodeEncoded = None


    def serialize(self):
        return {
            'PK_Queue': self.PK_Queue,
            'FK_Branch': self.FK_Branch,
            'Name': self.Name,
            'ApproximateTimeOfService' : self.ApproximateTimeOfService,
            'QRcodeEncoded' : self.QRcodeEncoded
        }


    def update(new_queue):
        self.FK_Branch = new_queue.FK_Branch
        self.Name = new_queue.Name
        self.ApproximateTimeOfService = new_queue.ApproximateTimeOfService


    def is_valid(self):
        """
        Returns a Tuple(is_valid, message)
        """
        message = ""

        # verify fields:
        if type(self.FK_Branch) is not int:
            message += "Branch id is invalid (must be an integer). | "
        

        # finalize returned tuple:
        if message == "":
            is_valid = True
            message = "OK | Cannot verify \'Referential Integrity\' for Foreign Key \'BranchId\' => Must be verified using DAL."
        else:
            is_valid = False
            # remove last 3 characters as they have an unnecessary bar in them
            message = message[:-3]

        # return tuple
        return (is_valid, message)

    def add_qr(QR_str,self):
        self.QRcodeEncoded = QR_str

    def get_QR(self):
        return self.QRcodeEncoded

class Token(db.Model):
    PK_Token = db.Column(db.Integer, primary_key=True)
    FK_Guest = db.Column(db.Integer, nullable=False)
    FK_Queue = db.Column(db.Integer, nullable=False)
    Status = db.Column(db.Integer, nullable=False)
    DateAndTime = db.Column(db.DateTime,default=datetime.datetime.utcnow, nullable=False)
    PositionInLine = db.Column(db.Integer, nullable=False)

    '''Status:
    0 : waiting (default)
    1 : Being serviced
    -1 : done
    every other value returns an error  
    '''
    def __init__(self, guest_id, queue_id, status, date_time, position):
        self.FK_Guest = guest_id
        self.FK_Queue = queue_id
        self.Status = status
        self.DateAndTime = date_time
        self.PositionInLine = position

    def serialize(self):
        return {
        'PK_Token': self.PK_Token,
        'FK_Guest' : self.FK_Guest,
        'FK_Queue': self.FK_Queue,
        'Status' : self.Status,
        'DateAndTime': self.DateAndTime,
        'PositionInLine': self.PositionInLine
        }

    def update(new_qu):
        self.FK_Guest = new_qu.FK_Guest
        self.FK_Queue = new_qu.FK_Queue
        self.Status = new_qu.Status
        self.DateAndTime = new_qu.DateAndTime
        self.PositionInLine = new_qu.PositionInLine


    def is_valid(self):
        """
        Returns a Tuple(is_valid, message)
        """
        message = ""

        # verify fields:
        if self.Status != 0 and self.Status != 1 and self.Status != -1 :
            message += "Status Value is not valid, must be either 1 or -1 or 0. |"
        
        if self.PositionInLine < 0:
            message += "Position in line is invalid. Must be a positive integer"


        # finalize returned tuple:
        if message == "":
            is_valid = True
            message = "OK"
        else:
            is_valid = False
            # remove last 3 characters as they have an unnecessary bar in them
            message = message[:-3]

        # return tuple
        return (is_valid, message)