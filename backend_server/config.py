from flask import Flask
from flask_cors import CORS

app = Flask(__name__)   # om de app te initialiseren
CORS(app)       # laat ons cross origin requests sturen

