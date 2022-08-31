from djitellopy import tello
import cv2

me = tello.Tello()
me.connect()
print(me.get_battery())
me.streamoff()
me.streamon()

while True:
    img = me.get_frame_read().frame
    img = cv2.resize(img, (640, 480))
    cv2.imshow("Image", img)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        me.streamoff()
        break

cv2.destroyAllWindows()
