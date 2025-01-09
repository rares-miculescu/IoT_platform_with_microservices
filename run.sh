#!/bin/bash

if [ "$#" -ne 1 ] || [ "$1" == "help" ]; then
    echo "Usage: $0 help / init / leave / close / run"
    exit 1
fi

if [ "$1" == "init" ]; then
    sudo docker swarm init 
    exit 0
fi

if [ "$1" == "leave" ]; then
    sudo docker swarm leave --force
    exit 0
fi

if [ "$1" == "close" ]; then
    docker stack ls --format "{{.Name}}" | xargs -n 1 docker stack rm
    exit 0
fi

if [ "$1" == "run" ]; then
    docker build -t iot_payload ./payload
    docker build -t iot_reciever ./reciever
    docker stack deploy -c stack.yml scd3
    exit 0
fi
