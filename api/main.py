
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  

@app.route('/')
def flask_route():
    return 'Hello from Flask!'