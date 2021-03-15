
# import flask modules
from flask import Flask
import urllib.parse

# import blueprints
from auth import auth_bp

# import db:
from dal import db

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

# extensions
db.app = app
db.init_app(app)

# register blueprints
app.register_blueprint(auth_bp)
