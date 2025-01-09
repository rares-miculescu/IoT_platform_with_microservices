import paho.mqtt.client as mqtt
import json
from datetime import datetime

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("#")

def on_message(client, userdata, msg):
    print("Recieved:")
    payload = json.loads(msg.payload.decode('utf-8'))
    print(msg.topic+" "+str(payload))
    for key in payload:
        if isinstance(payload[key], int) or isinstance(payload[key], float):
            print(f"{key}: {payload[key]}")
    if 'timestamp' in payload:
        timestamp = datetime.strptime(payload["timestamp"], "%Y-%m-%d %H:%M:%S.%f")
        print(f"timestamp: {timestamp}")
    print()


mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("mqtt", 1883)

mqttc.loop_forever()
mqttc.disconnect()
