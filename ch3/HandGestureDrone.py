import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.FaceDetectionModule import FaceDetector
import cvzone
from djitellopy import tello
import time
import threading

cap = cv2.VideoCapture(0)
detectorHand = HandDetector(maxHands=1, detectionCon=0.8)
detectorFace = FaceDetector(minDetectionCon=0.7)
gesture = ''

me = tello.Tello()
me.connect()
print(me.get_battery())
me.streamoff()
me.streamon()

me.takeoff()
time.sleep(5)
me.move_up(60)


# def job(name):  # 要被執行的方法(函數)
#     # me.flip_left()
#     print("HI " + name)


# # 放入執行序中
# t = threading.Thread(target=job, args=('Nash',))


while True:
    # _, img = cap.read()
    # img = cv2.resize(img, (640, 480))

    img = me.get_frame_read().frame
    img = cv2.resize(img, (640, 480))
    img = detectorHand.findHands(img, draw=True)
    lmList, bboxInfo = detectorHand.findPosition(img, draw=False)
    img, bboxs = detectorFace.findFaces(img, draw=False)

    if bboxs:
        x, y, w, h = bboxs[0]['bbox']  # [0] represent first face
        bboxRegion = x - 175-50, y - 75, 175, h + 75
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
                    gesture = " Forward"
                    me.send_rc_control(0, 30, 0, 0)
                   # me.move_forward(20)
                elif fingers == [0, 1, 0, 0, 0]:
                    gesture = "UP"
                    me.send_rc_control(0, 0, 30, 0)

                elif fingers == [0, 0, 0, 0, 0]:
                    gesture = "   Back"
                    me.send_rc_control(0, -30, 0, 0)

                elif fingers == [0, 0, 1, 0, 0]:
                    gesture = " STOP"
                    me.send_rc_control(0, 0, 0, 0)

                # elif fingers == [1, 1, 0, 0, 1]:
                #     gesture = "Flip"
                #     me.flip_left()
                    # time.sleep(1)
                    # t.start()  # 開始
                    # t.join()  # 等待結束
                    # break
                elif fingers == [0, 1, 1, 0, 0]:
                    gesture = " Down"
                    me.send_rc_control(0, 0, -20, 0)

                elif fingers == [1, 0, 0, 0, 0]:
                    gesture = "Right"
                    me.send_rc_control(20, 0, 0, 0)

                elif fingers == [0, 0, 0, 0, 1]:
                    gesture = "Left"
                    me.send_rc_control(-20, 0, 0, 0)
                # elif fingers == [0, 0, 1, 0, 1]:
                #     gesture = "OK Land"
                #     me.land()
                else:
                    me.send_rc_control(0, 0, 0, 0)

                cv2.rectangle(img, (bboxRegion[0], bboxRegion[1]+bboxRegion[3]+10), (bboxRegion[0]+bboxRegion[2], bboxRegion[1]+bboxRegion[3]+60), (0, 255, 0), cv2.FILLED
                              )
                cv2.putText(img, gesture, (bboxRegion[0]+10, bboxRegion[1] +
                            bboxRegion[3]+50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
            else:
                me.send_rc_control(0, 0, 0, 0)
        else:
            me.send_rc_control(0, 0, 0, 0)
    else:
        me.send_rc_control(0, 0, 0, 0)
    #imageStacked = cvzone.stackImages([img, imgPC], 1, 1)
    cv2.imshow("Image", img)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        me.land()
        me.streamoff()
        break

cv2.destroyAllWindows()
