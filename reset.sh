#!/bin/bash

./run.sh close
./run.sh leave
docker volume prune -f
docker network prune -f
docker volume rm scd3_grafana-volume
docker volume rm scd3_influx-volume
./run.sh init
./run.sh run