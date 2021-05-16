from flask import (
    Blueprint, render_template
)
import logging

import explorerhat as eh

# imports needed for stream server
import io
import picamera
import socketserver
from threading import Condition, Thread, Event
from http import server

car_engine = Blueprint('car_engine_app', __name__)

# for triggering the shutdown procedure when a signal is detected
keyboard_trigger = Event()


def signal_handler(signal, frame):
    logging.info('Signal detected. Stopping threads.')
    keyboard_trigger.set()


@car_engine.route("/")
@car_engine.route("/<state>")
def update_robot(state=None):
    if state == 'forward':
        eh.motor.one.backwards(100)
        eh.motor.two.forwards(100)
    if state == 'back':
        eh.motor.one.forwards(100)
        eh.motor.two.backwards(100)
    if state == 'left':
        eh.motor.two.stop()
        eh.motor.one.backwards(100)
    if state == 'right':
        eh.motor.one.stop()
        eh.motor.two.forwards(100)
    if state == 'stop':
        eh.motor.one.stop()
        eh.motor.two.stop()
    if state == 'anti-clockwise':
        eh.motor.one.backwards(100)
        eh.motor.two.backwards(100)
    if state == 'clockwise':
        eh.motor.one.forwards(100)
        eh.motor.two.forwards(100)
    template_data = {
        'title': state,
    }

    camera = picamera.PiCamera(resolution='1280x960', framerate=24)
    output = StreamingOutput()
    camera.start_recording(output, format='mjpeg')
    try:
        address = ('0.0.0.0', 8080)
        stream = StreamingServer(address, StreamingHandler)
        # starting the video streaming server
        streamServer = Thread(target=stream.serve_forever)
        streamServer.start()
        logging.info("Started stream server for picamera")
    finally:
        camera.stop_recording()

    return render_template('main.html', **template_data)


class StreamingOutput(object):
    """
    Class to which the video output is written to.
    The buffer of this class is then read by StreamingHandler continuously.
    """
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
    """
    Implementing GET request for the video stream.
    """
    def do_GET(self):
        if self.path == '/stream.mjpg':
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



