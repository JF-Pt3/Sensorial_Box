import datetime
import math
from bluepy import btle


class PostureMessageHandler(btle.DefaultDelegate):

    def __init__(self, addr, evaluator, sensor_number):
        btle.DefaultDelegate.__init__(self)

        self.__addr = addr
        self.__evaluator = evaluator
        self.__sensor_number = sensor_number

    def handleNotification(self, cHandle, data):
        if cHandle == 36:
            acc_adjust = 4.0 / 32767

            accX = ((data[2 * 0 + 3] & 0xff) << 8) | (data[2 * 0 + 2] & 0xff)
      
            if accX > 32767:
                accX = -(65534 - accX)
            
            accX *= acc_adjust

            accY = ((data[2 * 1 + 3] & 0xff) << 8) | (data[2 * 1 + 2] & 0xff)
    
            if accY > 32767:
                accY = -(65534 - accY)
            
            accY *= acc_adjust

            accZ = ((data[2 * 2 + 3] & 0xff) << 8) | (data[2 * 2 + 2] & 0xff)
            
            if accZ > 32767:
                accZ = -(65534 - accZ) 
            
            accZ *= acc_adjust

            normalizeOfG = math.sqrt(accX * accX + accY * accY + accZ * accZ)

            accY = accY / normalizeOfG

            yInclination = math.acos(accY) * (180 / math.pi)

            self.__evaluator.post(self.__sensor_number, yInclination)
