from goprocam import GoProCamera, constants
import time

goproCamera = GoProCamera.GoPro()

if goproCamera.IsRecording():
    print("Camera is already recording! Exiting...")
else:
    print("Recording for 10 seconds")
    goproCamera.shoot_video(10)
    epoch_time = str(int(time.time()))
    goproCamera.downloadLastMedia('videos/', epoch_time)
