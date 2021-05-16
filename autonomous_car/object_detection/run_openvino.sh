#!/bin/bash

python webstreaming_openvino.py --ip 0.0.0.0 --port 8080 --prototxt training/MobileNetSSD_deploy.prototxt --model training/MobileNetSSD_deploy.caffemodel
