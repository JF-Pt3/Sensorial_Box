import paho.mqtt.client as mqtt
import time
from threading import Thread
import board
import adafruit_bmp280

pollingInterval = 5

def task_environ_send_data():
    i2c = board.I2C()  # uses board.SCL and board.SDA
    bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

    while True:
       temperature = str(round(bmp280.temperature,2))
       client.publish("stream/bmp280/temperature", temperature)
       pressure = str(round(bmp280.pressure,2))
       client.publish("stream/bmp280/pressure", pressure)       
       time.sleep(pollingInterval)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

task_read_ambient_sensors = Thread(target = task_environ_send_data)
task_read_ambient_sensors.start()

# Create an MQTT client and attach our routines to it.
client = mqtt.Client()
client.on_connect = on_connect

client.connect("127.0.0.1", 1883, 60)

# Process network traffic and dispatch callbacks. This will also handle
# reconnecting. Check the documentation at
# https://github.com/eclipse/paho.mqtt.python
# for information on how to use other loop*() functions
client.loop_forever()