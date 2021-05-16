#!/bin/bash

python webstreaming_openvino.py --ip 0.0.0.0 --port 8080 --prototxt MobileNetSSD_deploy.prototxt --model MobileNetSSD_deploy.caffemodel
