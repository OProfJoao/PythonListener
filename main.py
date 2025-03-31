import paho.mqtt.client as mqtt
import os
import time
from dotenv import load_dotenv

load_dotenv()

def on_message(client,userData,msg):
    print(f"{msg.topic}: {str(msg.payload.decode())}")

BROKER = os.getenv("MQTT_BROKER")
PORT = 8883
USER = os.getenv("MQTT_USER")
PASSWORD = os.getenv("MQTT_PASSWORD")



mqttClient = mqtt.Client(client_id="GlobalListener")
mqttClient.tls_set()
mqttClient.tls_insecure_set()

mqttClient.username_pw_set(USER,PASSWORD)
mqttClient.connect(BROKER,PORT)

mqttClient.subscribe("#")
mqttClient.on_message = on_message

mqttClient.loop_forever()

time.sleep(0.5)

