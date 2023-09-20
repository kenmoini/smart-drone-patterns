from djitellopy import Tello
from threading import Thread
import time, cv2
#import logging

#Tello.LOGGER.setLevel(logging.DEBUG)

epoch_time = str(time.time())
keepRecording = True

print("Instanciating Tello...")
drone = Tello()

print("Connecting to Tello...")
drone.connect()

print(drone.get_battery())

#print("Battery: " + str(drone.get_battery()) + "%")

print("Starting video stream...")
drone.streamon()

def videoRecorder():
    frame_read = drone.get_frame_read()
    height, width, _ = frame_read.frame.shape
    force = cv2.VideoWriter_fourcc(*'XVID')
    #fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    #video = cv2.VideoWriter('video-'+epoch_time+'.avi', cv2.VideoWriter_fourcc(*'avc1'), 30, (width, height))
    video = cv2.VideoWriter('video-'+epoch_time+'.avi', force, 20.0, (width, height))
    #frame = cv2.flip(frame, 0)
    #video = cv2.VideoWriter('video-'+epoch_time+'.mp4', fourcc, 30, (width, height))

    while keepRecording:
        video.write(frame_read.frame)
        time.sleep(1 / 30)

    video.release()

def scanSurroundings():
    drone.takeoff()
    drone.rotate_counter_clockwise(45)
    time.sleep(1)
    drone.rotate_counter_clockwise(45)
    time.sleep(1)
    drone.rotate_counter_clockwise(45)
    time.sleep(1)
    drone.rotate_counter_clockwise(45)
    time.sleep(1)
    drone.rotate_clockwise(180)
    drone.land()

recorder = Thread(target=videoRecorder)
recorder.start()

#scanSurroundings()

time.sleep(30)

keepRecording = False
recorder.join()

drone.streamoff()