import paho.mqtt.client as mqtt
import time
from threading import Thread
import board
import adafruit_veml7700

pollingInterval = 5

def task_environ_send_data():
    i2c = board.I2C()  # uses board.SCL and board.SDA
    veml7700 = adafruit_veml7700.VEML7700(i2c)

    while True:
       ambient_light = str(round(veml7700.lux,2))
       client.publish("stream/veml7700/illuminance", ambient_light)
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