from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Guest:
    def __init__(self, name, phone_number):
        self.name = name
        self.phone_number = phone_number


class Establishment:
    def __init__(self, name, type, email, password):
        self.name = name
        self.type = type
        self.email = email
        self.password = password


class Branch:
    def __init__(self, establishment_id, address):
        self.establishment_id = establishment_id
        self.address = address
