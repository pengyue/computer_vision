from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import time
import sys
import numpy as np
import os

cas_path = os.getcwd()
cas_path += "/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cas_path)

class VideoCamera(object):

    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.

        self.PrintVersion()

        self.camera = PiCamera()

        # allow the camera to warmup
        time.sleep(0.1)
        lastTime = time.time()*1000.0

        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')

    def PrintVersion(self):
        # Print out OpenCV version
        print("OpenCV Version: {}".format(cv2.__version__))
        print("Python Version: {}".format(".".join(map(str, sys.version_info))))

    def get_frame(self):
        # initialize the camera and grab a reference to the raw camera capture
        self.camera.resolution = (160, 128)
        self.camera.framerate = 32
        rawCapture = PiRGBArray(self.camera, size=(160, 128))
        for frame in self.camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            image = frame.array
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags = cv2.CASCADE_SCALE_IMAGE
            )
            if faces is not ():
                for (x, y, w, h) in faces:
                    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

            ret, jpeg = cv2.imencode('.jpg', image)
            
            return jpeg.tobytes()

