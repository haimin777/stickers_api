import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "db/flask-api.db"))

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)

'''
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')
'''

from app.module.controller import *