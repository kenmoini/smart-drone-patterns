from djitellopy import Tello
from threading import Thread
import time, cv2

tello = Tello()

tello.connect()

epoch_time = str(time.time())
keepRecording = True
tello.streamon()
frame_read = tello.get_frame_read()

def videoRecorder():
    height, width, _ = frame_read.frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    #fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    #video = cv2.VideoWriter('video-'+epoch_time+'.avi', cv2.VideoWriter_fourcc(*'avc1'), 30, (width, height))
    video = cv2.VideoWriter('video-'+epoch_time+'.avi', fourcc, 30, (width, height))
    #video = cv2.VideoWriter('video-'+epoch_time+'.mp4', fourcc, 30, (width, height))

    while keepRecording:
        video.write(frame_read.frame)
        time.sleep(1 / 30)

    video.release()

def scanSurroundings():
    tello.takeoff()
    tello.rotate_counter_clockwise(45)
    time.sleep(1)
    tello.rotate_counter_clockwise(45)
    time.sleep(1)
    tello.rotate_counter_clockwise(45)
    time.sleep(1)
    tello.rotate_counter_clockwise(45)
    time.sleep(1)
    tello.rotate_clockwise(180)
    tello.land()

recorder = Thread(target=videoRecorder)
recorder.start()

#scanSurroundings()

time.sleep(3)

keepRecording = False
recorder.join()

tello.streamoff()