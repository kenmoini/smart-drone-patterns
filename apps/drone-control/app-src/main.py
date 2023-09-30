#import logging
from flask import Flask, request
from flask_cors import CORS, cross_origin
import os

app = Flask(__name__)
CORS(app) # This will enable CORS for all routes

#export FLASK_RUN_PORT=8080
#export FLASK_RUN_HOST=0.0.0.0
flaskPort = os.environ.get("FLASK_RUN_PORT", 8080)
flaskHost = os.environ.get("FLASK_RUN_HOST", "0.0.0.0")
tlsCert = os.environ.get("FLASK_TLS_CERT", "")
tlsKey = os.environ.get("FLASK_TLS_KEY", "")

@app.route("/healthz", methods = ['GET'])
def healthz():
    if request.method == 'GET':
        return "ok"

@app.route("/scan")
def scanner():
    rc = os.system("python3 droneScan.py")
    if rc == 0:
        return 'executed'
    else:
        return 'failed'

if __name__ == "__main__":
    if tlsCert != "" and tlsKey != "":
        print("Starting Drone Control on port " + str(flaskPort) + " and host " + str(flaskHost) + " with TLS cert " + str(tlsCert) + " and TLS key " + str(tlsKey))
        app.run(ssl_context=(str(tlsCert), str(tlsKey)), port=flaskPort, host=flaskHost)
    else:
        print("Starting Drone Control on port " + str(flaskPort) + " and host " + str(flaskHost))
        app.run(port=flaskPort, host=flaskHost)
