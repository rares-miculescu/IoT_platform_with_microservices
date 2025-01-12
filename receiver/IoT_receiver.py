import paho.mqtt.client as mqtt
import json
from datetime import datetime
from influxdb import InfluxDBClient
from influxdb_client import Point, WritePrecision, BucketsApi, QueryApi
from influxdb_client.client.write_api import SYNCHRONOUS
import logging
import os

# init logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# init influxdb client
influx_client = InfluxDBClient(host='influx', port=8086, username='rares', password='rares', database='scd')
enable_logs = os.getenv('DEBUG_DATA_FLOW')
logging.info(f"Enable logs: {enable_logs}")


def on_connect(client, userdata, flags, reason_code, properties):
    """ connect and subscribe to all """
    if enable_logs == "true":
        logging.info(f"Connected with result code {reason_code}")
    client.subscribe("#")

def on_message(client, userdata, msg):
    """ parse payload and send to influxdb """
    try:
        payload = json.loads(msg.payload.decode('utf-8'))
        location, device = msg.topic.split("/")
        point = {
            "measurement": "scd",
            "tags": {
                "location": location,
                "device": device
            },
            "fields":{}
        }

        for key in payload:
            # check if value is int or float
            if isinstance(payload[key], (int, float)):
                point["fields"][key] = payload[key]

        if 'timestamp' in payload:
            # check if value has timestamp
            timestamp = datetime.strptime(payload["timestamp"], "%Y-%m-%d %H:%M:%S.%f")
            point["timestamp"] = timestamp
        else:
            point["timestamp"] = datetime.now()

        influx_client.write_points([point])
        if enable_logs == "true":
            logging.info(f"Data written: {point}")

    except Exception as e:
        if enable_logs == "true":
            logging.error(f"Error processing message: {e}")

# init mqtt client
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.connect("mqtt", 1883)
mqttc.loop_start()

try:
    while True:
        pass
except KeyboardInterrupt:
    logging.info("Exiting...")

mqttc.loop_stop()
mqttc.disconnect()
influx_client.close()
