import paho.mqtt.client as mqtt
from time import sleep
import json
from datetime import datetime
import random
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

TOPICS = [ "UPB/RPi_1", "UPB/PRECIS", "UPB/SCD", "UPB/CS", "malware/unknown", "scd/teapa", "Craiova/macete" ]
FIELDS = [ "TMP", "HUMID", "BAT", "KMH", "RAIN", "PRESSURE", "WIND", "UV", "CO2", "NOISE", "PM1", "PM2.5", "PM10", "O3", "SO2", "NO2", "CO", "H2S", "NH3", "CH4", "C2H5OH", "C3H8", "C4H10", "C5H12", "C6H14", "C7H16", "C8H18", "C9H20", "C10H22", "C11H24", "C12H26", "C13H28", "C14H30", "C15H32", "C16H34", "C17H36", "C18H38", "C19H40", "C20H42", "C21H44", "C22H46", "C23H48", "C24H50", "C25H52", "C26H54", "C27H56", "C28H58", "C29H60", "C30H62", "C31H64", "C32H66", "C33H68", "C34H70", "C35H72", "C36H74", "C37H76", "C38H78", "C39H80", "C40H82", "C41H84", "C42H86", "C43H88", "C44H90", "C45H92", "C46H94", "C47H96", "C48H98", "C49H100", "C50H102", "C51H104", "C52H106", "C53H108", "C54H110", "C55H112", "C56H114", "C57H116", "C58H118", "C59H120", "C60H122", "C61H124", "C62H126", "C63H128", "C64H130", "C65H132", "C66H134", "C67H136", "C68H138", "C69H140", "C70H142", "C71H144", "C72H146", "C73H148", "C74H150",]
STRINGS = [ "teapa", "iti urez", "ok", "nu-i bine", "scd", "poate", "nu iti spun", "5 lei si iti zic", "au venit hacherii peste noi"]

def generate_json(timestamp):
    payload = {}
    length = random.randint(1, len(FIELDS))
    included = []
    for i in range(length):
        index = random.randint(0, len(FIELDS)-1)
        while index in included:
            index = random.randint(0, len(FIELDS)-1)
        field = FIELDS[index]
        included.append(index)
        if random.choice([True, False]):
            payload.update({field: STRINGS[random.randint(0, len(STRINGS)-1)]})
        else:
            payload.update({field: random.randint(0, 100)})
    if random.choice([True, False]):
        payload.update({"timestamp": str(timestamp)})
    return json.dumps(payload)

def on_connect(client, userdata, flags, reason_code, properties):
    logging.info(f"Connected with result code {reason_code}")

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect

mqttc.connect("mqtt", 1883)

mqttc.loop_start()

try:
    while True:
        number_of_publishings = random.randint(1, 20)
        logging.info(f"Publishing {number_of_publishings} messages")
        timestamp = datetime.now()
        for i in range(number_of_publishings):
            topic = TOPICS[random.randint(0, len(TOPICS)-1)]
            mqttc.publish(topic, generate_json(timestamp))
            logging.info(f"Published to {topic}")
            sleep(2)
except KeyboardInterrupt:
    logging.info("Exiting...")

mqttc.loop_stop()
mqttc.disconnect()


