# IoT platform with microservices

## Introduction

Platform that generates random IoT data, that is stored and viewed. The data is sent and recieved using MQTT protocol, stored inside InfluxDB database and viewed using Grafana.

## Solution description

The solution is implemented using Docker Swarm, where there are 4 components:

- Eclipse Mosquitto : MQTT container, listening on port 1883, with anonymous access

- IoT_payload : data feeder implemented to randomly generate data to be sent to MQTT. During a random timestamp, it generates a random number of payloads, with random fields and values. Instead of a numeric value, the program can also inject randomly a string.

- IoT_receiver : recieves all data from mqtt, filters the numerical data, checks if a timestamp exists (if not, the current time is added) and sends the information to the database.

- InfluxDB : database, where data is stored.

- Grafana : app that connects to the database to collect the data, to be shown in multiple ways.

## How to run

Use run.sh. 

To simply run this, use:
```
./run.sh run
```

To close it, run:
```
./run.sh close
```

For more informations:
```
./run.sh help
```
