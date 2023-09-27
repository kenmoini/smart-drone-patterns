# Use of this library: https://github.com/KonradIT/gopro-py-api
from goprocam import GoProCamera, constants
import time, os, json, logging
from io import StringIO 

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
log = logging.getLogger("gopro-control")

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout

log.info("===== Starting GoPro Control")

videoLength = os.environ.get("VIDEO_LENGTH", "15")
videoResolution = os.environ.get("VIDEO_RESOLUTION", "1080p")
videoFPS = os.environ.get("VIDEO_FPS", "30")
videoProtune = os.environ.get("VIDEO_PROTUNE", "OFF")
videoSavePath = os.environ.get("VIDEO_SAVE_PATH", "./")

log.info("- Video Length: " + videoLength + "s")
log.info("- Video Resolution: " + videoResolution)
log.info("- Video FPS: " + videoFPS)
log.info("- Video ProTune: " + videoProtune)
log.info("- Video Save Path: " + videoSavePath)

log.info("===== Initializing camera...")

with Capturing() as output:
    goproCamera = GoProCamera.GoPro()

def captureVideo():
    try:
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
            recordedVideo = goproCamera.shoot_video(int(videoLength))

            epoch_time = str(int(time.time()))
            dlMedia = goproCamera.downloadLastMedia(recordedVideo, custom_filename=videoSavePath + "GOPRO_" + epoch_time + ".MP4")

            json_data = '{"status":"success", "created_at": "' + epoch_time + '", "video_file": "GOPRO_' + epoch_time + '.MP4"}'
    except Exception as err:
        json_data = '{"status":"failed", "msg": "' + err + '"}'
    finally:
        json_obj = json.loads(json_data)

    print(json.dumps(json_obj))

captureVideo()
