from database import db
import datetime

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

    def is_valid(self):
        """
        Returns a Tuple(is_valid, message)
        """
        message = ""

        # verify fields:
        if type(self.Name) is not str:
            message += "Name is invalid (must be a string) | "
        elif len(self.Name) > 30:
            message += "Name is too long (30 characters max). | "

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


class Establishment:
    def __init__(self, id, name, type, email, password):
        self.id = id
        self.name = name
        self.type = type
        self.email = email
        self.password = password

    def is_valid(self):
        """
        Returns a Tuple(is_valid, message)
        """
        message = ""

        # verify fields:
        if type(self.name) is not str:
            message += "Name is invalid (must be a string). | "
        elif len(self.name) > 30:
            message += "Name is too long (30 characters max). | "

        if type(self.type) is not int:
            message += "Type is invalid (must be an int). | "

        if type(self.email) is not str:
            message += "Email is invalid (must be a string). | "
        elif len(self.email) > 20:
            message += "Email is too long (20 characters max). | "

        if type(self.password) is not str:
            message += "Password is invalid (must be a string). | "

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


class Branch:
    def __init__(self, id, establishment_id, address):
        self.id = id
        self.establishment_id = establishment_id
        self.address = address

    def is_valid(self):
        """
        Returns a Tuple(is_valid, message)
        """
        message = ""

        # verify fields:
        if type(self.address) is not str:
            message += "Address is invalid (must be a string). | "
        elif len(self.address) > 30:
            message += "Address is too long (30 characters max). | "

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
