import paho.mqtt.client as mqtt
import time
import uuid

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected success")
    else:
        print("Connected fail with code", {rc})

client = mqtt.Client()

def make_connection():
    client.username_pw_set(username="dso_server", password="dso_password")
    client.on_connect = on_connect
    id = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                   for ele in range(0, 8 * 6, 8)][::-1])
    id += " - Raspberry 1"
    # Last will message
    client.will_set('/uc3m/classrooms/leganes/myclass/disconnect', id, 0, False)
    client.connect("104.199.84.188", 1883, 60)

def send_temperature_humidity(temperature, humidity):
    # the four parameters are topic, sending content, QoS and whether retaining the message respectively
    client.publish('/uc3m/classrooms/leganes/myclass/temperature', payload=temperature, qos=0, retain=False)
    time.sleep(1)

def send_temperature(temperature):
    # the four parameters are topic, sending content, QoS and whether retaining the message respectively
    client.publish('/uc3m/classrooms/leganes/myclass/temperature', payload=temperature, qos=0, retain=False)
    time.sleep(1)

def send_humidity(humidity):
    # the four parameters are topic, sending content, QoS and whether retaining the message respectively
    client.publish('/uc3m/classrooms/leganes/myclass/humidity', payload=humidity, qos=0, retain=False)
    time.sleep(1)

def send_time(time):
    # the four parameters are topic, sending content, QoS and whether retaining the message respectively
    client.publish('/uc3m/classrooms/leganes/myclass/time', payload=time, qos=0, retain=False)
    time.sleep(1)

def send_id(id):
    # the four parameters are topic, sending content, QoS and whether retaining the message respectively
    client.publish('/uc3m/classrooms/leganes/myclass/device_info', payload=id, qos=0, retain=False)
    time.sleep(1)
