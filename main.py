import paho.mqtt.client as mqtt
import os
import time
from dotenv import load_dotenv

load_dotenv()

def on_message(client,userData,msg):
    print(f"Topic: {msg.topic} | Mensagem: {str(msg.payload.decode())}")

def on_connect(client, userdata, flags, reason_code, properties=None):
    if( reason_code == 0):
        print(f"Connected with code: {reason_code}")
        mqttClient.subscribe("#")
        print("Listening to broker...")
    else:
        print("Failed to connect to Broker")
        
BROKER = os.getenv("MQTT_BROKER")
PORT = 8883
USER = os.getenv("MQTT_USER")
PASSWORD = os.getenv("MQTT_PASSWORD")



mqttClient = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,client_id="GlobalListener")
mqttClient.tls_set()
mqttClient.tls_insecure_set(True)

mqttClient.username_pw_set(USER,PASSWORD)
mqttClient.connect(BROKER,PORT)



mqttClient.on_connect = on_connect
mqttClient.on_message = on_message

mqttClient.loop_forever()

mqttClient.disconnect()

