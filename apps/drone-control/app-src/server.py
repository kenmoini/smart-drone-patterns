#import logging
from flask import Flask
import os

app = Flask(__name__)

#export FLASK_RUN_PORT=8080
#export FLASK_RUN_HOST=0.0.0.0

@app.route("/scan")
def scanner():
    rc = os.system("python3 droneScan.py")
    if rc == 0:
        return 'executed'
    else:
        return 'failed'
