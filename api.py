
# import flask modules
from flask import Flask
import urllib.parse

# import database
from database import db

# import blueprints
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
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SECRET_KEY'] = "cM9s$AZTdeZs5Yt"

# register blueprints
app.register_blueprint(guests_bp)
app.register_blueprint(establishments_bp)
app.register_blueprint(branches_bp)

# TODO: Implement the following blueprints:
# app.register_blueprint(queues_bp)
# app.register_blueprint(tokens_bp)
# app.register_blueprint(ratings_bp)
# app.register_blueprint(feedback_bp)
# app.register_blueprint(contact_messages_bp)
# app.register_blueprint(operating_hours_bp)
# app.register_blueprint(covid_infections_bp)

# extensions
db.app = app
db.init_app(app)
