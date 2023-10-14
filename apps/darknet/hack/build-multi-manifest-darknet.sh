#!/bin/bash

REGISTRY_BASE="quay.io/kenmoini"
REGISTRY_IMAGE="darkness"

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd $SCRIPT_DIR/..

echo -e "\n\n===== Pruning previous images =====\n\n"
#podman system prune -f -a
podman rmi -f ${REGISTRY_BASE}/${REGISTRY_IMAGE}:latest-darknet-ubnt22 || true
podman rmi -f ${REGISTRY_BASE}/${REGISTRY_IMAGE}:main-darknet-ubnt22 || true
podman rmi -f ${REGISTRY_BASE}/${REGISTRY_IMAGE}:$(git rev-parse --short HEAD)-darknet-ubnt22 || true
podman rmi -f ${REGISTRY_BASE}/${REGISTRY_IMAGE}:$(git rev-parse HEAD)-darknet-ubnt22 || true

echo -e "\n\n===== Removing any previous manifests - latest-darknet-ubnt22 =====\n\n"
podman manifest rm ${REGISTRY_BASE}/${REGISTRY_IMAGE}:latest-darknet-ubnt22
echo -e "\n\n===== Removing any previous manifests - main-darknet-ubnt22 =====\n\n"
podman manifest rm ${REGISTRY_BASE}/${REGISTRY_IMAGE}:main-darknet-ubnt22
echo -e "\n\n===== Removing any previous manifests - $(git rev-parse --short HEAD)-darknet-ubnt22 =====\n\n"
podman manifest rm ${REGISTRY_BASE}/${REGISTRY_IMAGE}:$(git rev-parse --short HEAD)-darknet-ubnt22
echo -e "\n\n===== Removing any previous manifests - $(git rev-parse HEAD)-darknet-ubnt22 =====\n\n"
podman manifest rm ${REGISTRY_BASE}/${REGISTRY_IMAGE}:$(git rev-parse HEAD)-darknet-ubnt22

echo -e "\n\n===== Creating multi-arch manifests - latest-darknet-ubnt22 =====\n\n"
podman manifest create \
  ${REGISTRY_BASE}/${REGISTRY_IMAGE}:latest-darknet-ubnt22 \
  ${REGISTRY_BASE}/${REGISTRY_IMAGE}:latest-darknet-ubnt22-linux-arm64
#  ${REGISTRY_BASE}/${REGISTRY_IMAGE}:latest-darknet-ubnt22-linux-amd64

echo -e "\n\n===== Creating multi-arch manifests - main-darknet-ubnt22 =====\n\n"
podman manifest create \
  ${REGISTRY_BASE}/${REGISTRY_IMAGE}:main-darknet-ubnt22 \
  ${REGISTRY_BASE}/${REGISTRY_IMAGE}:main-darknet-ubnt22-linux-arm64
#  ${REGISTRY_BASE}/${REGISTRY_IMAGE}:main-darknet-ubnt22-linux-amd64

echo -e "\n\n===== Creating multi-arch manifests - $(git rev-parse --short HEAD)-darknet-ubnt22 =====\n\n"
podman manifest create \
  ${REGISTRY_BASE}/${REGISTRY_IMAGE}:$(git rev-parse --short HEAD)-darknet-ubnt22 \
  ${REGISTRY_BASE}/${REGISTRY_IMAGE}:$(git rev-parse --short HEAD)-darknet-ubnt22-linux-arm64
#  ${REGISTRY_BASE}/${REGISTRY_IMAGE}:$(git rev-parse --short HEAD)-darknet-ubnt22-linux-amd64

echo -e "\n\n===== Creating multi-arch manifests - $(git rev-parse HEAD)-darknet-ubnt22 =====\n\n"
podman manifest create \
  ${REGISTRY_BASE}/${REGISTRY_IMAGE}:$(git rev-parse HEAD)-darknet-ubnt22 \
  ${REGISTRY_BASE}/${REGISTRY_IMAGE}:$(git rev-parse HEAD)-darknet-ubnt22-linux-arm64
#  ${REGISTRY_BASE}/${REGISTRY_IMAGE}:$(git rev-parse HEAD)-darknet-ubnt22-linux-amd64

echo -e "\n\n===== Pushing multi-arch manifests =====\n\n"
podman manifest push --rm ${REGISTRY_BASE}/${REGISTRY_IMAGE}:latest-darknet-ubnt22 docker://${REGISTRY_BASE}/${REGISTRY_IMAGE}:latest-darknet-ubnt22
podman manifest push --rm ${REGISTRY_BASE}/${REGISTRY_IMAGE}:main-darknet-ubnt22 docker://${REGISTRY_BASE}/${REGISTRY_IMAGE}:main-darknet-ubnt22
podman manifest push --rm ${REGISTRY_BASE}/${REGISTRY_IMAGE}:$(git rev-parse --short HEAD)-darknet-ubnt22 docker://${REGISTRY_BASE}/${REGISTRY_IMAGE}:$(git rev-parse --short HEAD)-darknet-ubnt22
podman manifest push --rm ${REGISTRY_BASE}/${REGISTRY_IMAGE}:$(git rev-parse HEAD)-darknet-ubnt22 docker://${REGISTRY_BASE}/${REGISTRY_IMAGE}:$(git rev-parse HEAD)-darknet-ubnt22
