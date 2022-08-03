from threading import Thread
from ble import PostureFusion
from paho.mqtt.client import Client
import sys

if (len(sys.argv) != 4):
    print("Better check your arguments buddy.")
    exit()

peripheral1 = sys.argv[1]
peripheral2 = sys.argv[2]
name = sys.argv[3]

def on_connect(client, userdata, flags, rc):
    fusion = PostureFusion(peripheral1, peripheral2, name, client, 21)

    ft = Thread(target=fusion.start)
    ft.start()

if __name__ == '__main__':
    client = Client()
    client.on_connect = on_connect

    client.connect("localhost")
    client.loop_forever()
