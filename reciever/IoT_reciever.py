import paho.mqtt.client as mqtt
import json
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# influx_client = InfluxDBClient(url="http://localhost:8086", token="", org="-")
# write_api = influx_client.write_api(write_options=SYNCHRONOUS)

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("#")

def on_message(client, userdata, msg):
    print("Recieved:")

    payload = json.loads(msg.payload.decode('utf-8'))
    valid_payload = {}
    point = Point("data")

    print(msg.topic+" "+str(payload))
    
    for key in payload:
        if isinstance(payload[key], (int, float)):
            # print(f"{key}: {payload[key]}")
            point = point.field(key, payload[key])
            valid_payload[key] = payload[key]

    if 'timestamp' in payload:
        timestamp = datetime.strptime(payload["timestamp"], "%Y-%m-%d %H:%M:%S.%f")
        # print(f"timestamp: {timestamp}")
    else:
        timestamp = datetime.now()
    
    point = point.time(timestamp, WritePrecision.MS)
    # write_api.write(bucket=msg.topic, record=point)
    
    valid_payload["timestamp"] = timestamp
    
    print(point)
    print(valid_payload)
    print()


mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("localhost", 1883)

mqttc.loop_start()
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Exiting...")

# influx_client.close()
mqttc.loop_stop()
mqttc.disconnect()
