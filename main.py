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
    "ferrorama/station/luminanceStatus": None,
    "ferrorama/station/presence3": None,
    "ferrorama/station/presence1": None,
    "ferrorama/station/humidity": None,
    "ferrorama/station/temperature": None,
}

# Função para atualizar os indicadores na interface
def update_indicator(topic, message):
    # Para indicadores booleanos
    if topic in [
        "ferrorama/station/luminanceStatus",
        "ferrorama/station/presence3",
        "ferrorama/station/presence1"
    ]:
        color = "green" if message == "1" else "red" if message == "0" else "gray"
        indicators[topic].config(bg=color, text=f"{topic.split('/')[-1]}: {message}")
    # Para temperatura e umidade, apenas atualizar texto
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
        print(f"Conectado com código: {reason_code}")
        client.subscribe("#")
        print("Escutando o broker...")
    else:
        print("Falha na conexão com o Broker")

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
