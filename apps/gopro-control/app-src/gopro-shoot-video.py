from goprocam import GoProCamera, constants
import time, os

videoLength = os.environ.get("VIDEO_LENGTH", "15")

goproCamera = GoProCamera.GoPro()

goproCamera.video_settings("1080p","30")
goproCamera.webcamFOV("02")

if goproCamera.IsRecording():
    print("Camera is already recording! Exiting...")
else:
    print("Recording for " + videoLength + " seconds")
    recordedVideo = goproCamera.shoot_video(int(videoLength))

    epoch_time = str(int(time.time()))
    goproCamera.downloadLastMedia(recordedVideo, custom_filename="GOPRO_" + epoch_time + ".MP4")
