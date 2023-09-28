import subprocess
import json
from flask import Flask
from flask_cors import CORS, cross_origin

# creates a Flask application
#export FLASK_RUN_PORT=8282
#export FLASK_RUN_HOST=0.0.0.0

app = Flask(__name__)
CORS(app) # This will enable CORS for all routes

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
