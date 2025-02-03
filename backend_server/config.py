from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)   # om de app te initialiseren
CORS(app)       # laat ons cross origin requests sturen

"""
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///school_agenda.db"   # maken de locatie van de database aan
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False    # we gaan de modificaties van de database niet tracken

db = SQLAlchemy(app)    # om toegang te krijgen tot de database (mydatabase.db)
"""