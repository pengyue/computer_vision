import signal
import sys
import logging
from time import sleep

# check if it's ran with Python3
assert sys.version_info[0:1] == (3,)

# imports needed for web server
from flask import Flask, jsonify, render_template, request, Response, send_from_directory, url_for
from threading import Thread, Event

import picamera

from src.video.streaming import StreamingOutput, StreamingServer, StreamingHandler
from src.car.engine import WebServerThread

logging.basicConfig(level=logging.DEBUG)

# for triggering the shutdown procedure when a signal is detected
keyboard_trigger = Event()


def signal_handler(signal, frame):
    logging.info('Signal detected. Stopping threads.')
    keyboard_trigger.set()


HOST = "0.0.0.0"
WEB_PORT = 5000
STREAM_PORT = 5001
app = Flask(__name__, static_url_path='')

#############################
### Aggregating all calls ###
#############################

if __name__ == "__main__":
    # registering both types of signals
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # firing up the video camera (pi camera)
    camera = picamera.PiCamera(resolution='960x480', framerate=30)
    output = StreamingOutput()
    camera.start_recording(output, format='mjpeg')
    logging.info("Started recording with picamera")
    stream = StreamingServer((HOST, STREAM_PORT), StreamingHandler)

    # starting the video streaming server
    streamserver = Thread(target=stream.serve_forever)
    streamserver.start()
    logging.info("Started stream server for picamera")

    # starting the web server
    webserver = WebServerThread(app, HOST, WEB_PORT)
    webserver.start()
    logging.info("Started Flask web server")

    # and run it indefinitely
    while not keyboard_trigger.is_set():
        sleep(0.5)

    # until some keyboard event is detected
    logging.info("Keyboard event detected")

    # trigger shutdown procedure
    webserver.shutdown()
    camera.stop_recording()
    stream.shutdown()

    # and finalize shutting them down
    webserver.join()
    streamserver.join()
    logging.info("Stopped all threads")

    sys.exit(0)
