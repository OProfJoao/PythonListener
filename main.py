import paho.mqtt.client as mqtt
import os
import tkinter as tk
from dotenv import load_dotenv

load_dotenv()

# Configurações MQTT
BROKER = os.getenv("MQTT_BROKER")
PORT = 8883
USER = os.getenv("MQTT_USER")
PASSWORD = os.getenv("MQTT_PASSWORD")

# Tópicos a monitorar
TOPICS = {
    "ferrorama/nodes/luminanceStatus": None,
    "ferrorama/station/presence3": None,
    "ferrorama/nodes/presence1": None,
    "ferrorama/nodes/presence2": None,
    "ferrorama/nodes/presence3": None,
    "ferrorama/nodes/presence4": None,
    "ferrorama/nodes/humidity": None,
    "ferrorama/nodes/temperature": None,
}

# Tópicos com valores booleanos (0/1)
BOOLEAN_TOPICS = [
    "ferrorama/nodes/luminanceStatus",
    "ferrorama/station/presence3",
    "ferrorama/nodes/presence1",
    "ferrorama/nodes/presence2",
    "ferrorama/nodes/presence3",
    "ferrorama/nodes/presence4"
]

# Função para atualizar os indicadores na interface
def update_indicator(topic, message):
    if topic in BOOLEAN_TOPICS:
        msg = message.strip()
        color = "green" if msg == "1" else "red" if msg == "0" else "gray"
        indicators[topic].config(bg=color, text=f"{topic.split('/')[-1]}: {msg}")
    else:
        indicators[topic].config(bg="white", text=f"{topic.split('/')[-1]}: {message}")

# Função chamada quando uma mensagem chega
def on_message(client, userdata, msg):
    message = msg.payload.decode()
    topic = msg.topic
    print(f"Topic: {topic} | Mensagem: {message}")
    if topic in TOPICS:
        root.after(0, update_indicator, topic, message)

# Função chamada ao conectar no broker
def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print(f"Conectado com sucesso ao broker.")
        client.subscribe("#")
        print("Escutando todos os tópicos...")
    else:
        print(f"Falha na conexão com o Broker. Código: {reason_code}")

# Cliente MQTT
mqttClient = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="GlobalListener")
mqttClient.tls_set()
mqttClient.tls_insecure_set(True)
mqttClient.username_pw_set(USER, PASSWORD)
mqttClient.on_connect = on_connect
mqttClient.on_message = on_message
mqttClient.connect(BROKER, PORT)
mqttClient.loop_start()

# Interface Tkinter
root = tk.Tk()
root.title("Indicadores MQTT")

indicators = {}
for idx, topic in enumerate(TOPICS):
    lbl = tk.Label(root, text=f"{topic.split('/')[-1]}: N/A", width=30, height=2, bg="gray", font=("Arial", 14))
    lbl.grid(row=idx, column=0, padx=10, pady=5)
    indicators[topic] = lbl

try:
    root.mainloop()
finally:
    mqttClient.loop_stop()
    mqttClient.disconnect()
