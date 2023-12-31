# Use of this library: https://github.com/KonradIT/gopro-py-api
# flask --app gopro-shoot-video run
from goprocam import GoProCamera, constants
import time, os, json, logging, sys
from io import StringIO 
from flask import Flask, make_response, request
from flask_cors import CORS, cross_origin

# Pull Environmental variables
#export FLASK_RUN_PORT=8181
#export FLASK_RUN_HOST=0.0.0.0
flaskPort = os.environ.get("FLASK_RUN_PORT", 8181)
flaskHost = os.environ.get("FLASK_RUN_HOST", "0.0.0.0")
tlsCert = os.environ.get("FLASK_TLS_CERT", "")
tlsKey = os.environ.get("FLASK_TLS_KEY", "")

videoLength = os.environ.get("VIDEO_LENGTH", "15")
videoResolution = os.environ.get("VIDEO_RESOLUTION", "1080p")
videoFPS = os.environ.get("VIDEO_FPS", "30")
videoProtune = os.environ.get("VIDEO_PROTUNE", "OFF")
videoSavePath = os.environ.get("VIDEO_SAVE_PATH", "./")

# Configure logging
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger("gopro-control")

log.info("===== Starting GoPro Control")

# Log inputs
log.info("- Video Length: " + videoLength + "s")
log.info("- Video Resolution: " + videoResolution)
log.info("- Video FPS: " + videoFPS)
log.info("- Video ProTune: " + videoProtune)
log.info("- Video Save Path: " + videoSavePath)

# Initialize the Flask application
app = Flask(__name__)
CORS(app) # This will enable CORS for all routes

# Health check endpoint
@app.route("/healthz", methods = ['GET'])
def healthz():
    if request.method == 'GET':
        return "ok"

# Define a fn class that will trap the output of printed lines from 3rd party modules
class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout

# Define the video function that will record and transfer the video from the GoPro
def captureVideo():
    try:
        log.info("===== Initializing camera...")
        with Capturing() as output:
            goproCamera = GoProCamera.GoPro()
        log.info(output)

        # Check to see if it is already recording
        if goproCamera.IsRecording():
            log.info("Camera is already recording! Exiting...")
            json_data = '{"status":"failed", "msg": "Camera is already recording!"}'

        else:
            log.info("- Setting mode to video...")
            goproCamera.mode(constants.Mode.VideoMode)
            log.info("- Setting resolution to " + videoResolution + " @ " + videoFPS + "fps...")
            goproCamera.video_settings(videoResolution, videoFPS)

            if videoProtune == "OFF":
                log.info("- Setting ProTune to Off...")
                goproCamera.gpControlSet(constants.Video.PROTUNE_VIDEO, constants.Video.ProTune.OFF)
            else:
                log.info("- Setting ProTune to On...")
                goproCamera.gpControlSet(constants.Video.PROTUNE_VIDEO, constants.Video.ProTune.ON)

            log.info("- Setting FOV to linear...")
            goproCamera.gpControlSet(constants.Video.FOV, constants.Video.Fov.Linear)

            log.info("- Recording for " + videoLength + " seconds...")
            with Capturing() as output:
                recordedVideo = goproCamera.shoot_video(int(videoLength))

            epoch_time = str(int(time.time()))

            with Capturing() as output:
                goproCamera.downloadLastMedia(recordedVideo, custom_filename=videoSavePath + "GOPRO_" + epoch_time + ".MP4")
            log.info(output)

            json_data = '{"status":"success", "created_at": "' + epoch_time + '", "video_file": "GOPRO_' + epoch_time + '.MP4", "path": "' + os.path.abspath(videoSavePath) + '"}'
    except Exception as err:
        json_data = '{"status":"failed", "msg": "' + str(err) + '"}'
    finally:
        json_obj = json.loads(json_data)
    
    log.info(json_obj)
    return json.dumps(json_obj)

@app.route("/recordgopro", methods=["GET", "OPTIONS"])
def recordgopro():
    rc = captureVideo()
    return rc

#captureVideo()

if __name__ == "__main__":
    if tlsCert != "" and tlsKey != "":
        print("Starting GoPro Control on port " + str(flaskPort) + " and host " + str(flaskHost) + " with TLS cert " + str(tlsCert) + " and TLS key " + str(tlsKey))
        app.run(ssl_context=(str(tlsCert), str(tlsKey)), port=flaskPort, host=flaskHost)
    else:
        print("Starting GoPro Control on port " + str(flaskPort) + " and host " + str(flaskHost))
        app.run(port=flaskPort, host=flaskHost)
