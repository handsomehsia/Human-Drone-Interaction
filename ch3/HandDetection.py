import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)

while True:
    _, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    print(lmList)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
