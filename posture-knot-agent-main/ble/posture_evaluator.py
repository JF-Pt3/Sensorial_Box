import math


class PostureEvaluator:

    def __init__(self, threshold, client, topic, vibrator):
        self.__sensors_angle = [0, 0]
        self.__sensors_battery = [101, 101]
        self.__client = client
        self.__status = 0
        self.__threshold = threshold
        self.__topic = topic
        self.__sensor_battery_lowest = 101
        self.__vibrator = vibrator

    def __battery_percent(self, bat_raw):
        if bat_raw < 1090:
            bat_perc = 1
            return bat_perc
        if bat_raw == 1090:
            bat_perc = 5
            return bat_perc
        if (bat_raw > 1090) and (bat_raw < 1095):
            bat_perc = 7
            return bat_perc
        if bat_raw == 1095:
            bat_perc = 10
            return bat_perc

        if (bat_raw > 1095) and (bat_raw < 1100):
            bat_perc = 12
            return bat_perc
        if bat_raw == 1100:
            bat_perc = 15
            return bat_perc
        if (bat_raw > 1100) and (bat_raw < 1110):
            bat_perc = 17
            return bat_perc
        if bat_raw == 1110:
            bat_perc = 20
            return bat_perc

        if (bat_raw > 1110) and (bat_raw < 1120):
            bat_perc = 23
            return bat_perc
        if bat_raw == 1120:
            bat_perc = 25
            return bat_perc
        if (bat_raw > 1120) and (bat_raw < 1131):
            bat_perc = 28
            return bat_perc
        if bat_raw == 1131:
            bat_perc = 30
            return bat_perc

        if (bat_raw > 1131) and (bat_raw < 1145):
            bat_perc = 32
            return bat_perc
        if bat_raw == 1145:
            bat_perc = 35
            return bat_perc
        if (bat_raw > 1145) and (bat_raw < 1160):
            bat_perc = 38
            return bat_perc
        if bat_raw == 1160:
            bat_perc = 40
            return bat_perc

        if (bat_raw > 1160) and (bat_raw < 1180):
            bat_perc = 43
            return bat_perc
        if bat_raw == 1180:
            bat_perc = 45
            return bat_perc
        if (bat_raw > 1180) and (bat_raw < 1204):
            bat_perc = 47
            return bat_perc
        if bat_raw == 1204:
            bat_perc = 50
            return bat_perc

        if (bat_raw > 1204) and (bat_raw < 1228):
            bat_perc = 53
            return bat_perc
        if bat_raw == 1228:
            bat_perc = 55
            return bat_perc
        if (bat_raw > 1228) and (bat_raw < 1252):
            bat_perc = 57
            return bat_perc
        if bat_raw == 1252:
            bat_perc = 60
            return bat_perc

        if (bat_raw > 1252) and (bat_raw < 1267):
            bat_perc = 63
            return bat_perc
        if bat_raw == 1267:
            bat_perc = 65
            return bat_perc
        if (bat_raw > 1267) and (bat_raw < 1283):
            bat_perc = 67
            return bat_perc
        if bat_raw == 1283:
            bat_perc = 70
            return bat_perc

        if (bat_raw > 1283) and (bat_raw < 1296):
            bat_perc = 73
            return bat_perc
        if bat_raw == 1296:
            bat_perc = 75
            return bat_perc
        if (bat_raw > 1296) and (bat_raw < 1309):
            bat_perc = 77
            return bat_perc
        if bat_raw == 1309:
            bat_perc = 80
            return bat_perc

        if (bat_raw > 1309) and (bat_raw < 1320):
            bat_perc = 83
            return bat_perc
        if bat_raw == 1320:
            bat_perc = 85
            return bat_perc
        if (bat_raw > 1320) and (bat_raw < 1333):
            bat_perc = 87
            return bat_perc
        if bat_raw == 1333:
            bat_perc = 90
            return bat_perc

        if (bat_raw > 1333) and (bat_raw < 1370):
            bat_perc = 93
            return bat_perc
        if bat_raw == 1370:
            bat_perc = 95
            return bat_perc
        if (bat_raw > 1370) and (bat_raw < 1400):
            bat_perc = 97
            return bat_perc
        if (bat_raw == 1400) or (bat_raw > 1400):
            bat_perc = 100
            return bat_perc

    def post(self, sensor_number, angle):
        self.__sensors_angle[sensor_number] = angle

        #print(sensor_number, angle)

        if abs(self.__sensors_angle[0] - self.__sensors_angle[1]) < self.__threshold:
            status = 1
        else:
            status = 0

        if self.__status != status:
            #print(self.__topic + "/posture", status)
            self.__status = status
            self.__client.publish(self.__topic + "/posture", status)
            self.__vibrator.vibrate(status)

    def postBatt(self, sensor_number, battery_raw):
        battery = self.__battery_percent(battery_raw)
        #print(str(sensor_number), str(battery))
        self.__sensors_battery[sensor_number] = battery

        lowest = min(self.__sensors_battery)
        
        if lowest != self.__sensor_battery_lowest:
            #print(self.__topic + "/battery", battery)
            self.__sensor_battery_lowest = lowest
            self.__client.publish(self.__topic + "/battery", battery)