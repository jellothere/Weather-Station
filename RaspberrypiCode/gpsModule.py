from publisher import *
import uuid
import pynmea2
import serial
import time
from datetime import datetime
#export PYTHONPATH=~/sesion10/utils/


def locationID():
    make_connection()
    while True:
        port = "/dev/ttyAMA0"
        ser = serial.Serial(port, baudrate=9600, timeout=0.5)
        dataout = pynmea2.NMEAStreamReader()
        newdata = ser.readline()
        # Filtering for the right line in the data from the GPS
        if newdata[0:6] == "$GPRMC":
            newmsg = pynmea2.parse(newdata)
            lat = newmsg.latitude
            lng = newmsg.longitude
            latitude = str(lat)
            longitude = str(lng)
            # For debugging purposes
            print(latitude)
            print(longitude)
            id = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                           for ele in range(0,8*6,8)][::-1])
            id += " - Raspberry 1"
            data = {"device_id": id, "latitude": latitude,
                    "longitude": longitude, "date_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}
            send_id(str(data))
            # Every hour
            time.sleep(60*60)

if __name__ == "__main__":
    locationID()