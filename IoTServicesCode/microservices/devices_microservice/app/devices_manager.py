import mysql.connector
import os
import json

def connect_database ():
    mydb = mysql.connector.connect(
        host = os.getenv('DBHOST'),
        user = os.getenv('DBUSER'),
        password = os.getenv('DBPASSWORD'),
        database = os.getenv('DBDATABASE')
    )
    return mydb

def devices_retriever():
    mydb = connect_database()
    r = []
    with mydb.cursor() as mycursor:
        mycursor.execute("SELECT device_id, status, latitude, longitude, date_time FROM devices;")
        myresult = mycursor.fetchall()
        for device_id, status, latitude, longitude, date_time in myresult:
            r.append({"device_id": device_id, "status": status, "latitude": latitude, "longitude": longitude, "date_time": date_time.strftime('%Y-%m-%d, %H:%M:%S.%f')[:-7]})
        mydb.commit()
    result = json.dumps(r, sort_keys=True)
    return result

def devices_regiter(params):
    mydb = connect_database()
    with mydb.cursor() as mycursor:
        sql = "REPLACE INTO devices (device_id,status, latitude, longitude) VALUES (%s, %s, %s, %s);"
        val = (params['device_id'], "ACTIVE", params['latitude'], params['longitude'])
        print(val)
        try:
            mycursor.execute(sql, val)
            mydb.commit()
        except:
            print("Error registering the device")

def device_disconnnect(params):
    mydb = connect_database()
    with mydb.cursor() as mycursor:
        sql = "UPDATE devices SET status = %s WHERE device_id = %s;"
        val = ('INACTIVE', params["device_id"])
        try:
            mycursor.execute(sql, val)
            mydb.commit()
        except:
            print("Error disconnecting the device")
