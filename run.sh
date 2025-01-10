#!/bin/bash

# help message
if [ "$#" -ne 1 ] || [ "$1" == "help" ]; then
    echo "Usage: $0 <option>"
    echo ""
    echo "  help: Display this help message"
    echo ""
    echo "  init: Initialize the swarm"
    echo ""
    echo "  run: Build images and run the stack (also runs init)"
    echo ""
    echo "  close: Close the stack and remove all services (also runs leave)"
    echo ""
    echo "  leave: Leave the swarm"
    echo ""
    echo "  volumes: Remove all unused volumes"
    exit 1
fi

# init swarm
if [ "$1" == "init" ]; then
    sudo docker swarm init 
    exit 0
fi

# leave swarm
if [ "$1" == "leave" ]; then
    sudo docker swarm leave --force
    exit 0
fi

# close stack
if [ "$1" == "close" ]; then
    docker stack ls --format "{{.Name}}" | xargs -n 1 docker stack rm 
    ./run.sh leave
    exit 0
fi

# run stack
if [ "$1" == "run" ]; then
    ./run.sh init
    docker build -t iot_payload ./payload
    docker build -t iot_receiver ./receiver
    docker stack deploy -c stack.yml scd3
    exit 0
fi

# remove unused volumes
if [ "$1" == "volumes" ]; then
    docker volume prune -f
    exit 0
fi
