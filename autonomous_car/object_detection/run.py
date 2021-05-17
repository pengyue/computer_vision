from application import create_app
import threading
import argparse

# construct the argument parser and parse command line arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--ip", type=str, required=True, help="ip address of the device")
ap.add_argument("-o", "--port", type=int, required=True, help="ephemeral port number of the server (1024 to 65535)")
ap.add_argument("-f", "--frame-count", type=int, default=32, help="# of frames used to construct the background model")
ap.add_argument("-p", "--prototxt", type=str, required=True, help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", type=str, required=True, help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.2, help="minimum probability to filter weak detections")
ap.add_argument("-u", "--movidius", type=bool, default=0, help="boolean indicating if the Movidius should be used")
args = vars(ap.parse_args())

app = create_app()

app.config.from_mapping(
    IP=args["ip"],
    PORT=args["port"],
    FRAME_COUNT=32,
    PROTOTXT=args["prototxt"],
    MODEL=args["model"],
    CONFIDENCE=args["confidence"],
    USE_MOVIDIUS=args["movidius"],
)

def detect_motion(frame_count):
    from src.tracking.openvino.openvino import detect_motion
    detect_motion(frame_count)

# start a thread that will perform motion detection
t = threading.Thread(target=detect_motion, args=(32,))
t.daemon = True
t.start()

# start the flask app
app.run(host=app.config["IP"], port=app.config["PORT"], debug=True, threaded=True, use_reloader=False)