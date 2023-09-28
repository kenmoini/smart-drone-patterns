# Use of this library: https://github.com/KonradIT/gopro-py-api
# flask --app server run
import time, os, json, logging, sys
from io import StringIO
from flask import Flask
from flask import render_template
from flask_cors import CORS, cross_origin

# Pull Environmental variables
#export FLASK_RUN_PORT=9191
#export FLASK_RUN_HOST=0.0.0.0
#export S3_SHIPPER_ENDPOINT=
#export GOPRO_CONTROL_ENDPOINT=
#export DRONE_CONTROL_ENDPOINT=

s3ShipperEndpoint = os.environ.get("S3_SHIPPER_ENDPOINT", "someURL")
goproControlEndpoint = os.environ.get("GOPRO_CONTROL_ENDPOINT", "http://egd.kemo.edge:8181/recordgopro")
droneControlEndpoint = os.environ.get("DRONE_CONTROL_ENDPOINT", "someURL")

# creates a Flask application
app = Flask(__name__)
CORS(app) # This will enable CORS for all routes

@app.route("/")
def index():
    return render_template('index.html')

# Config glue shit
@app.route("/config")
def config():
    # Assemble a JSON string
    data = '{"s3Shipper": {"endpoint": "' + s3ShipperEndpoint + '"}, "goproControl": {"endpoint": "' + goproControlEndpoint + '"}, "droneControl": {"endpoint": "' + droneControlEndpoint + '"} }'
    return data

# GoPro shit
@app.route("/edge-delivery")
def edgeDelivery():
    return render_template('edge-delivery.html')

# Architecture shit
@app.route("/architecture")
def architecture():
    return render_template('architecture.html')

# Drone shit
@app.route("/mobile-edge")
def mobileEdge():
    return render_template('mobile-edge.html')

# Pipeline shit
@app.route("/mlops")
def mlops():
    return render_template('mlops.html')
