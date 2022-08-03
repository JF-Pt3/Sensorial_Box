import paho.mqtt.client as mqtt
import time
from threading import Thread
import board
import adafruit_dht as dht

pollingInterval = 5

def task_environ_send_data():
    dhtDevice = dht.DHT11(board.D18)

    while True:
        try:
            # Print the values to the serial port
            temperature_c = dhtDevice.temperature
            humidity = dhtDevice.humidity
            client.publish("stream/dht11/temperature", temperature_c)
            client.publish("stream/dht11/humidity", humidity)
        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
            time.sleep(2.0)
            continue
        except Exception as error:
            dhtDevice.exit()
            raise error

        time.sleep(pollingInterval)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

task_read_ambient_sensors = Thread(target = task_environ_send_data)
task_read_ambient_sensors.start()

# Create an MQTT client and attach our routines to it.
client = mqtt.Client()
client.on_connect = on_connect
#client.on_message = on_message

client.connect("127.0.0.1", 1883, 60)

# Process network traffic and dispatch callbacks. This will also handle
# reconnecting. Check the documentation at
# https://github.com/eclipse/paho.mqtt.python
# for information on how to use other loop*() functions
client.loop_forever()