import os, json
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from twilio.rest import Client

##############################
# Setup Flask Variables
flaskPort = os.environ.get("FLASK_RUN_PORT", 8675)
flaskHost = os.environ.get("FLASK_RUN_HOST", "0.0.0.0")
tlsCert = os.environ.get("FLASK_TLS_CERT", "")
tlsKey = os.environ.get("FLASK_TLS_KEY", "")

##############################
# Setup Twilio Variables
twilioAccountSid = os.environ.get("TWILIO_ACCOUNT_SID", "")
twilioAuthToken = os.environ.get("TWILIO_AUTH_TOKEN", "")
twilioFromNumber = os.environ.get("TWILIO_FROM_NUMBER", "")

##############################
# Setup Twilio Client
if twilioAccountSid != "" and twilioAuthToken != "" and twilioFromNumber != "":
    twilioClient = Client(twilioAccountSid, twilioAuthToken)
else:
    print("Twilio variables not set, cannot creating Twilio client")
    raise Exception("TwilioParamError")

##############################
# Send a message with the Twilio API
def sendTextMessage(toNumber, msgBody):
  message = twilioClient.messages.create(
    from_=twilioFromNumber,
    body=msgBody,
    to=toNumber
  )
  return message

##############################
# creates a Flask application
app = Flask(__name__)
CORS(app) # This will enable CORS for all routes

# Health check endpoint
@app.route("/healthz", methods = ['GET'])
def healthz():
    if request.method == 'GET':
        return "ok"

# Index endpoint
@app.route("/")
def index():
    return "Shooby dooby dooby doo!"

# Send a text message endpoint
@app.route("/sendTextMessage", methods = ['POST'])
def sendTextMessageRoute():
    if request.method == 'POST':
        # Get the JSON data from the POST request
        data = request.get_json()
        # Pull the phone number and message body from the JSON data
        toNumber = data['toNumber']
        msgBody = data['msgBody']
        # Send the text message
        message = sendTextMessage(toNumber, msgBody)
        print(message)
        # Return the JSON message
        return json.dumps(message.sid)

##############################
## Start the application when the pythong script is run
if __name__ == "__main__":
    if tlsCert != "" and tlsKey != "":
        print("Starting Banana Phone on port " + str(flaskPort) + " and host " + str(flaskHost) + " with TLS cert " + str(tlsCert) + " and TLS key " + str(tlsKey))
        app.run(ssl_context=(str(tlsCert), str(tlsKey)), port=flaskPort, host=flaskHost)
    else:
        print("Starting Banana Phone on port " + str(flaskPort) + " and host " + str(flaskHost))
        app.run(port=flaskPort, host=flaskHost)
