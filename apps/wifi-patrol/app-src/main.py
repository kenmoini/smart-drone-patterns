import subprocess, json, os
from flask import Flask, request
from flask_cors import CORS, cross_origin

# creates a Flask application
#export FLASK_RUN_PORT=8282
#export FLASK_RUN_HOST=0.0.0.0

flaskPort = os.environ.get("FLASK_RUN_PORT", 8282)
flaskHost = os.environ.get("FLASK_RUN_HOST", "0.0.0.0")
tlsCert = os.environ.get("FLASK_TLS_CERT", "")
tlsKey = os.environ.get("FLASK_TLS_KEY", "")

app = Flask(__name__)
CORS(app) # This will enable CORS for all routes

# Health check endpoint
@app.route("/healthz", methods = ['GET'])
def healthz():
    if request.method == 'GET':
        return "ok"

def scanForWifi():
    # Get the list of wifi access points
    meta_data = subprocess.check_output(['nmcli', 'dev', 'wifi', 'list'])
    data = meta_data.decode('utf-8', errors ="backslashreplace")
    data = data.split('\n')

    activeNetwork = []
    allNetworks = []

    for i in data:
        allNetworks.append(i.strip().split())
        if i.startswith('*'):
            activeNetwork.append(i.strip().split())

    json_obj = {"allNetworks": allNetworks, "activeNetwork": activeNetwork}
    #json_obj = json.loads(json_data)

    return json.dumps(json_obj)

@app.route("/status")
def statusCheck():
    return scanForWifi()

if __name__ == "__main__":
    if tlsCert != "" and tlsKey != "":
        print("Starting Wifi Patrol on port " + str(flaskPort) + " and host " + str(flaskHost) + " with TLS cert " + str(tlsCert) + " and TLS key " + str(tlsKey))
        app.run(ssl_context=(str(tlsCert), str(tlsKey)), port=flaskPort, host=flaskHost)
    else:
        print("Starting Wifi Patrol on port " + str(flaskPort) + " and host " + str(flaskHost))
        app.run(port=flaskPort, host=flaskHost)