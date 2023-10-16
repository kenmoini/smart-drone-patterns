#!/bin/bash

# This script is used to build and run Symphony locally for development purposes.
# It is not intended to be used in production.

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR/..

VOLUMES=""

if [ "${1}" == "live" ]; then
  VOLUMES = "-v $(pwd)/app-src/templates:/opt/app-root/src/templates -v $(pwd)/app-src/static:/opt/app-root/src/static"
fi

echo -e "\n\n========= Building Symphony =========\n"
podman build -t symphony -f Containerfile .

cd ../roboflow-robot
echo -e "\n\n========= Building Roboflow Robot =========\n"
podman build -t roboflow-robot -f Containerfile .

cd ../symphony

#export BANANA_PHONE_ENDPOINT="http://localhost:8675"

podman kill symphony || true
podman rm symphony || true
podman run --name symphony -d -p 9191:9191 \
 -e ROBOFLOW_ROBOT_ENDPOINT="http://endurance.kemo.labs:7272" \
 -e BANANA_PHONE_ENDPOINT="http://endurance.kemo.labs:8675" \
 ${VOLUMES} \
 symphony

# Also will need to run a few other services...
#source ~/.banana-phone.env

podman kill banana-phone || true
podman rm banana-phone || true
podman run --name banana-phone -d -p 8675:8675 --env-file ~/.banana-phone.env quay.io/kenmoini/banana-phone:latest

podman kill roboflow-robot || true
podman rm roboflow-robot || true
podman run --name roboflow-robot -d -p 7272:7272 \
 -v /tmp/roboflow/data:/tmp/roboflow/data:Z \
 --env-file ~/.roboflow-robot.env \
 roboflow-robot
