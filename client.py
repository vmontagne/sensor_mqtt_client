import paho.mqtt.client as mqtt
import base64
import json
import os
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))

topic= 'v3/+/devices/+/up'

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    obj = json.loads(msg.payload)

    encoded_string = obj['uplink_message']['frm_payload']

    decoded_string = base64.b64decode(encoded_string)

    [temperature, humidite] = decoded_string.decode('utf-8').split(';')

    device = msg.topic.split('/')[3]
    print(f"device : {device}")
    print(f"temperature : {temperature}")
    print(f"humidite : {humidite}")

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

username = 'noel@ttn'
password = 'NNSXS.5R3UGAANB7OK67HD4SRCV2YJCGZQJ57SWQZDDRQ.HNCJAWPB3SGDL3YSVUTFJ2IRODONOJ7SHLDINY6IGKUDHOFWHTAA'
mqttc.username_pw_set(USERNAME, PASSWORD)

mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect(HOST, PORT, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
mqttc.loop_forever()

# device | temperature | humidite | datetime | data
# {"label": value}

# device | label