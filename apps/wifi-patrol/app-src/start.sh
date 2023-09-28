#!/bin/bash

echo "Starting wifi-patrol"

python3 main.py

#echo "FLASK_TLS_CERT: $FLASK_TLS_CERT"
#echo "FLASK_TLS_KEY: $FLASK_TLS_KEY"

#if [ -z "$FLASK_TLS_CERT" ]; then
#    echo "Starting wifi-patrol with TLS"
#    flask --app wifi-status --cert=$FLASK_TLS_CERT --key=$FLASK_TLS_KEY run
#else
#    echo "Starting wifi-patrol without TLS"
#    flask --app wifi-status run
#fi
