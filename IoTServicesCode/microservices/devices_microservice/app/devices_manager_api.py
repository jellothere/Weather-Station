from flask import Flask, request
from flask_cors import CORS
import os
from devices_manager import *

app = Flask(__name__)
CORS(app)


@app.route('/devices/register/', methods=['POST'])
def save_deviceinfo():
    params = request.get_json()
    devices_regiter(params)
    return {"result": "record inserted"}, 201


@app.route('/devices/retrieve/')
def retrieve_devices():
    return devices_retriever()


@app.route('/devices/disconnect/', methods=['POST'])
def disconnect_device():
    params = request.get_json()
    device_disconnnect(params)
    return {"result": "record changed"}, 201


HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
app.run(host=HOST, port=PORT)
