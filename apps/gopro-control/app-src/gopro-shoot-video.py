from goprocam import GoProCamera, constants

goproCamera = GoProCamera.GoPro()

if goproCamera.IsRecording():
    print("Camera is already recording!")
else:
    print("Recording for 10 seconds")
    goproCamera.shoot_video(10)
