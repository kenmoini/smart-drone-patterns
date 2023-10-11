# 
from pprint import pprint
import pathlib
import os
from flask import Flask, request
from flask_cors import CORS, cross_origin

# export FLASK_RUN_PORT=8777
# export FLASK_RUN_HOST=0.0.0.0
# python3 main.py

flaskPort = os.environ.get("FLASK_RUN_PORT", 8777)
flaskHost = os.environ.get("FLASK_RUN_HOST", "0.0.0.0")
tlsCert = os.environ.get("FLASK_TLS_CERT", "")
tlsKey = os.environ.get("FLASK_TLS_KEY", "")

app = Flask(__name__)
CORS(app) # This will enable CORS for all routes

@app.route("/", methods = ['GET'])
def index():
    if request.method == 'GET':
        return "ok"

@app.route("/healthz", methods = ['GET'])
def healthz():
    if request.method == 'GET':
        return "ok"

@app.route("/process-inference", methods = ['POST'])
def upload():
    if request.method == 'POST':
        status = {}

        data = request.get_json()
        print(data)
        # expects {"fileType": "video", "fileName": "/shared-data/GOPRO_VID069420.mp4"}
        if data['fileType'] == "video":
            print("Processing video file: " + data['fileName'])

            rc = os.system("darknet version")
            if rc == 0:
                status['darknet'] = 'ok'
            else:
                status['darknet'] = 'failed'

        elif data['fileType'] == "image":
            print("Processing image file: " + data['fileName'])
        
        return status

# Start the server
if __name__ == "__main__":
    if tlsCert != "" and tlsKey != "":
        print("Starting Uruhara on port " + str(flaskPort) + " and host " + str(flaskHost) + " with TLS cert " + str(tlsCert) + " and TLS key " + str(tlsKey))
        app.run(ssl_context=(str(tlsCert), str(tlsKey)), port=flaskPort, host=flaskHost)
    else:
        print("Starting Uruhara on port " + str(flaskPort) + " and host " + str(flaskHost))
        app.run(port=flaskPort, host=flaskHost)
