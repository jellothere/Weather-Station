import mysql.connector
import os
import json

def connect_database ():
    mydb = mysql.connector.connect(
        host=os.getenv("DBHOST"),
        user=os.getenv("DBUSER"),
        password=os.getenv("DBPASSWORD"),
        database=os.getenv("DBDATABASE")
    )
    return mydb

def measurements_retriever(params):
    mydb = connect_database()
    r = []
    print(params)
    params = eval(params)
    print(params)
    with mydb.cursor() as mycursor:
        sql = "SELECT temperature, humidity, date_time, device_id FROM sensor_data WHERE device_id = %s AND unix_timestamp(date_time) >= %s AND unix_timestamp(date_time) <= %s ORDER BY id DESC;"
        val = (params["device_id"], params["start"], params["end"])
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        for temperature, humidity, date_time, device_id in myresult:
            r.append({"temperature": temperature, "humidity": humidity, "date_time": date_time.strftime('%Y-%m-%d, %H:%M:%S.%f')[:-7],
                      "device_id": device_id})
        mydb.commit()
    result = json.dumps(r, sort_keys=True)
    return result

def measurements_register(params):
    mydb = connect_database()
    with mydb.cursor() as mycursor:
        sql = "INSERT INTO sensor_data (temperature, humidity, date_time, device_id) VALUES (%s, %s, %s, %s)"
        val = (params["temperature"], params["humidity"], params["date_time"], params['device_id'])
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
