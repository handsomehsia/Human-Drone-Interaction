import cv2
from djitellopy import tello

# cap = cv2.VideoCapture(0)

me = tello.Tello()
me.connect()
print(me.get_battery())
me.streamoff()
me.streamon()
img = me.get_frame_read().frame
img = cv2.resize(img, (640, 480))

tracker = cv2.legacy.TrackerMOSSE_create()
bbox = cv2.selectROI("tracking", img, False)
tracker.init(img, bbox)


def drawBox(img, bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(img, (x, y), ((x+w), (y+h)), (255, 0, 255), 3, 1)
    cv2.putText(img, "tracking", (75, 75),
                cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)
    pass


while True:

    timer = cv2.getTickCount()
    # _, img = cap.read()
    img = me.get_frame_read().frame
    img = cv2.resize(img, (640, 480))

    _, bbox = tracker.update(img)

    if bbox:
        drawBox(img, bbox)

    else:
        cv2.putText(img, "lost", (75, 75),
                    cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)

    fps = cv2.getTickFrequency()/(cv2.getTickCount()-timer)
    cv2.putText(img, str(int(fps)), (75, 50),
                cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)
    cv2.imshow("tracking", img)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break
