from threading import Thread
from time import sleep
from bluepy import btle

from .posture_message_handler import PostureMessageHandler


class PosturePeripheral:

    UUID_SERVICE_DATA = "0000ff30-0000-1000-8000-00805f9b34fb"
    UUID_CHARACTERISTIC_ACCELEROMETER = "0000ff35-0000-1000-8000-00805f9b34fb"
    UUID_CHARACTERISTIC_BATTERY = "0000ff36-0000-1000-8000-00805f9b34fb"
    
    STREAM_ACCY = 1
    STREAM_BATTERY = 2

    def __init__(self, addr, evaluator, sensor_number):
        self.__addr = addr
        self.__dev = None
        self.__evaluator = evaluator
        self.__sensor_number = sensor_number
        self.__batt_char = None
        self.__batt_thread = None
        self.__read_battery = True
        self.__toggle_vibrate = False
        self.__vibrate = False

    def __batt(self):
        while self.__running:
            self.__read_battery = True
            sleep(60)

    def connect(self):
        print("Connecting", self.__addr, "...")
        try:
            self.__dev = btle.Peripheral(self.__addr)
            self.__dev.setDelegate(PostureMessageHandler(self.__addr, self.__evaluator, self.__sensor_number))

            acc_service = self.__dev.getServiceByUUID(btle.UUID(PosturePeripheral.UUID_SERVICE_DATA))
            acc_characteristic = acc_service.getCharacteristics(btle.UUID(PosturePeripheral.UUID_CHARACTERISTIC_ACCELEROMETER))[0]
            self.__batt_char = acc_service.getCharacteristics(btle.UUID(PosturePeripheral.UUID_CHARACTERISTIC_BATTERY))[0]

            self.__running = True
            self.__batt_thread = Thread(target= self.__batt)
            self.__batt_thread.start()

            sleep(1)

            acc_characteristic.write(bytes('\x08', encoding='utf-8'))
            acc_characteristic.write(bytes('\x01', encoding='utf-8'))

            while self.__dev.waitForNotifications(5):
                if self.__read_battery:
                    self.__read_battery = False
                    val = self.__batt_char.read()
                    self.__evaluator.postBatt(self.__sensor_number, (val[1] & 0xff) << 8 | (val[0] & 0xff))
            
                if self.__toggle_vibrate:
                    self.__vibrate = not self.__vibrate
                    
                    if self.__vibrate:
                        #print("vibrate")
                        acc_characteristic.write(bytes('\x07', encoding='utf-8'))
                    else:
                        #print("no vibrate")
                        acc_characteristic.write(bytes('\x08', encoding='utf-8'))

                    self.__toggle_vibrate = False

                continue

            self.disconnect()

        except Exception as e:
            print(e)
            self.disconnect()

    def vibrate(self, status):
        #print("vibrate", self.__addr, status, self.__vibrate)
        if (status == 0 and not self.__vibrate) or (status == 1 and self.__vibrate):
            self.__toggle_vibrate = True
        else:
            self.__toggle_vibrate = False

    def disconnect(self):
        self.__running = False

        if self.__dev is not None and self.__dev.status:
            try:
                self.__dev.disconnect()
            except:
                sleep(0)

        if self.__batt_thread is not None and self.__batt_thread.is_alive():
            self.__batt_thread.join()
