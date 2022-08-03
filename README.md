# sersorsProject Rapsberry OS Preparation

First you need to install the 32 bit version of the Raspberry Pi OS. Make sure it is up to date:


```
sudo apt update
sudo apt dist-upgrade -y
```

## Library Installation Process

#### Bluetooth libraries:

```bash
sudo apt-get install python3-pip libglib2.0-dev
sudo pip3 install bluepy
```

#### Mosquitto PAHO MQTT:

```bash
sudo pip3 install paho-mqtt
sudo apt update && sudo apt upgrade
sudo apt install -y mosquitto mosquitto-clients
sudo systemctl enable mosquitto.service
```
##### Then execute:

```bash
mosquitto -v 

should look something like this:
1657182040: mosquitto version 2.0.11 starting
1657182040: Using default config.
1657182040: Starting in local only mode. Connections will only be possible from clients running on this machine.
1657182040: Create a configuration file which defines a listener to allow remote access.
1657182040: For more details see https://mosquitto.org/documentation/authentication-methods/
1657182040: Opening ipv4 listen socket on port 1883.
1657182040: Error: Address already in use
1657182040: Opening ipv6 listen socket on port 1883.
1657182040: Error: Address already in use
```

##### Next in order to enable remote access:

```bash
Run the following:

sudo nano /etc/mosquitto/mosquitto.conf
```

##### Add the following to the file:

```bash
listener 1883
allow_anonymous true

Then: ctrl + x and option s or y (if in English)
```

##### For the changes to take effect:

```bash
sudo systemctl restart mosquitto

sudo systemctl status mosquitto.service
```

###### If the service reports as "active(running) in green, it means that everything is ok. Reboot the system

#### MARIADB INSTALLATION:

```bash
sudo apt-get install mariadb-server --fix-missing

sudo apt-get install mariadb-client

sudo mysql_secure_installation

"Enter current password for root (enter for none):" raspi123
```
###### The next questions answer all "n", until "Thanks for using MariaDB" appears

```bash
sudo mysql -u root -p

Password is: raspi123

To show all users:

SELECT User, Host FROM mysql.user;


Let's create a new user:

CREATE USER 'testuser'@'localhost' IDENTIFIED BY 'test123';

SELECT User, Host FROM mysql.user; ->>> check if the new user has been created

GRANT ALL PRIVILEGES ON *.* TO 'testuser'@'localhost';

show databases; ->>> Shows all databases

To create the sersorsProject database:

CREATE DATABASE sersorsProject;

show databases; ->>> check if the db was created successfully

use sersorsProject; ->>> Select the database

You then create the following tables:

CREATE TABLE Co2(value_measured FLOAT(8,4),last_update DATETIME);
CREATE TABLE Temperature(value_measured FLOAT(8,4),last_update DATETIME);
CREATE TABLE Humidity(value_measured FLOAT(8,4),last_update DATETIME);
CREATE TABLE Illuminance(value_measured FLOAT(8,4),last_update DATETIME);
CREATE TABLE Noise(value_measured FLOAT(8,4),last_update DATETIME);
CREATE TABLE Pressure(value_measured FLOAT(8,4),last_update DATETIME);
CREATE TABLE Teste(value_measured FLOAT(8,4),last_update DATETIME);

Verify that the tables were created successfully:

show tables;
```

#### Python <-> MariaDB connection
##### Next, in order to make the connection between python programs and MariaDB you need to install the following:

```bash
sudo pip3 install mysql-connector-python

```

#### Sensor installation:
##### Temperature/Humidity Sensor DHT11:

```bash
cd /home/pi

git clone https://github.com/adafruit/Adafruit_Python_DHT.git

cd Adafruit_Python_DHT

sudo apt-get install build-essential python-dev

sudo apt-get install python3-setuptools

sudo python3 setup.py install

```

##### Light Sensor veml7700

```bash
sudo pip3 install adafruit-circuitpython-veml7700

Then, in the terminal, execute:

sudo raspi-config

Interface-Options;

Activar o I2C

Selecionar Finish e fazer reboot

```

##### Both the Sound sensor and the co2 sensor require an external ADC, because the Raspberry Pi has no internal ADC:

```bash
cd /home/pi

git clone https://github.com/abelectronicsuk/ABElectronics_Python_Libraries.git

cd ABElectronics_Python_Libraries/

sudo python3 setup.py install

Then run :

i2cdetect -y 1

A table of the type should appear:

     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:                         -- -- -- -- -- -- -- -- 
10: 10 -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
60: -- -- -- -- -- -- -- -- -- -- 6a 6b -- -- -- -- 
70: -- -- -- -- -- -- -- --


Point out the active i2c addresses, in this case it is "6a" and "6b

```

#### Installation of Python's graphical modules:

```bash
sudo apt-get install python3-tk

sudo apt-get install python3-pil python3-pil.imagetk

```

#### Other required modules:

```bash
sudo pip3 install bson

The SPI protocol module must be enabled:

sudo raspi-config

Interface-Options;

Activate SPI

Select Finish and reboot

```

### CREATE SERVICES AT RASPBERRY PI BOOT

```bash

You need to go to the program folder and execute in the terminal the following command over the launch.command file:

chmod u+x /home/pi/Desktop/sersorsProject/launch.command
We will have 2 services:

1) client.service is the service that allows you to automatically start the backend

2) sersorsProject_db.service Database service, which listens for mqtt threads from the sensors, storing their values in the database;

Relative to 1):

execute:  sudo nano /lib/systemd/system/client.service and put in the following code:

[Unit]
Description=Start Myproject
After=graphical.target
Wants=graphical.target

[Service]
User=pi
Group=pi
ExecStart=/bin/bash -c "export DISPLAY=:0; export XAUTHORITY=/home/pi/.Xauthority; /home/pi/Desktop/sersorsProject/launch.command"

[Install]
WantedBy=graphical.target


ctrt + x; 
s
press enter;


Regarding 2):

execute: sudo nano /lib/systemd/system/sersorsProject_db.service

[Unit]
Description=Example python App running on Ubuntu
After=multi-user.target
[Service]
Type=simple

ExecStart=/usr/bin/python3 -u /home/pi/Desktop/Code_DB/teste.py
Restart=always
# Restart service after 10 seconds if the dotnet service crashes:
RestartSec=10
KillSignal=SIGINT
SyslogIdentifier=Nameofyourapp

[Install]
WantedBy=multi-user.target

```

#### Then perform the following:

```bash
Then execute:

sudo systemctl enable sersorsProject_db.service

sudo systemctl enable client.service

sudo systemctl daemon-reload

sudo systemctl start sersorsProject_db.service

sudo systemctl start client.service

To check the status of the services:


sudo systemctl status sersorsProject_db.service

sudo systemctl status client.service


From this point on, on each boot the backend system/graphical interface and database service start up automatically.

```

### Pinout

![alt text](https://docs.microsoft.com/pt-br/windows/iot-core/media/pinmappingsrpi/rp2_pinout.png)

### The sensors should be connected according to the following tables:

| DHT11 Temp/Hum    | Raspberry Pi  | ADC PI  
| -------------     | ------------- | --------|
| `-`               | 14            |         |
| `+`               | 4             |         |
| `Sinal`           | 7             |         |

| Co2               | Raspberry Pi  | ADC PI  
| -------------     | ------------- | --------|
| `Vcc`             |               |  5V     |
| `Gnd`             |               |  Gnd    |
| `A0`              |               |  Pin 1  |

| Sensor VEML7700 Luz  | Raspberry Pi  | ADC PI  
| -------------     | ------------- | --------|
| `Vcc`             |     1         |         |
| `Gnd`             |     6         |         |
| `SCL`             |     5         |         |
| `SDA`             |     3         |         |


| Sensor LM386 Som    | Raspberry Pi  | ADC PI  
| -------------     | ------------- | --------|
| `Vcc`               | 2            |         |
| `Gnd`               | 9             |         |
| `Sinal`           |              |    2     |


### Getting the backend up and running (other than for the service)

```bash
cd /home/pi/Desktop/sersorsProject/

sudo python3 client.py

```

### Place the Database to acquire / store values

```bash
cd /home/pi/Desktop/Code_DB/

sudo python3 teste.py

```

