#!/bin/bash


podman build -t simple-chat -f Containerfile .

podman kill simple-chat || true
podman rm simple-chat || true

if [ "${1}" == "persistent" ]; then
  if [ "$(podman volume exists simple-chat-data)" == "1" ]; then
    podman volume create simple-chat-data
  fi

  podman run -d --name simple-chat -p 6969:6969 -p 7979:7979 -v simple-chat-data:/opt/app-root/src/data simple-chat
else
  podman run -d --name simple-chat -p 6969:6969 -p 7979:7979 simple-chat
fi

podman logs -f simple-chat
