import cv2
from cvzone.PoseModule import PoseDetector

cap = cv2.VideoCapture(0)
# width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
# height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
# print(width, height)

detector = PoseDetector(upBody=True)

while True:
    _, img = cap.read()

    img = detector.findPose(img, draw=False)
    lmList, bboxInfo = detector.findPosition(
        img, draw=False, bboxWithHands=False)

    gesture = ''

    if bboxInfo:
        # represent the land mark of mediapipe
        angArmL = detector.findAngle(img, 13, 11, 23, draw=False)
        angArmR = detector.findAngle(img, 14, 12, 24, draw=False)
        crossDistL, img, _ = detector.findDistance(15, 12, img)
        crossDistR, img, _ = detector.findDistance(16, 11, img)

        if (detector.angleCheck(angArmL, 90) and detector.angleCheck(angArmR, 270)):
            gesture = 'T Pose'

        elif (detector.angleCheck(angArmL, 180) and detector.angleCheck(angArmR, 180)):
            gesture = 'Up Pose'

        elif crossDistL:
            if crossDistL < 120 and crossDistR < 120:
                gesture = 'Cross'

        cv2.putText(img, gesture, (20, 50),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
