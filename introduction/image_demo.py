from djitellopy import tello
import cv2

from cvzone.FaceDetectionModule import FaceDetector
detector = FaceDetector(minDetectionCon=0.5)

me = tello.Tello()
me.connect()

print(me.get_battery())

# tuen off and on streaming
me.streamoff()
me.streamon()

while True:
    # get frame
    img = me.get_frame_read().frame

    # find faces
    # img, bboxs = detector.findFaces(img, draw=True)

    # display every frame
    cv2.imshow("Image", img)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        me.streamoff()
        break

cv2.destroyAllWindows()
