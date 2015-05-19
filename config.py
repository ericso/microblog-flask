import os


basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

OPENID_PROVIDERS = [
  {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
  {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
  {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
  {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}
]

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# Mail server settings
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None

# Administrator list
ADMINS = ['you@example.com']

# Pagination
POSTS_PER_PAGE = 3

# Whoosh Full Text Search
WHOOSH_BASE = os.path.join(basedir, 'search.db')
MAX_SEARCH_RESULTS = 50
