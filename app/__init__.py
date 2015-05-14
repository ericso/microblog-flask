import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID

from config import basedir


app = Flask(__name__)
app.config.from_object('config')

# Database
db = SQLAlchemy(app)

# User Login
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))

# Put views import after app creation to avoid circular import
from app import views, models
