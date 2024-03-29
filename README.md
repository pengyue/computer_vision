# image_processing

## Getting Started

These instructions will help you to install the library into your project.

### Installing

**OpenCV 3 and Python 3 are required to run those scripts, virtualenv and virtualenvwrapper are strongly recommended, to install OpenCV on Raspberry Pi, please refer to [Pyimageresearch](http://www.pyimagesearch.com/2016/04/18/install-guide-raspberry-pi-3-raspbian-jessie-opencv-3/)**



## Face Detection

### how to run on Raspberry Pi (Zero W)

python detect.py ../haarcascade_frontalface_default.xml

### how to rin on the PC with webcam

python detect.py -f ../haarcascade_frontalface_default.xml -e ../haarcascade_eye.xml

==============================================================

## Object Tracking

### how to run on local machine with webcam

python track.py

### how to run on local machine with video files

python track.py -v path-to-video-file -b buffer-size

===============================================================

## Pedestrian Detection

### how to run on local machine or Raspberry Pi (Zero W)

python detect.py -i path-to-images-files

===============================================================

## Game finder

python find_game.py

===============================================================

## Real time object detection

python real_time_object_detection.py --prototxt MobileNetSSD_deploy.prototxt.txt --model MobileNetSSD_deploy.caffemodel


==============================================================

## Streaming face detection into web browser (PC or RPi with webcam)

python main.py
