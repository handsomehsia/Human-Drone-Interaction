from djitellopy import tello
import cv2
from cvzone.PoseModule import PoseDetector
import cvzone
import time


class BodyFollowing:

    def __init__(self, drone):
        self.me = drone

    def run(self):

        detector = PoseDetector(upBody=True)

        #cap = cv2.VideoCapture(0)
        #_, img = cap.read()

        #img = cv2.resize(img, (640, 480))
        hi, wi = 480, 640
        # print(hi, wi)

        #                    P  I  D
        #             P:ratio to drone speed
        #             D: derivative term to redce the speed cause by momentum
        xPID = cvzone.PID([0.22, 0, 0.1], wi//2)
        yPID = cvzone.PID([0.27, 0, 0.1], hi//2, axis=1)
        # when it comes closer when it comes backward
        zPID = cvzone.PID([0.00016, 0, 0.000011], 150000, limit=[-20, 15])

        myPlotX = cvzone.LivePlot(yLimit=[-100, 100], char='X')
        myPlotY = cvzone.LivePlot(yLimit=[-100, 100], char='Y')
        myPlotZ = cvzone.LivePlot(yLimit=[-100, 100], char='Z')

        # me = tello.Tello()
        # me.connect()
        print(self.me.get_battery())

        self.me.streamoff()
        self.me.streamon()
        self.me.takeoff()
        time.sleep(5)
        self.me.move_up(80)

        while True:
            #_, img = cap.read()

            img = self.me.get_frame_read().frame
            img = cv2.resize(img, (640, 480))
            img = detector.findPose(img, draw=True)
            lmList, bboxInfo = detector.findPosition(
                img, draw=True, bboxWithHands=False)

            xVal = 0
            yVal = 0
            zVal = 0

            if bboxInfo:
                cx, cy = bboxInfo['center']
                x, y, w, h = bboxInfo['bbox']
                area = w * h
                # print(area)  # how far the drone from u

                xVal = int(xPID.update(cx))  # error distance btween center
                yVal = int(yPID.update(cy))  # error distance btween center
                zVal = int(zPID.update(area))  # error distance btween center
                # print(zVal)
                imgPlotX = myPlotX.update(xVal)
                imgPlotY = myPlotY.update(yVal)
                imgPlotZ = myPlotZ.update(zVal)

                img = xPID.draw(img, [cx, cy])
                img = yPID.draw(img, [cx, cy])

                # cv2.putText(img, str(xVal), (50, 100),
                #             cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 255), 3)

                #cv2.line(img, (wi//2, 0), (wi//2, hi), (255, 0, 255), 1)

                # cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
                # error = wi//2 - cx
                # cv2.putText(img, str(error), (50, 100),
                #             cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 255), 3)
                # cv2.line(img, (wi//2, hi//2), (cx, cy), (255, 0, 255), 3)
            #imageStacked = cvzone.stackImages([img, imgPlotX, imgPlotY, imgPlotZ], 2, 0.75)
                imageStacked = cvzone.stackImages(
                    [img, imgPlotX, imgPlotY, imgPlotZ], 2, 0.75)
                # cv2.putText(imageStacked, str(area), (20, 50),
                #             cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)
            else:
                xVal = 20
                imageStacked = cvzone.stackImages([img], 1, 0.75)

            self.me.send_rc_control(0, -zVal, -yVal, xVal)
            #me.send_rc_control(0, -zVal, 0, 0)

            cv2.imshow("Image", imageStacked)
            #cv2.imshow("Image", img)
            #cv2.imshow("ImagePlotX", imgPlotX)
            if cv2.waitKey(5) & 0xFF == ord('q'):
                self.me.land()
                # me.streamoff()
                break

        cv2.destroyAllWindows()


def main():
    me = tello.Tello()
    me.connect()
    selfiedrone = BodyFollowing(drone=me)
    selfiedrone.run()


if __name__ == "__main__":
    main()
