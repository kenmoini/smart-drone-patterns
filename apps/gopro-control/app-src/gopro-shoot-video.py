# Use of this library: https://github.com/KonradIT/gopro-py-api
from goprocam import GoProCamera, constants
import time, os, json

videoLength = os.environ.get("VIDEO_LENGTH", "15")
videoResolution = os.environ.get("VIDEO_RESOLUTION", "1080p")
videoFPS = os.environ.get("VIDEO_FPS", "30")
videoProtune = os.environ.get("VIDEO_PROTUNE", "OFF")

goproCamera = GoProCamera.GoPro()

if goproCamera.IsRecording():
    print("Camera is already recording! Exiting...")

else:
    print("Setting mode to video...")
    goproCamera.mode(constants.Mode.VideoMode)
    print("Setting resolution to " + videoResolution + " @ " + videoFPS + "fps...")
    goproCamera.video_settings(videoResolution, videoFPS)

    if videoProtune == "OFF":
        print("Setting ProTune to Off...")
        goproCamera.gpControlSet(constants.Video.PROTUNE_VIDEO, constants.Video.ProTune.OFF)
    else:
        print("Setting ProTune to On...")
        goproCamera.gpControlSet(constants.Video.PROTUNE_VIDEO, constants.Video.ProTune.ON)

    print("Setting FOV to linear...")
    goproCamera.gpControlSet(constants.Video.FOV, constants.Video.Fov.Linear)

    print("Recording for " + videoLength + " seconds")
    recordedVideo = goproCamera.shoot_video(int(videoLength))

    epoch_time = str(int(time.time()))
    goproCamera.downloadLastMedia(recordedVideo, custom_filename="GOPRO_" + epoch_time + ".MP4")

    json_data = '{"status":"success", "created_at": "' + epoch_time + '", "video_file": "GOPRO_' + epoch_time + '.MP4"}'

    json_obj = json.loads(json_data)

    print(json.dumps(json_obj, indent=2))