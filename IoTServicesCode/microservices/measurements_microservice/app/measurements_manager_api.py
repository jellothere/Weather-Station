from flask import Flask, request
from flask_cors import CORS
import os

from measurements_manager import *

app = Flask(__name__)
CORS(app)

@app.route('/measurements/register/', methods=['POST'])
def set_measurement():
    params = request.get_json()
    measurements_register(params)
    return {"result":"record inserted"}, 201

@app.route('/measurements/retrieve/')
def get_measurements():
    params = request.get_json()
    return measurements_retriever(params)

host = os.getenv('HOST')
port = os.getenv('PORT')
app.run(host=host, port=port)
