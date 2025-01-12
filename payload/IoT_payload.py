import paho.mqtt.client as mqtt
from time import sleep
import json
from datetime import datetime
import random
import logging

# init logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# topics, fields and strings
TOPICS = [ "UPB/RPi_1", "UPB/PRECIS", "UPB/SCD", "UPB/CS", "malware/unknown", "scd/teapa", "Craiova/macete" ]
FIELDS = [ "TMP", "HUMID", "BAT", "KMH", "RAIN", "PRESSURE", "WIND", "UV", "CO2", "NOISE", "PM1", "PM2.5", "PM10", "O3", "SO2", "NO2", "CO", "H2S", "NH3", "CH4"]
STRINGS = [ "teapa", "iti urez", "ok", "nu-i bine", "scd", "poate", "nu iti spun", "5 lei si iti zic", "au venit hacherii peste noi"]

def generate_json(timestamp):
    """ generates random json payload """

    payload = {}
    # get length of payload
    length = random.randint(2, len(FIELDS))
    included = []
    for i in range(length):
        # get random field
        index = random.randint(0, len(FIELDS)-1)
        while index in included:
            # if already included, get another one
            index = random.randint(0, len(FIELDS)-1)
        field = FIELDS[index]
        included.append(index)
        if random.choice([True, False]):
            # if random choice is True, add a string, else add a number
            payload.update({field: STRINGS[random.randint(0, len(STRINGS)-1)]})
        else:
            payload.update({field: random.randint(0, 100)})
    if random.choice([True, False]):
        # if random choice is True, add a timestamp
        payload.update({"timestamp": str(timestamp)})
    return json.dumps(payload)

def on_connect(client, userdata, flags, reason_code, properties):
    logging.info(f"Connected with result code {reason_code}")

# mqtt connection
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect

mqttc.connect("mqtt", 1883)

mqttc.loop_start()

try:
    while True:
        # get number of messages on that timestamp
        number_of_publishings = random.randint(1, 20)
        logging.info(f"Publishing {number_of_publishings} messages")
        timestamp = datetime.now()
        for i in range(number_of_publishings):
            # publish to random topic
            topic = TOPICS[random.randint(0, len(TOPICS)-1)]
            mqttc.publish(topic, generate_json(timestamp))
            logging.info(f"Published to {topic}")
            sleep(2)
except KeyboardInterrupt:
    logging.info("Exiting...")

mqttc.loop_stop()
mqttc.disconnect()


