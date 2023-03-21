from djitellopy import tello
import cv2
from cvzone.PoseModule import PoseDetector

# get the detection model
detector = PoseDetector(upBody=True)
cap = cv2.VideoCapture(1)

while True:
    _, img = cap.read()
    img = cv2.resize(img, (640, 480))
    img = detector.findPose(img, draw=False)
    lmList, bboxInfo = detector.findPosition(
        img, draw=True, bboxWithHands=False)

    cv2.imshow("Image", img)

    cv2.waitKey(1)
