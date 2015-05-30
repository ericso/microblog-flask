import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID

from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView

from flask.ext.mail import Mail
from flask.ext.babel import Babel

from config import (
  basedir,
  ADMINS,
  MAIL_SERVER,
  MAIL_PORT,
  MAIL_USERNAME,
  MAIL_PASSWORD,
)

from app.momentjs import momentjs


app = Flask(__name__)
app.config.from_object('config')

# Localization
babel = Babel(app)

# Email
mail = Mail(app)

# Database
db = SQLAlchemy(app)

# User Login
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))

# Admin interface
admin = Admin(app)

# Logging
if not app.debug:
  import logging
  from logging.handlers import SMTPHandler, RotatingFileHandler

  # Email Logging
  credentials = None
  if MAIL_USERNAME or MAIL_PASSWORD:
    credentials = (MAIL_USERNAME, MAIL_PASSWORD)
  mail_handler = SMTPHandler(
    (MAIL_SERVER, MAIL_PORT),
    'no-reply@' + MAIL_SERVER,
    ADMINS,
    'microblog failure',
    credentials
  )
  mail_handler.setLevel(logging.ERROR)
  app.logger.addHandler(mail_handler)

  # File Logging
  file_handler = RotatingFileHandler(
    'tmp/microblog.log',
    'a',
    1 * 1024 * 1024, # 10 MB log size
    10 # Keep last 10 log files
  )
  file_handler.setFormatter(
    logging.Formatter(
      '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    )
  )
  app.logger.setLevel(logging.INFO)
  file_handler.setLevel(logging.INFO)
  app.logger.addHandler(file_handler)
  app.logger.info('microblog startup')

# Templating
app.jinja_env.globals['momentjs'] = momentjs


# Put views import after app creation to avoid circular import
from app import views, models


# Add admin views
admin.add_view(ModelView(models.User, db.session))
admin.add_view(ModelView(models.Post, db.session))
