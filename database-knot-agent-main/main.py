from configparser import NoSectionError
import mysql.connector as database
from datetime import datetime
import paho.mqtt.client as mqtt
import time
from threading import Thread

global temperatureVals
global humidityVals
global airQualityVals
global noiseVals  
global illuminanceVals
global pressureVals

pollingInterval = 60
temperatureVals = []
humidityVals = []
airQualityVals = []
noiseVals = []
illuminanceVals = []
pressureVals = []

def send_data():
    while True:
        time.sleep(pollingInterval)
        connection = database.connect(
            user="sersorsProject",
            password="sersorsProject",
            host="127.0.0.1",
            database="sersorsProject") 
        cursor = connection.cursor()
        add_data(cursor, "temperature", temperatureVals)
        add_data(cursor, "humidity", humidityVals)
        add_data(cursor, "airquality", airQualityVals)
        add_data(cursor, "noise", noiseVals)
        add_data(cursor, "pressure", pressureVals)
        add_data(cursor, "illuminance", illuminanceVals)
        connection.commit()
        connection.close()
        temperatureVals.clear()
        humidityVals.clear()
        airQualityVals.clear()
        noiseVals.clear()
        illuminanceVals.clear()
        pressureVals.clear()

def add_data(cursor, table, values_measured):
    try:
        statement = "INSERT INTO "+ str(table)+" (value, timestamp, sensor) VALUES (%s, %s, %s)"
        cursor.executemany(statement, values_measured)
        #print("Successfully added entry to database")
    except database.Error as e:
        print(f"Error adding entry to database: {e}")

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))  
    client.subscribe("stream/dht11/temperature")
    client.subscribe("stream/dht11/humidity")
    client.subscribe("stream/veml7700/illuminance2")
    client.subscribe("stream/bmp280/temperature")
    client.subscribe("stream/bmp280/pressure")        
    client.subscribe("stream/adcpi/air-quality")
    client.subscribe("stream/adcpi/noise")    
    client.subscribe("stream/aqara/temperature")
    client.subscribe("stream/aqara/humidity")
    client.subscribe("stream/aqara/pressure")
    
def on_message(client, userdata, msg): 
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

    if msg.topic == "stream/dht11/temperature":
        temp = msg.payload.decode("utf-8")
        temperatureVals.append((str(temp), dt_string, "dht11"))
    
    elif msg.topic == "stream/dht11/humidity":
        temp = msg.payload.decode("utf-8")
        humidityVals.append((str(temp), dt_string, "dht11"))    

    elif msg.topic == "stream/veml7700/illuminance":
        temp = msg.payload.decode("utf-8")
        illuminanceVals.append((str(temp), dt_string, "veml7700"))
        
    elif msg.topic == "stream/bmp280/temperature":
        temp = msg.payload.decode("utf-8")
        temperatureVals.append((str(temp), dt_string, "bmp280"))

    elif msg.topic == "stream/bmp280/pressure":
        temp = msg.payload.decode("utf-8")
        pressureVals.append((str(temp), dt_string, "bmp280")) 

    elif msg.topic == "stream/adcpi/air-quality":
        temp = msg.payload.decode("utf-8")
        airQualityVals.append((str(temp), dt_string, "adcpi"))

    elif msg.topic == "stream/adcpi/noise":
        temp = msg.payload.decode("utf-8")
        noiseVals.append((str(temp), dt_string, "adcpi"))           

    elif msg.topic == "stream/aqara/temperature":
        temp = msg.payload.decode("utf-8")
        temperatureVals.append((str(temp), dt_string, "aqara"))             

    elif msg.topic == "stream/aqara/humidity":
        temp = msg.payload.decode("utf-8")
        humidityVals.append((str(temp), dt_string, "aqara"))

    elif msg.topic == "stream/aqara/pressure":
        temp = msg.payload.decode("utf-8")
        pressureVals.append((str(temp), dt_string, "aqara"))                               

task_send_data = Thread(target = send_data)
task_send_data.start()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
 
client.connect("127.0.0.1", 1883, 60)

client.loop_forever()
