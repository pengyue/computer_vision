import cv2
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--face", required=True, help="path to front face cascade classifier")
ap.add_argument("-e", "--eye", required=True, help="path to eye cascade classifier")
args = vars(ap.parse_args())

faceCascade = cv2.CascadeClassifier(args["face"])

if args["eye"]:
    eye_cascade = cv2.CascadeClassifier(args["eye"])
else:
    eye_cascade = False

video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        img = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        if not eye_cascade:
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
