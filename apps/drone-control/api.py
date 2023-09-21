from djitellopy import Tello
from threading import Thread
import time, cv2
#import logging

#Tello.LOGGER.setLevel(logging.DEBUG)

epoch_time = str(int(time.time()))
keepRecording = True

print("Instanciating Tello...")
drone = Tello()

print("Connecting to Tello...")
drone.connect()

print("Battery: " + str(drone.get_battery()) + "%")

print("Starting video stream...")
drone.streamon()

def videoRecorder():
    frame_read = drone.get_frame_read()
    height, width, _ = frame_read.frame.shape
    #force = cv2.VideoWriter_fourcc(*'XVID')
    #fourcc = cv2.VideoWriter_fourcc(*"avc1")
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video = cv2.VideoWriter('video-'+epoch_time+'.mp4', fourcc, 30, (width, height))

    while keepRecording:
        video.write(frame_read.frame)
        time.sleep(1 / 30)

    video.release()

recorder = Thread(target=videoRecorder)

def scanSurroundings():
    while True:
        try:
            drone.takeoff()
            time.sleep(3)
            drone.rotate_counter_clockwise(45)
            time.sleep(3)
            drone.rotate_counter_clockwise(45)
            time.sleep(3)
            drone.rotate_counter_clockwise(45)
            time.sleep(3)
            drone.rotate_counter_clockwise(45)
            time.sleep(3)
            drone.rotate_clockwise(180)
            time.sleep(3)
            drone.land()
            drone.streamoff()
            drone.end()
            keepRecording = False
            recorder.join()
        except:
            drone.streamoff()
            drone.end()
            keepRecording = False
            recorder.join()
        

recorder.start()

scanSurroundings()
time.sleep(18)

keepRecording = False
recorder.join()
