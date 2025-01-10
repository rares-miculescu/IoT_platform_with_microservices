import paho.mqtt.client as mqtt
import json
from datetime import datetime
from influxdb import InfluxDBClient
from influxdb_client import Point, WritePrecision, BucketsApi, QueryApi
from influxdb_client.client.write_api import SYNCHRONOUS
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

influx_client = InfluxDBClient(host='influx', port=8086, username='rares', password='rares', database='scd')

# print(influx_client.get_list_database())

# # init write api
# write_api = influx_client.write_api(write_options=SYNCHRONOUS)
# # init buckets api
# bucket_api = influx_client.buckets_api()
# # init query api
# query_api = influx_client.query_api()

# create retention policy
def on_connect(client, userdata, flags, reason_code, properties):
    logging.info(f"Connected with result code {reason_code}")
    client.subscribe("#")

def on_message(client, userdata, msg):
    try:
        logging.info("Recieved:")
        # print(f"Topic: {msg.topic} Message: {msg.payload}")

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
            if isinstance(payload[key], (int, float)):
                point["fields"][key] = payload[key]

        if 'timestamp' in payload:
            timestamp = datetime.strptime(payload["timestamp"], "%Y-%m-%d %H:%M:%S.%f")
            point["timestamp"] = timestamp
        else:
            point["timestamp"] = datetime.now()

        influx_client.write_points([point])
        # write_api.write(bucket="scd", record=point, org="upb")
        logging.info(f"Data written: {point}")

    except Exception as e:
        logging.error(f"Error processing message: {e}")

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
# influx_client.close()

# print("Data written successfully.")
# query = '''
# from(bucket: "scd")
#     |> range(start: -1d)
# '''
# result = query_api.query(query=query)
# for table in result:
#     for record in table.records:
#         print(f"Time: {record.get_time()}, Record: {record}")
