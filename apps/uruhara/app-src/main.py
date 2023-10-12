# Uruhara runs the model inference and then parses the output. It then returns the parsed output in JSON format.
from pprint import pprint
import pathlib, json
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

        # Determine predicted file name
        predictedFileName = data['fileName'].replace("inf_", "pred_")
        # expects {"fileType": "video", "fileName": "/shared-data/GOPRO_VID069420.mp4"}
        if data['fileType'] == "video":
            print("Processing video file: " + data['fileName'])
            status['fileType'] = 'video'

            predictionDataFileName = os.path.splitext(data['fileName'].replace("inf_", "pred_"))[0] + ".txt"
            predictionJSONFileName = os.path.splitext(data['fileName'].replace("inf_", "pred_"))[0] + ".json"

            rc = os.system("darknet detector demo -dont_show ./models/hats/hats.data ./models/hats/hats.cfg ./models/hats/hats_best.weights " + data['fileName'] + " -out_filename " + predictedFileName + " -ext_output > " + predictionDataFileName)
            if rc == 0:
                status['darknet'] = 'ok'
                status['predictedFileName'] = predictedFileName
                # Next run the parser
                prc = os.system("python3 parse_output.py -i " + predictionDataFileName + " -o " + predictionJSONFileName)
                if prc == 0:
                    status['outputParser'] = 'ok'
                    status['predictionJSONFileName'] = predictionJSONFileName
                    status['predictionData'] = json.load(open(predictionJSONFileName, "r"))
                else:
                    status['outputParser'] = 'failed'
            else:
                status['darknet'] = 'failed'

        elif data['fileType'] == "image":
            print("Processing image file: " + data['fileName'])
            status['fileType'] = 'image'

            colorSwappedFilename = os.path.splitext(predictedFileName)[0] + "-swapped." + os.path.splitext(predictedFileName)[1]
            predictionJSONFileName = os.path.splitext(predictedFileName)[0] + ".json"

            rc = os.system("darknet detector test -dont_show ./models/hats/hats.data ./models/hats/hats.cfg ./models/hats/hats_best.weights " + data['fileName'] + " -out " + predictionJSONFileName)
            if rc == 0:
                status['darknet'] = 'ok'
                # Copy the prediction.jpg file to where the predicted file name is
                os.system("cp predictions.jpg " + predictedFileName)
                status['predictedFileName'] = predictedFileName
                status['predictionJSONFileName'] = predictionJSONFileName

                # Next run the script to swap the colorspace
                scrc = os.system("python3 swap-colorspace.py -i " + predictedFileName + " -o " + colorSwappedFilename)
                if scrc == 0:
                    status['swapColorspace'] = 'ok'
                    status['swappedFileName'] = colorSwappedFilename
                else:
                    status['swapColorspace'] = 'failed'
            else:
                status['darknet'] = 'failed'
        
        return status

# Start the server
if __name__ == "__main__":
    if tlsCert != "" and tlsKey != "":
        print("Starting Uruhara on port " + str(flaskPort) + " and host " + str(flaskHost) + " with TLS cert " + str(tlsCert) + " and TLS key " + str(tlsKey))
        app.run(ssl_context=(str(tlsCert), str(tlsKey)), port=flaskPort, host=flaskHost)
    else:
        print("Starting Uruhara on port " + str(flaskPort) + " and host " + str(flaskHost))
        app.run(port=flaskPort, host=flaskHost)
