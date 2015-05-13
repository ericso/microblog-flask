from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

# Put views import after app creation to avoid circular import
from app import views
