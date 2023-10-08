#!/bin/bash

REGISTRY_BASE="quay.io/kenmoini"
REGISTRY_IMAGE="b-sep-ubnt22-cmake"

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd $SCRIPT_DIR/..

echo -e "\n\n===== Setting up multiarch build environment =====\n\n"
podman run --rm --privileged docker.io/multiarch/qemu-user-static --reset -p yes

function buildImageSet() {
  arch=$1
  archSlash=""

  if [ -z "$arch" ]; then
    echo "No architecture specified"
    exit 1
  fi
  if [ "$arch" != "linux-amd64" ] && [ "$arch" != "linux-arm64" ]; then
    echo "Invalid architecture specified"
    exit 1
  fi

  if [ "$arch" == "linux-amd64" ]; then
    archSlash="linux/amd64"
  fi
  if [ "$arch" == "linux-arm64" ]; then
    archSlash="linux/arm64/v8"
  fi

  echo -e "\n\n===== Pulling base image =====\n\n"
  podman pull --platform ${archSlash} nvcr.io/nvidia/cuda:12.2.0-devel-ubuntu22.04

  echo -e "\n\n===== Building for ${arch} =====\n\n"
  podman build --platform ${archSlash} -t ${REGISTRY_BASE}/${REGISTRY_IMAGE}-${arch} -f Containerfile.ubnt22-b-cmake .

  echo -e "\n\n===== Tagging for ${arch} =====\n\n"
  podman tag ${REGISTRY_BASE}/${REGISTRY_IMAGE}-${arch} ${REGISTRY_BASE}/${REGISTRY_IMAGE}:latest-${arch}
  podman tag ${REGISTRY_BASE}/${REGISTRY_IMAGE}-${arch} ${REGISTRY_BASE}/${REGISTRY_IMAGE}:main-${arch}
  podman tag ${REGISTRY_BASE}/${REGISTRY_IMAGE}-${arch} ${REGISTRY_BASE}/${REGISTRY_IMAGE}:$(git rev-parse --short HEAD)-${arch}
  podman tag ${REGISTRY_BASE}/${REGISTRY_IMAGE}-${arch} ${REGISTRY_BASE}/${REGISTRY_IMAGE}:$(git rev-parse HEAD)-${arch}
}

buildImageSet "linux-amd64"
buildImageSet "linux-arm64"

#podman push ${REGISTRY_BASE}/${REGISTRY_IMAGE}:latest
#podman push ${REGISTRY_BASE}/${REGISTRY_IMAGE}:main
#podman push ${REGISTRY_BASE}/${REGISTRY_IMAGE}:$(git rev-parse --short HEAD)
#podman push ${REGISTRY_BASE}/${REGISTRY_IMAGE}:$(git rev-parse HEAD)

#podman manifest create \
#  ${REGISTRY_BASE}/${REGISTRY_IMAGE}:latest \
#  ${REGISTRY_BASE}/${REGISTRY_IMAGE}:latest-linux-arm64 \
#  ${REGISTRY_BASE}/${REGISTRY_IMAGE}:latest-linux-amd64

#podman manifest create \
#  ${REGISTRY_BASE}/${REGISTRY_IMAGE}:main \
#  ${REGISTRY_BASE}/${REGISTRY_IMAGE}:main-linux-arm64 \
#  ${REGISTRY_BASE}/${REGISTRY_IMAGE}:main-linux-amd64

#podman manifest create \
#  ${REGISTRY_BASE}/${REGISTRY_IMAGE}:$(git rev-parse --short HEAD) \
#  ${REGISTRY_BASE}/${REGISTRY_IMAGE}:$(git rev-parse --short HEAD)-linux-arm64 \
#  ${REGISTRY_BASE}/${REGISTRY_IMAGE}:$(git rev-parse --short HEAD)-linux-amd64

#podman manifest create \
#  ${REGISTRY_BASE}/${REGISTRY_IMAGE}:$(git rev-parse HEAD) \
#  ${REGISTRY_BASE}/${REGISTRY_IMAGE}:$(git rev-parse HEAD)-linux-arm64 \
#  ${REGISTRY_BASE}/${REGISTRY_IMAGE}:$(git rev-parse HEAD)-linux-amd64

#podman manifest push ${REGISTRY_BASE}/${REGISTRY_IMAGE}:latest docker://${REGISTRY_BASE}/${REGISTRY_IMAGE}:latest
#podman manifest push ${REGISTRY_BASE}/${REGISTRY_IMAGE}:main docker://${REGISTRY_BASE}/${REGISTRY_IMAGE}:main
#podman manifest push ${REGISTRY_BASE}/${REGISTRY_IMAGE}:$(git rev-parse --short HEAD) docker://${REGISTRY_BASE}/${REGISTRY_IMAGE}:$(git rev-parse --short HEAD)
#podman manifest push ${REGISTRY_BASE}/${REGISTRY_IMAGE}:$(git rev-parse HEAD) docker://${REGISTRY_BASE}/${REGISTRY_IMAGE}:$(git rev-parse HEAD)
