# Web streaming example
# Source code from the official PiCamera package
# http://picamera.readthedocs.io/en/latest/recipes2.html#web-streaming

import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server
from centroid_tracker.centroid_tracker import CentroidTracker
#from imutils.video import VideoStream
import numpy as np
import argparse
#import imutils
import time
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True, help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True, help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.5, help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# initialize our centroid tracker and frame dimensions
ct = CentroidTracker()
(H, W) = (None, None)
# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])
# initialize the video stream and allow the camera sensor to warmup
print("[INFO] starting video stream...")

PAGE = """\
<html>
<head>
<title>Autonomous Car Video Streaming</title>
</head>
<body>
<center>
    <h1>Autonomous Car Video Streaming</h1>
    <img src="stream.mjpg" width="640" height="480" />
</center>
</body>
</html>
"""


class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)


class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                        if W is None or H is None:
                                (H, W) = frame.shape[:2]
                        # construct a blob from the frame, pass it through the network,
                        # obtain our output predictions, and initialize the list of
                        # bounding box rectangles
                        blob = cv2.dnn.blobFromImage(frame, 1.0, (W, H),
                                                     (104.0, 177.0, 123.0))
                        net.setInput(blob)
                        detections = net.forward()
                        rects = []
                        # loop over the detections
                        for i in range(0, detections.shape[2]):
                            # filter out weak detections by ensuring the predicted
                            # probability is greater than a minimum threshold
                            if detections[0, 0, i, 2] > args["confidence"]:
                                # compute the (x, y)-coordinates of the bounding box for
                                # the object, then update the bounding box rectangles list
                                box = detections[0, 0, i, 3:7] * np.array([W, H, W, H])
                                rects.append(box.astype("int"))
                                # draw a bounding box surrounding the object so we can
                                # visualize it
                                (startX, startY, endX, endY) = box.astype("int")
                                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                        # update our centroid tracker using the computed set of bounding
                        # box rectangles
                        objects = ct.update(rects)
                        # loop over the tracked objects
                        for (objectID, centroid) in objects.items():
                            # draw both the ID of the object and the centroid of the
                            # object on the output frame
                            text = "ID {}".format(objectID)
                            cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                            cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
                        # show the output frame
                        cv2.imshow("Frame", frame)
                        key = cv2.waitKey(1) & 0xFF
                        # if the `q` key was pressed, break from the loop
                        if key == ord("q"):
                            break
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()


class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


with picamera.PiCamera(resolution='1280x960', framerate=24) as camera:
    output = StreamingOutput()
    camera.start_recording(output, format='mjpeg')
    try:
        address = ('', 80)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()

