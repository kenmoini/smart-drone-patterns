from pprint import pprint
import pathlib, json
import os, uuid
from flask import Flask, request, send_file
from flask_cors import CORS, cross_origin
from roboflow import Roboflow

####################
## Setup Flask Variables
flaskHost = os.environ.get("FLASK_RUN_HOST", "0.0.0.0")
flaskPort = os.environ.get("FLASK_RUN_PORT", 7272)
tlsCert = os.environ.get("FLASK_TLS_CERT", "")
tlsKey = os.environ.get("FLASK_TLS_KEY", "")

####################
## Setup Roboflow Variables
roboflowAPIKey = os.environ.get("RF_API_KEY", "")
roboflowProject = os.environ.get("RF_PROJECT", "")
roboflowModelVersion = os.environ.get("RF_MODEL_VERSION", 1)
roboflowDataDirectory = os.environ.get("RF_DATA_DIRECTORY", "/tmp/roboflow/data")

####################
## Setup Roboflow Connector
pathlib.Path(roboflowDataDirectory).mkdir(parents=True, exist_ok=True)
rf = Roboflow(api_key=roboflowAPIKey)
project = rf.workspace().project(roboflowProject)
model = project.version(int(roboflowModelVersion)).model

####################
## Setup Flask
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

@app.route("/inference", methods = ['GET', 'POST'])
def inference():
    # We're getting the image of a requested inference
    if request.method == 'GET':
        # Get the image URL
        imageName = request.args.get('imageName')

        # Get the image file
        imageFilepath = roboflowDataDirectory + "/" + imageName

        # Return the image
        return send_file(imageFilepath)

    elif request.method == 'POST':            
        # We'll be receiving an image file, then returning some JSON with the results
        # Get the image file and request data
        imageFile = request.files['image']
        r_confidence = request.args.get('confidence') or 40
        r_overlap = request.args.get('overlap') or 30

        # Get the extension of the file
        imageFileExtension = imageFile.filename.split(".")[-1]
        # Set a unique filename
        filename = str(uuid.uuid4())
        originalFileName = filename + "." + imageFileExtension
        inferenceFilename = "p_" + originalFileName
        filepath = roboflowDataDirectory + "/" + originalFileName
        inferenceFilepath = roboflowDataDirectory + "/" + inferenceFilename
        # Save the image to a file
        imageFile.save(filepath)
        # Run the inference and get the JSON data
        inference = model.predict(filepath, confidence=int(r_confidence), overlap=int(r_overlap))
        inferenceJSON = inference.json()
        inference.save(inferenceFilepath)

        # Create the response JSON
        response = {}
        response["hash"] = filename
        response["original"] = originalFileName
        response["inference"] = inferenceFilename
        response["data"] = inferenceJSON

        # Return the response
        return response

# Start the server
if __name__ == "__main__":
    if tlsCert != "" and tlsKey != "":
        print("Starting Roboflow Robot on port " + str(flaskPort) + " and host " + str(flaskHost) + " with TLS cert " + str(tlsCert) + " and TLS key " + str(tlsKey))
        app.run(ssl_context=(str(tlsCert), str(tlsKey)), port=flaskPort, host=flaskHost)
    else:
        print("Starting Roboflow Robot on port " + str(flaskPort) + " and host " + str(flaskHost))
        app.run(port=flaskPort, host=flaskHost)


# Sample JSON response:
# {
#     "data": {
#         "image": {
#             "height": "430",
#             "width": "640"
#         },
#         "predictions": [
#             {
#                 "class": "railway",
#                 "class_id": 1,
#                 "confidence": 0.796828031539917,
#                 "height": 160.0,
#                 "image_path": "/tmp/roboflow/data/566576fa-c6fd-4273-b9a9-088e6285ed42.jpg",
#                 "prediction_type": "ObjectDetectionModel",
#                 "width": 284.0,
#                 "x": 498.0,
#                 "y": 350.0
#             }
#         ]
#     },
#     "hash": "566576fa-c6fd-4273-b9a9-088e6285ed42",
#     "inference": "p_566576fa-c6fd-4273-b9a9-088e6285ed42.jpg",
#     "original": "566576fa-c6fd-4273-b9a9-088e6285ed42.jpg"
# }