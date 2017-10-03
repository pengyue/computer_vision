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
        self.video = self.VideoCapture()
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')

    def VideoCapture(self):
        video = cv2.VideoCapture(0)
        video.set(3, 340)
        video.set(4, 240)

        return video

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, frame = self.video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        if faces is not ():
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
