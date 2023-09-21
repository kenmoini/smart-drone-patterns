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

# videoRecorderCV works with djitrellopy 2.4.0
def videoRecorderCV():
    frame_read = drone.get_frame_read()
    height, width, _ = frame_read.frame.shape
    #fourcc = cv2.VideoWriter_fourcc(*'XVID')
    #fourcc = cv2.VideoWriter_fourcc(*"avc1")
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video = cv2.VideoWriter('video-'+epoch_time+'.mp4', fourcc, 30, (width, height))

    while keepRecording:
        video.write(frame_read.frame)
        time.sleep(1 / 30)

    video.release()

def scanSurroundings():
    try:
        print("Running flight pattern")
        drone.takeoff()
        time.sleep(3)
        drone.rotate_counter_clockwise(45)
        time.sleep(1)
        drone.rotate_counter_clockwise(45)
        time.sleep(1)
        drone.rotate_counter_clockwise(45)
        time.sleep(1)
        drone.rotate_counter_clockwise(45)
        time.sleep(1)
        drone.rotate_clockwise(180)
        time.sleep(3)
        drone.land()
    except:
        print("Hit exception in flight pattern execution!")

print("Starting recording...")
recorder = Thread(target=videoRecorderCV)
recorder.start()

print("Sleeping for 15 seconds...")
time.sleep(15)

print("Starting scanning...")
scanSurroundings()

print("Terminating recording...")
keepRecording = False
recorder.join()

drone.streamoff()
