from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "dqlmjdfqlkdjfm"
CORS(app)

# Configure the Flask app to use a database URI
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///weatherData.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_BINDS"] = {
    'unique_icons': 'sqlite:///unique_icons.sqlite3',
    'dayWeather': 'sqlite:///dayWeather.sqlite3',
    'preFetch': 'sqlite:///preFetch.sqlite3',
    'week_data': 'sqlite:///week_data.sqlite3'
}

# Initialize SQLAlchemy with Flask
db = SQLAlchemy(app)
