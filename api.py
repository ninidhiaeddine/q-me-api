
# import flask modules
from flask import Flask
from flask_cors import CORS, cross_origin
import urllib.parse

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

# import database
from database import db

# import blueprints
from blueprints.register import register_bp
from blueprints.auth import auth_bp
from blueprints.guests import guests_bp
from blueprints.establishments import establishments_bp
from blueprints.branches import branches_bp
from blueprints.queues import queues_bp
from blueprints.tokens import tokens_bp
from blueprints.ratings import ratings_bp
from blueprints.operating_hours import operating_hours_bp
from blueprints.feedback import feedback_bp
from blueprints.contact_messages import contact_messages_bp
from blueprints.covid_infections import covid_infections_bp


# configure database URI
CONNETION_STRING = "Driver={ODBC Driver 13 for SQL Server};"\
    "Server=tcp:q-me.database.windows.net,1433;"\
    "Database=q-me-database;"\
    "Uid=ninidhia-proj-16;"\
    "Pwd=cM9s$AZTdeZs5Yt;"\
    "Encrypt=yes;"\
    "TrustServerCertificate=no;"\
    "Connection Timeout=30;"

params = urllib.parse.quote_plus(CONNETION_STRING)

# initialization
app = Flask(__name__)
# initialize CORS
cors = CORS(app)
# initialize JWT
app.config['JWT_SECRET_KEY'] = '5GNVM9McWdtnN778Fhmj'  # Change this!
jwt = JWTManager(app)

# app config:
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SECRET_KEY'] = "cM9s$AZTdeZs5Yt"
app.config['CORS_HEADERS'] = 'Content-Type'


# register blueprints
app.register_blueprint(register_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(guests_bp)
app.register_blueprint(establishments_bp)
app.register_blueprint(branches_bp)
app.register_blueprint(queues_bp)
app.register_blueprint(tokens_bp)
app.register_blueprint(covid_infections_bp)


# TODO: Implement the following blueprints:
# app.register_blueprint(ratings_bp)
# app.register_blueprint(feedback_bp)
# app.register_blueprint(contact_messages_bp)
# app.register_blueprint(operating_hours_bp)


# extensions
db.app = app
db.init_app(app)
