from djitellopy import tello
import time
import cv2

me = tello.Tello()
me.connect()
me.enable_mission_pads()

print(me.get_battery())

me.takeoff()
time.sleep(3)
me.move_up(50)
time.sleep(3)
me.flip_left()
time.sleep(3)
me.send_rc_control(0, 0, 0, 50)
time.sleep(3)
me.send_rc_control(0, 0, 0, 0)
time.sleep(3)
me.land()

me.takeoff()
time.sleep(3)
me.send_rc_control(10, 0, 0, 0)
time.sleep(1)
me.send_rc_control(0, 0, 0, 0)
me.land()


me.streamoff()
me.streamon1()
frame_read = me.get_frame_read()
while True:
    # get frame
    img = frame_read.frame

    

    # display every frame
    cv2.imshow("Image", img)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        me.streamoff()
        break

cv2.destroyAllWindows()



