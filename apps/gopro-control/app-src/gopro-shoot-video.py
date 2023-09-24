from goprocam import GoProCamera, constants
import time, os

videoLength = os.environ.get("VIDEO_LENGTH", "15")
pathToSavedVideos = os.environ.get("PATH_TO_SAVED_VIDEOS", "videos")

goproCamera = GoProCamera.GoPro()

if goproCamera.IsRecording():
    print("Camera is already recording! Exiting...")
else:
    print("Recording for " + videoLength + " seconds")
    recordedVideo = goproCamera.shoot_video(int(videoLength))

    epoch_time = str(int(time.time()))
    goproCamera.downloadLastMedia(recordedVideo, path=pathToSavedVideos, custom_filename="GOPRO_" + epoch_time + ".MP4")
