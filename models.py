# Database Models (Plain Old Objects)

class Guest:
    def __init__(self, id, name, phone_number):
        self.id = id
        self.name = name
        self.phone_number = phone_number

    def is_valid(self):
        """
        Returns a Tuple(is_valid, message)
        """
        message = ""

        # verify fields:
        if type(self.name) is not str:
            message += "Name is invalid (must be a string) | "
        elif len(self.name) > 30:
            message += "Name is too long (30 characters max). | "

        if type(self.phone_number) is not str:
            message += "Phone Number is invalid (must be a string). | "
        elif len(self.phone_number) > 20:
            message += "Phone Number is too long (20 characters max). | "
        elif self.phone_number[0] != '+':
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
