#!/bin/bash

REGISTRY_BASE="quay.io/kenmoini"

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd $SCRIPT_DIR/..

echo -e "\n\n====== Building wifi-status ======"
cd apps/wifi-patrol/
podman build -t ${REGISTRY_BASE}/wifi-status:latest -f Containerfile.wifi-status .
echo -e "\n\n====== Pushing wifi-status ======"
podman push ${REGISTRY_BASE}/wifi-status:latest
cd $SCRIPT_DIR/..

echo -e "\n\n====== Building gopro-control ======"
cd apps/gopro-control/
podman build -t ${REGISTRY_BASE}/gopro-control:latest -f Containerfile .
echo -e "\n\n====== Pushing gopro-control ======"
podman push ${REGISTRY_BASE}/gopro-control:latest
cd $SCRIPT_DIR/..

echo -e "\n\n====== Building drone-control ======"
cd apps/drone-control/
podman build -t drone-control -f Containerfile .
echo -e "\n\n====== Pushing drone-control ======"
podman push ${REGISTRY_BASE}/drone-control:latest
cd $SCRIPT_DIR/..

echo -e "\n\n====== Building s3-shipper ======"
cd apps/s3-shipper/
podman build -t ${REGISTRY_BASE}/s3-shipper:latest -f Containerfile .
echo -e "\n\n====== Pushing s3-shipper ======"
podman push ${REGISTRY_BASE}/s3-shipper:latest
cd $SCRIPT_DIR/..

echo -e "\n\n====== Building symphony ======"
cd apps/symphony/
podman build -t ${REGISTRY_BASE}/symphony:latest -f Containerfile .
echo -e "\n\n====== Pushing symphony ======"
podman push ${REGISTRY_BASE}/symphony:latest

echo -e "\n\n====== Finished! ======"
