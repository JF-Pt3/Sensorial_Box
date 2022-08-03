# Zigbee2Mqtt

Zigbee2Mqtt is a bridge to read temperature, humidity and pressure for a aqara sensor

Publish in the following topics MQTT

```
"stream/aqara/temperature"
"stream/aqara/humidity"
"stream/aqara/pressure"
```

## Installation

For Raspberry Pi OS

```bash
sudo sh install.sh

nano /opt/zigbee2mqtt/data/configuration.yaml
    homeassistant: false
    permit_join: true
    mqtt:
        base_topic: stream
        server: 'mqtt://localhost'
    serial:
        port: /dev/ttyACM0
    advanced:
        network-key: GENERATE
        output: attribute

cd /opt/zigbee2mqtt
npm start

-- Connect aqara sensor --

nano /opt/zigbee2mqtt/data/configuration.yaml
-- change friendly name to aqara --
-- change permit_join to false --

sudo systemctl start zigbee2mqtt
```