#!/bin/bash

if [ "$#" -ne 1 ] || [ "$1" == "help" ]; then
    echo "Usage: $0 <option>"
    echo ""
    echo "  help: Display this help message"
    echo ""
    echo "  init: Initialize the swarm"
    echo ""
    echo "  run: Build images and run the stack"
    echo ""
    echo "  close: Close the stack and remove all services"
    echo ""
    echo "  leave: Leave the swarm"
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
    docker build -t iot_receiver ./receiver
    docker stack deploy -c stack.yml scd3
    exit 0
fi

if [ "$1" == "volumes" ]; then
    docker volume prune -f
    exit 0
fi
