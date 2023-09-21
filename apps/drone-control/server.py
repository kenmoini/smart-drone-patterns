#import logging
from flask import Flask

app = Flask(__name__)

#export FLASK_RUN_PORT=8080
#export FLASK_RUN_HOST=0.0.0.0

@app.route("/scan")
def scanner():
    exec(open("droneScan.py").read())
