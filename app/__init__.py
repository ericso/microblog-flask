from flask import Flask

app = Flask(__name__)

# Put views import after app creation to avoid circular import
from app import views
