import adafruit_dht
from publisher import *
import uuid
import threading
import board
import drivers
from time import sleep
import sys
import RPi.GPIO as GPIO
import signal
#export PYTHONPATH=~/sesion10/utils/
display = drivers.Lcd()
BUTTON_GPIO = 16
mode = True
newhumidity = 0
newtemperature = 0



def temperatureSensor():
    DHT_PIN = board.D4
    DHT_SENSOR = adafruit_dht.DHT11(DHT_PIN, use_pulseio=False)
    newtemperature = 0
    while True:
        temperature = DHT_SENSOR.temperature
        if temperature is not None:
            if(newtemperature != temperature):
                newtemperature = temperature
                send_temperature(temperature)
            print("Temp={0:0.1f}C ".format(temperature))
        else:
            print("Sensor failure. Check wiring.")
        time.sleep(3)

def button_released_callback(channel):
    global mode
    global newhumidity
    global newtemperature
    print("\n CHANGING LCD INFO: \n")
    print(" ----------------------- \n")
    mode = not mode
    display.lcd_clear()
    if mode == 1:
        display.lcd_display_string("Humidity: " + str(newhumidity)+"%", 1)  # Write line of text to first line of display
    else:
        display.lcd_display_string("Temperature: " + str(newtemperature)+ "C", 1)  # Second line of display

def signal_handler(sig, frame):
    display.lcd_clear()
    sys.exit(0)


def temperatureHumiditySensor():
    global newhumidity
    global newtemperature
    DHT_PIN = board.D4
    DHT_SENSOR = adafruit_dht.DHT11(DHT_PIN, use_pulseio=False)
    id = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                   for ele in range(0, 8 * 6, 8)][::-1])
    id += " - Raspberry 2"
    while True:
        # Displaying error in the sensor
        try:
            humidity = DHT_SENSOR.humidity
            temperature = DHT_SENSOR.temperature
        except:
            display.lcd_display_string("Error in the sensor measurement, please restart the device.", 1)
        if humidity is not None:
            if(newhumidity != humidity):
                newhumidity = humidity
                data = {"humidity": humidity, "device_id": id}
                send_humidity(str(data))
                if mode == 1:
                    display.lcd_display_string("Humidity: "+str(newhumidity)+"%", 1)  # Write line of text to first line of display
            print("Hum={0:0.1f}C ".format(humidity))
        else:
            print("Sensor failure. Check wiring.")
        if temperature is not None:
            if(newtemperature != temperature):
                newtemperature = temperature
                data = {"temperature": temperature, "device_id": id}
                send_temperature(str(data))
                if mode == 0:
                    display.lcd_display_string("Temperature: " + str(newtemperature) + "C", 1)  # Second line of display
            print("Temp={0:0.1f}C ".format(temperature))
        else:
            print("Sensor failure. Check wiring.")
        # Every minute
        time.sleep(60)


if __name__ == "__main__":
    make_connection()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BUTTON_GPIO, GPIO.RISING, callback = button_released_callback, bouncetime=200)
    signal.signal(signal.SIGINT, signal_handler)
    temperatureHumidity = threading.Thread(target=temperatureHumiditySensor)
    send_id(0)
    temperatureHumidity.start()




