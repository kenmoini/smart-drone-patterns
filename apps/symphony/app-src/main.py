# Use of this library: https://github.com/KonradIT/gopro-py-api
# flask --app server run
import time, os, json, logging, sys
from io import StringIO
from flask import Flask, render_template
from flask_cors import CORS, cross_origin

# Pull Environmental variables
#export FLASK_RUN_PORT=9191
#export FLASK_RUN_HOST=0.0.0.0

flaskPort = os.environ.get("FLASK_RUN_PORT", 8282)
flaskHost = os.environ.get("FLASK_RUN_HOST", "0.0.0.0")
tlsCert = os.environ.get("FLASK_TLS_CERT", "")
tlsKey = os.environ.get("FLASK_TLS_KEY", "")

#export S3_SHIPPER_ENDPOINT=
#export GOPRO_CONTROL_ENDPOINT=
#export DRONE_CONTROL_ENDPOINT=
#export WIFI_STATUS_ENDPOINT=

#goproControlEndpoint = os.environ.get("GOPRO_CONTROL_ENDPOINT", "http://egd.kemo.edge:8181/recordgopro")
#droneControlEndpoint = os.environ.get("DRONE_CONTROL_ENDPOINT", "http://egd.kemo.edge:8080/scan")
droneControlEndpoint = os.environ.get("DRONE_CONTROL_ENDPOINT", "https://drone-control.apps.egd.kemo.edge:8080/scan")
droneControlTargetAP = os.environ.get("DRONE_CONTROL_TARGET_AP", "TELLO-9AFD00")
droneControlTargetBucket = os.environ.get("DRONE_CONTROL_TARGET_BUCKET", "drone-videos")

goproControlEndpoint = os.environ.get("GOPRO_CONTROL_ENDPOINT", "https://gopro-control.apps.egd.kemo.edge:8181/recordgopro")
goproControlTargetAP = os.environ.get("GOPRO_CONTROL_TARGET_AP", "kemoGoProH7B")
goproControlTargetBucket = os.environ.get("GOPRO_CONTROL_TARGET_BUCKET", "gopro-videos")

wifiStatusEndpoint = os.environ.get("WIFI_STATUS_ENDPOINT", "https://wifi-status.apps.egd.kemo.edge:8282/status")
s3ShipperEndpoint = os.environ.get("S3_SHIPPER_ENDPOINT", "https://s3-shipper-s3-shipper.apps.sno.kemo.edge/upload")


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
    data = '{"s3Shipper": {"endpoint": "' + s3ShipperEndpoint + '"}, "goproControl": {"endpoint": "' + goproControlEndpoint + '", "targetAP": "' + goproControlTargetAP + '", "targetBucket": "' + goproControlTargetBucket + '"}, "droneControl": {"endpoint": "' + droneControlEndpoint + '", "targetAP": "' + droneControlTargetAP + '"}, "wifiStatus": {"endpoint": "' + wifiStatusEndpoint + '"} }'
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

if __name__ == "__main__":
    if tlsCert != "" and tlsKey != "":
        print("Starting Symphony on port " + str(flaskPort) + " and host " + str(flaskHost) + " with TLS cert " + str(tlsCert) + " and TLS key " + str(tlsKey))
        app.run(ssl_context=(str(tlsCert), str(tlsKey)), port=flaskPort, host=flaskHost)
    else:
        print("Starting Symphony on port " + str(flaskPort) + " and host " + str(flaskHost))
        app.run(port=flaskPort, host=flaskHost)
