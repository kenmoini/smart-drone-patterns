#!/bin/bash

REGISTRY_BASE="quay.io/kenmoini"
REGISTRY_IMAGE="darkness"
TAG_BASE="sep-models-"

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd $SCRIPT_DIR/..

function pullImageSet() {
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

  echo -e "\n\n===== Pulling tagged images for ${archSlash} =====\n\n"
  podman pull --platform ${archSlash} ${REGISTRY_BASE}/${REGISTRY_IMAGE}:${TAG_BASE}latest${tagSuffix}
  podman pull --platform ${archSlash} ${REGISTRY_BASE}/${REGISTRY_IMAGE}:${TAG_BASE}main${tagSuffix}
  podman pull --platform ${archSlash} ${REGISTRY_BASE}/${REGISTRY_IMAGE}:${TAG_BASE}$(git rev-parse --short HEAD)${tagSuffix}
  podman pull --platform ${archSlash} ${REGISTRY_BASE}/${REGISTRY_IMAGE}:${TAG_BASE}$(git rev-parse HEAD)${tagSuffix}
}

#pullImageSet x86_64
#pullImageSet aarch64

echo -e "\n\n===== Pruning previous images =====\n\n"
#podman system prune -f -a
podman rmi -f ${REGISTRY_BASE}/${REGISTRY_IMAGE}:${TAG_BASE}latest || true
podman rmi -f ${REGISTRY_BASE}/${REGISTRY_IMAGE}:${TAG_BASE}main || true
podman rmi -f ${REGISTRY_BASE}/${REGISTRY_IMAGE}:${TAG_BASE}$(git rev-parse --short HEAD) || true
podman rmi -f ${REGISTRY_BASE}/${REGISTRY_IMAGE}:${TAG_BASE}$(git rev-parse HEAD) || true

echo -e "\n\n===== Removing any previous manifests - ${TAG_BASE}latest =====\n\n"
podman manifest rm ${REGISTRY_BASE}/${REGISTRY_IMAGE}:${TAG_BASE}latest
echo -e "\n\n===== Removing any previous manifests - ${TAG_BASE}main =====\n\n"
podman manifest rm ${REGISTRY_BASE}/${REGISTRY_IMAGE}:${TAG_BASE}main
echo -e "\n\n===== Removing any previous manifests - ${TAG_BASE}$(git rev-parse --short HEAD) =====\n\n"
podman manifest rm ${REGISTRY_BASE}/${REGISTRY_IMAGE}:${TAG_BASE}$(git rev-parse --short HEAD)
echo -e "\n\n===== Removing any previous manifests - ${TAG_BASE}$(git rev-parse HEAD) =====\n\n"
podman manifest rm ${REGISTRY_BASE}/${REGISTRY_IMAGE}:${TAG_BASE}$(git rev-parse HEAD)

echo -e "\n\n===== Creating multi-arch manifests - latest =====\n\n"
podman manifest create \
  ${REGISTRY_BASE}/${REGISTRY_IMAGE}:${TAG_BASE}latest \
  ${REGISTRY_BASE}/${REGISTRY_IMAGE}:${TAG_BASE}latest-linux-arm64 \
  ${REGISTRY_BASE}/${REGISTRY_IMAGE}:${TAG_BASE}latest-linux-amd64

echo -e "\n\n===== Creating multi-arch manifests - main =====\n\n"
podman manifest create \
  ${REGISTRY_BASE}/${REGISTRY_IMAGE}:${TAG_BASE}main \
  ${REGISTRY_BASE}/${REGISTRY_IMAGE}:${TAG_BASE}main-linux-arm64 \
  ${REGISTRY_BASE}/${REGISTRY_IMAGE}:${TAG_BASE}main-linux-amd64

echo -e "\n\n===== Creating multi-arch manifests - $(git rev-parse --short HEAD) =====\n\n"
podman manifest create \
  ${REGISTRY_BASE}/${REGISTRY_IMAGE}:${TAG_BASE}$(git rev-parse --short HEAD) \
  ${REGISTRY_BASE}/${REGISTRY_IMAGE}:${TAG_BASE}$(git rev-parse --short HEAD)-linux-arm64 \
  ${REGISTRY_BASE}/${REGISTRY_IMAGE}:${TAG_BASE}$(git rev-parse --short HEAD)-linux-amd64

echo -e "\n\n===== Creating multi-arch manifests - $(git rev-parse HEAD) =====\n\n"
podman manifest create \
  ${REGISTRY_BASE}/${REGISTRY_IMAGE}:${TAG_BASE}$(git rev-parse HEAD) \
  ${REGISTRY_BASE}/${REGISTRY_IMAGE}:${TAG_BASE}$(git rev-parse HEAD)-linux-arm64 \
  ${REGISTRY_BASE}/${REGISTRY_IMAGE}:${TAG_BASE}$(git rev-parse HEAD)-linux-amd64

echo -e "\n\n===== Pushing multi-arch manifests =====\n\n"
podman manifest push --rm ${REGISTRY_BASE}/${REGISTRY_IMAGE}:${TAG_BASE}latest docker://${REGISTRY_BASE}/${REGISTRY_IMAGE}:${TAG_BASE}latest
podman manifest push --rm ${REGISTRY_BASE}/${REGISTRY_IMAGE}:${TAG_BASE}main docker://${REGISTRY_BASE}/${REGISTRY_IMAGE}:${TAG_BASE}main
podman manifest push --rm ${REGISTRY_BASE}/${REGISTRY_IMAGE}:${TAG_BASE}$(git rev-parse --short HEAD) docker://${REGISTRY_BASE}/${REGISTRY_IMAGE}:${TAG_BASE}$(git rev-parse --short HEAD)
podman manifest push --rm ${REGISTRY_BASE}/${REGISTRY_IMAGE}:${TAG_BASE}$(git rev-parse HEAD) docker://${REGISTRY_BASE}/${REGISTRY_IMAGE}:${TAG_BASE}$(git rev-parse HEAD)
