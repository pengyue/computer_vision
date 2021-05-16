#!/bin/bash

python webstreaming_centroid.py --ip 0.0.0.0 --port 8080 --prototxt training_model/deploy.prototxt --model training_model/res10_300x300_ssd_iter_140000.caffemodel
