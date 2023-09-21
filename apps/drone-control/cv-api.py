#import logging
from djitellopy import Tello
from threading import Thread
import time, cv2
from flask import Flask

app = Flask(__name__)

#export FLASK_RUN_PORT=8080
#export FLASK_RUN_HOST=0.0.0.0

#Tello.LOGGER.setLevel(logging.DEBUG)

epoch_time = str(int(time.time()))
keepRecording = True
 
print("Instanciating Tello...")
drone = Tello()

# videoRecorderCV works with djitrellopy 2.4.0
def videoRecorderCV():
    frame_read = drone.get_frame_read()
    height, width, _ = frame_read.frame.shape
    #fourcc = cv2.VideoWriter_fourcc(*'XVID')
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video = cv2.VideoWriter('video-'+epoch_time+'.mp4', fourcc, 30, (width, height))

    while keepRecording:
        video.write(frame_read.frame)
        time.sleep(1 / 30)

    video.release()

def scanSurroundings():
    try:
        print("Running flight pattern")
        print("Taking off...")
        drone.takeoff()
        print("Sleeping for 3 seconds...")
        time.sleep(3)
        #drone.rotate_counter_clockwise(45)
        #time.sleep(1)
        #drone.rotate_counter_clockwise(45)
        #time.sleep(1)
        #drone.rotate_counter_clockwise(45)
        #time.sleep(1)
        #drone.rotate_counter_clockwise(45)
        #time.sleep(1)
        #drone.rotate_counter_clockwise(360)
        print("Rotating...")
        drone.send_rc_control(0, 0, 0, 30)
        print("Sleeping for 12 seconds...")
        time.sleep(12)
        print("Landing...")
        drone.land()
    except:
        print("Hit exception in flight pattern execution!")
        #drone.land()

@app.route("/execute-scan")
def executeScan():
    keepRecording = True

    print("Connecting to Tello...")
    drone.connect()

    print("Battery: " + str(drone.get_battery()) + "%")

    print("Starting video stream...")

    # These are SDK 3 and 2.5.0 functions
    # Resolution can be set via the mobile app which will persist between restarts
    #drone.set_video_resolution(Tello.RESOLUTION_720P)
    #drone.set_video_fps(Tello.FPS_30)
    #drone.set_video_bitrate(Tello.BITRATE_5MBPS)
    drone.streamon()

    print("Starting recording...")
    recorder = Thread(target=videoRecorderCV)
    recorder.start()

    print("Sleeping for 10 seconds...")
    time.sleep(10)

    print("Starting scanning...")
    scanSurroundings()

    print("Terminating recording...")
    keepRecording = False
    recorder.join()

    drone.streamoff()


@app.route("/drone-scan")
def droneScan():
    # epoch_time = str(int(time.time()))
    # keepRecording = True

    print("Instanciating Tello...")
    drone = Tello()

    print("Connecting to Tello...")
    drone.connect()

    print("Battery: " + str(drone.get_battery()) + "%")

    print("Starting video stream...")

    # These are SDK 3 and 2.5.0 functions
    # Resolution can be set via the mobile app which will persist between restarts
    #drone.set_video_resolution(Tello.RESOLUTION_720P)
    #drone.set_video_fps(Tello.FPS_30)
    #drone.set_video_bitrate(Tello.BITRATE_5MBPS)
    drone.streamon()

    print("Starting recording...")
    recorder = Thread(target=videoRecorderCV)
    recorder.start()

    print("Sleeping for 10 seconds...")
    time.sleep(10)

    print("Starting scanning...")
    scanSurroundings()

    print("Terminating recording...")
    keepRecording = False
    recorder.join()

    drone.streamoff()
