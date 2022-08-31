import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.FaceDetectionModule import FaceDetector
import cvzone

cap = cv2.VideoCapture(0)
detectorHand = HandDetector(maxHands=1, detectionCon=0.7)
detectorFace = FaceDetector(minDetectionCon=0.7)
gesture = ''

while True:
    _, img = cap.read()
    img = detectorHand.findHands(img)
    lmList, bboxInfo = detectorHand.findPosition(img)
    img, bboxs = detectorFace.findFaces(img, draw=True)

    if bboxs:
        x, y, w, h = bboxs[0]['bbox']  # [0] represent first face
        bboxRegion = x - 175 - 130, y - 75, 175, h + 75
        cvzone.cornerRect(img, bboxRegion, rt=0, t=10, colorC=(0, 0, 255))
        # print(detectorHand.handType())

        if lmList and detectorHand.handType() == 'Right':

            handCenter = bboxInfo['center']
            #     x       <     cx        <      x+w
            inside = bboxRegion[0] < handCenter[0] < bboxRegion[0]+bboxRegion[2] and \
                bboxRegion[1] < handCenter[1] < bboxRegion[1]+bboxRegion[3]
            #   y    <    cy   < y+h

            if inside:
                cvzone.cornerRect(img, bboxRegion, rt=0,
                                  t=10, colorC=(0, 255, 0))

                fingers = detectorHand.fingersUp()
                # print(fingers)

                if fingers == [1, 1, 1, 1, 1]:
                    gesture = " Open"
                elif fingers == [0, 1, 0, 0, 0]:
                    gesture = "Index"
                elif fingers == [0, 0, 0, 0, 0]:
                    gesture = "   Fist"
                elif fingers == [0, 0, 1, 0, 0]:
                    gesture = " Middle"
                elif fingers == [1, 1, 0, 0, 1]:
                    gesture = "Spiderman"
                elif fingers == [0, 1, 1, 0, 0]:
                    gesture = " Victory"
                elif fingers == [1, 0, 0, 0, 0]:
                    gesture = "Thumb"
                elif fingers == [0, 0, 0, 0, 1]:
                    gesture = "Pinky"
                cv2.rectangle(img, (bboxRegion[0], bboxRegion[1]+bboxRegion[3]+10), (bboxRegion[0]+bboxRegion[2], bboxRegion[1]+bboxRegion[3]+60), (0, 255, 0), cv2.FILLED
                              )
                cv2.putText(img, gesture, (bboxRegion[0]+10, bboxRegion[1] +
                            bboxRegion[3]+50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
