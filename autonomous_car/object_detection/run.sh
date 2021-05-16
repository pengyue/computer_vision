#!/bin/bash

sudo ~/.virtualenvs/py3cv4/bin/python3  rpi_camera_object_detection.py --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel
