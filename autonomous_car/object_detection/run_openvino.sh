#!/bin/bash

python webstreaming_openvino.py --ip 0.0.0.0 --port 8080 --prototxt training_model/MobileNetSSD_deploy.prototxt --model training_model/MobileNetSSD_deploy.caffemodel --movidius 1
