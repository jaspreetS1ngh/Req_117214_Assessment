import os

# config.py

class Config:
    MQTT_BROKER = "test.mosquitto.org"
    MQTT_PORT = 1883
    MQTT_TOPIC_ID = "19d19053-749e-4f2c-a8c8-d0c5edce92f9" # topic id is variable you can change it as needed.

    MQTT_TOPIC_INPUT = f"BRE/calculateWinterSupplementInput/{MQTT_TOPIC_ID}"
    MQTT_TOPIC_OUTPUT = f"BRE/calculateWinterSupplementOutput/{MQTT_TOPIC_ID}"
    
