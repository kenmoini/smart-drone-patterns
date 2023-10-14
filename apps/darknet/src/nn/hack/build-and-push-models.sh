#!/bin/bash

REGISTRY_BASE="quay.io/kenmoini"
REGISTRY_IMAGE="darkness"
TAG_BASE="sep-models-"

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR/..

function buildImageSet() {
  arch=$1
  archSlash=""

  if [ -z "$arch" ]; then
    echo "No architecture specified"
    exit 1
  fi
  if [ "$arch" != "x86_64" ] && [ "$arch" != "aarch64" ]; then
    echo "Invalid architecture specified"
    exit 1
  fi

  if [ "$arch" == "x86_64" ]; then
    archSlash="linux/amd64"
  fi
  if [ "$arch" == "aarch64" ]; then
    archSlash="linux/arm64/v8"
  fi

  if [ "$arch" == "x86_64" ]; then
    tagSuffix="-linux-amd64"
  fi
  if [ "$arch" == "aarch64" ]; then
    tagSuffix="-linux-arm64"
  fi

  echo -e "\n\n===== Pulling base image... =====\n\n"
  podman pull registry.access.redhat.com/ubi8/ubi-minimal:8.8-1072.1696517598

  echo -e "\n\n===== Building for ${arch} =====\n\n"
  podman build -t ${REGISTRY_BASE}/${REGISTRY_IMAGE}-${TAG_BASE}${tagSuffix} -f Containerfile.models .

  echo -e "\n\n===== Tagging for ${arch} =====\n\n"
  podman tag ${REGISTRY_BASE}/${REGISTRY_IMAGE}-${TAG_BASE}${tagSuffix} ${REGISTRY_BASE}/${REGISTRY_IMAGE}:${TAG_BASE}latest${tagSuffix}
  podman tag ${REGISTRY_BASE}/${REGISTRY_IMAGE}-${TAG_BASE}${tagSuffix} ${REGISTRY_BASE}/${REGISTRY_IMAGE}:${TAG_BASE}main${tagSuffix}
  podman tag ${REGISTRY_BASE}/${REGISTRY_IMAGE}-${TAG_BASE}${tagSuffix} ${REGISTRY_BASE}/${REGISTRY_IMAGE}:${TAG_BASE}$(git rev-parse --short HEAD)${tagSuffix}
  podman tag ${REGISTRY_BASE}/${REGISTRY_IMAGE}-${TAG_BASE}${tagSuffix} ${REGISTRY_BASE}/${REGISTRY_IMAGE}:${TAG_BASE}$(git rev-parse HEAD)${tagSuffix}

  echo -e "\n\n===== Pushing images for ${arch} =====\n\n"
  podman push ${REGISTRY_BASE}/${REGISTRY_IMAGE}:${TAG_BASE}latest${tagSuffix}
  podman push ${REGISTRY_BASE}/${REGISTRY_IMAGE}:${TAG_BASE}main${tagSuffix}
  podman push ${REGISTRY_BASE}/${REGISTRY_IMAGE}:${TAG_BASE}$(git rev-parse --short HEAD)${tagSuffix}
  podman push ${REGISTRY_BASE}/${REGISTRY_IMAGE}:${TAG_BASE}$(git rev-parse HEAD)${tagSuffix}
}

buildImageSet "$(uname -i)"
