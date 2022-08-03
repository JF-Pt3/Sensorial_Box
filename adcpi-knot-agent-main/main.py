import paho.mqtt.client as mqtt
import math
import time
from datetime import datetime
from threading import Thread
import time
from ADCPi import ADCPi

pollingInterval = 5.
adc = ADCPi(0x6a, 0x6b, 18)
global tempDht11
tempDht11 = 25
global humDht11
humDht11 = 50

class MQ135(object):
    """ Class for dealing with MQ13 Gas Sensors """
    # The load resistance on the board
    RLOAD = 1.0
    # Calibration resistance at atmospheric CO2 level
    RZERO = 69.50
    # Parameters for calculating ppm of CO2 from sensor resistance
    PARA = 116.6020682
    PARB = 2.769034857

    # Parameters to model temperature and humidity dependence
    CORA = 0.00035
    CORB = 0.02718
    CORC = 1.39538
    CORD = 0.0018
    CORE = -0.003333333
    CORF = -0.001923077
    CORG = 1.130128205

    # Atmospheric CO2 level for calibration purposes
    ATMOCO2 = 414.47

    def __init__(self, pin):
        self.pin = pin

    def get_correction_factor(self, temperature, humidity):
        """Calculates the correction factor for ambient air temperature and relative humidity
        Based on the linearization of the temperature dependency curve
        under and above 20 degrees Celsius, asuming a linear dependency on humidity,
        provided by Balk77 https://github.com/GeorgK/MQ135/pull/6/files
        """

        if temperature < 20:
            return self.CORA * temperature * temperature - self.CORB * temperature + self.CORC - (humidity - 33.) * self.CORD

        return self.CORE * temperature + self.CORF * humidity + self.CORG

    def get_resistance(self):
        """Returns the resistance of the sensor in kOhms // -1 if not value got in pin"""
        value = adc.read_raw(self.pin)
        if value == 0:
            return -1

        return (262143./value - 1.) * self.RLOAD

    def get_corrected_resistance(self, temperature, humidity):
        """Gets the resistance of the sensor corrected for temperature/humidity"""
        return self.get_resistance()/ self.get_correction_factor(temperature, humidity)

    def get_ppm(self):
        """Returns the ppm of CO2 sensed (assuming only CO2 in the air)"""
        return self.PARA * math.pow((self.get_resistance()/ self.RZERO), -self.PARB)

    def get_corrected_ppm(self, temperature, humidity):
        """Returns the ppm of CO2 sensed (assuming only CO2 in the air)
        corrected for temperature/humidity"""
        return self.PARA * math.pow((self.get_corrected_resistance(temperature, humidity)/ self.RZERO), -self.PARB)

    def get_rzero(self):
        """Returns the resistance RZero of the sensor (in kOhms) for calibration purposes"""
        return self.get_resistance() * math.pow((self.ATMOCO2/self.PARA), (1./self.PARB))

    def get_corrected_rzero(self, temperature, humidity):
        """Returns the resistance RZero of the sensor (in kOhms) for calibration purposes
        corrected for temperature/humidity"""
        return self.get_corrected_resistance(temperature, humidity) * math.pow((self.ATMOCO2/self.PARA), (1./self.PARB))

def task_adc():
    mq135 = MQ135(1)
    ref_SPL = 94
    sensitivity = 3.16
    while True:
        #resistor = mq135.get_corrected_rzero(tempDht11, humDht11) 
        #print(str(resistor))
        ppm = mq135.get_corrected_ppm(tempDht11, humDht11)
        ppm_str = str(round(ppm,2))
        client.publish("stream/adcpi/air-quality", ppm_str)   
        
        samples = 16
        tmp = 0                
        while samples > 0:
            rms = adc.read_voltage(2)
            tmp += (rms*rms)
            samples -= 1
            time.sleep(pollingInterval/16.)
        rms = math.sqrt(tmp/2)
        db_current = ref_SPL+20*math.log10(rms/sensitivity)
        db_current_str = str(round(db_current,2))
        client.publish("stream/adcpi/noise", db_current_str)
               
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    
    client.subscribe("stream/dht11/temperature")
    client.subscribe("stream/dht11/humidity")
    
def on_message(client, userdata, msg):
    if msg.topic == "stream/dht11/temperature":
        tempStr = msg.payload.decode("utf-8")
        tempDht11 = float(tempStr)
    elif msg.topic == "stream/dht11/humidity":
        humStr = msg.payload.decode("utf-8")
        humDht11 = float(humStr)
           
# Create an MQTT client and attach our routines to it.
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("127.0.0.1", 1883, 60)

task_read_adc = Thread(target = task_adc)
task_read_adc.start()

# Process network traffic and dispatch callbacks. This will also handle
# reconnecting. Check the documentation at
# https://github.com/eclipse/paho.mqtt.python
# for information on how to use other loop*() functions
client.loop_forever()