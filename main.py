import paho.mqtt.client as mqtt

def on_message(client,userData,msg):
    print(f"{msg.topic}: {str(msg.payload)}")
    pass



mqttClient = mqtt.Client(mqtt.API_VERSION2,client_id="GlobalListener")
mqttClient.tls_insecure_set()

mqttClient.username_pw_set("USER","PASSWORD")
mqttClient.connect("host",8883,)

mqttClient.subscribe("topic")
mqttClient.on_message = on_message()

mqttClient.loop_forever()


