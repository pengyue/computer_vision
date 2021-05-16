#!/usr/bin python
from importlib import import_module
import os
from flask import (
    Blueprint, render_template, Response
)

video_streaming = Blueprint('video_streaming_app', __name__)

# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('src.video.camera.camera_' + os.environ['CAMERA']).Camera
else:
    from src.video.camera.camera import Camera


@video_streaming.route('/')
def index():
    """Video streaming home page."""
    return render_template('main.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@video_streaming.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')