from goprocam import GoProCamera, constants
import time, os

videoLength = os.environ.get("VIDEO_LENGTH", "15")
videoResolution = os.environ.get("VIDEO_RESOLUTION", "1080p")
videoFPS = os.environ.get("VIDEO_FPS", "30")

goproCamera = GoProCamera.GoPro()

print("Setting mode to video...")
goproCamera.mode(constants.Mode.VideoMode)
print("Setting resolution to " + videoResolution + " @ " + videoFPS + "fps...")
goproCamera.video_settings(videoResolution, videoFPS)

# IDK how this works
#print("Setting FOV to linear...")
goproCamera.gpControlSet(constants.Video.PROTUNE_VIDEO, constants.Video.ProTune.ON)
goproCamera.gpControlSet(constants.Hero3Status.FOV, "00")
#goproCamera.parse_value(constants.Hero3Status.FOV, "90")

if goproCamera.IsRecording():
    print("Camera is already recording! Exiting...")
else:
    print("Recording for " + videoLength + " seconds")
    recordedVideo = goproCamera.shoot_video(int(videoLength))

    epoch_time = str(int(time.time()))
    goproCamera.downloadLastMedia(recordedVideo, custom_filename="GOPRO_" + epoch_time + ".MP4")
