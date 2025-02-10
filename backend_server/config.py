from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)   # om de app te initialiseren
CORS(app)       # laat ons cross origin requests sturen

"""
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///weatherData.db"   # maken de locatie van de database aan
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False    # we gaan de modificaties van de database niet tracken
app.config["SQLALCHEMY_BINDS"] = {
    'unique_icons': 'sqlite:///unique_icons.db'     # maakt een extra database voor de icons
}

db = SQLAlchemy(app)    # om toegang te krijgen tot de database (mydatabase.db)
"""