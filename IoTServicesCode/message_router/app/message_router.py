import time
import paho.mqtt.client as paho
from measurement_register_interface import *
from device_register_interface import *
from datetime import datetime
import os
import json

# global vars definition
current_temperature=0
current_humidity=0

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected success")
        client.subscribe("/uc3m/classrooms/leganes/myclass/temperature")
        client.subscribe("/uc3m/classrooms/leganes/myclass/humidity")
        client.subscribe("/uc3m/classrooms/leganes/myclass/device_info")
        client.subscribe('/uc3m/classrooms/leganes/myclass/disconnect')
    else:
        print("Connected fail with code", {rc})


# define mqtt callback
def on_message(client, userdata, message):
    global current_temperature, current_humidity
    print("received message =",str(message.payload.decode("utf-8")))
    if message.topic == "/uc3m/classrooms/leganes/myclass/temperature":
        r = message.payload.decode("utf-8")
        params = eval(r)
        current_temperature = params['temperature']
        device_id = params['device_id']
        data = {"temperature": current_temperature, "humidity": current_humidity,
                "date_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), "device_id": device_id}
        submit_data_to_store(data)
        print(data)
    if message.topic == "/uc3m/classrooms/leganes/myclass/humidity":
        r = message.payload.decode("utf-8")
        params = eval(r)
        current_humidity = params['humidity']
        device_id = params['device_id']
        data = {"temperature": current_temperature, "humidity": current_humidity,
                "date_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), "device_id": device_id}
        submit_data_to_store(data)
        print(data)
    if message.topic == "/uc3m/classrooms/leganes/myclass/device_info":
        r = message.payload.decode("utf-8")
        data = eval(r)
        submit_device_info_to_store(data)
        print(data)
    if message.topic == "/uc3m/classrooms/leganes/myclass/disconnect":
        r = message.payload.decode("utf-8")
        data = {"device_id": r}
        submit_device_disconnect_to_store(data)
        print(data)


# Create client object client1.on_publish = on_publish #assign function to callback client1.connect(broker,port) #establish connection client1.publish("house/bulb1","on")
myhost = os.getenv('BROKER_ADDRESS')
myport = int(os.getenv('BROKER_PORT'))
myuser = os.getenv('BROKER_USER')
mypassword = os.getenv('BROKER_PWD')
mykeepalive = int(os.getenv('BROKER_KEEP_ALIVE'))
client=paho.Client()
client.username_pw_set(username=myuser, password=mypassword)
client.on_connect = on_connect
# Bind function to callback
client.on_message=on_message
# Initializate cursor instance
print("connecting to broker ",myhost)
client.connect(myhost, 1883, mykeepalive) # connect
# Start loop to process received messages
client.loop_forever()
