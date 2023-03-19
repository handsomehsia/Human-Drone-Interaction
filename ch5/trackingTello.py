# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
from djitellopy import tello
import cvzone
import time

me = tello.Tello()
me.connect()
print(me.get_battery())
me.streamoff()
me.streamon()
img = me.get_frame_read().frame
# me.takeoff()
# time.sleep(3)
# me.move_up(100)

hi, wi = 480, 640
# print(hi, wi)

#                    P  I  D
#             P:ratio to drone speed
#             D: derivative term to redce the speed cause by momentum
xPID = cvzone.PID([0.22, 0, 0.1], wi//2)
yPID = cvzone.PID([0.27, 0, 0.2], hi//2, axis=1)
# when it comes closer when it comes backward
zPID = cvzone.PID([0.15, 0, 0.7], 250, limit=[-15, 15])
# zPID = cvzone.PID([0.0015, 0, 0.007], 25000, limit=[-15, 15])


myPlotX = cvzone.LivePlot(yLimit=[-100, 100], char='X')
myPlotY = cvzone.LivePlot(yLimit=[-100, 100], char='Y')
myPlotZ = cvzone.LivePlot(yLimit=[-100, 100], char='Z')


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
                help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
                help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
# greenLower = (29, 86, 6)
# greenUpper = (64, 255, 255)
# greenLower = (100, 83, 86)
# greenUpper = (124, 255, 255)
# White
# greenLower = (0, 0, 221)
# greenUpper = (180, 30, 255)
# black
greenLower = (0, 0, 0)
greenUpper = (360, 200, 50)
pts = deque(maxlen=args["buffer"])
# if a video path was not supplied, grab the reference
# to the webcam
# if not args.get("video", False):
#     vs = VideoStream(src=0).start()
# # otherwise, grab a reference to the video file
# else:
#     vs = cv2.VideoCapture(args["video"])
# allow the camera or video file to warm up
time.sleep(2.0)
# cap = cv2.VideoCapture(0)
# _, img = cap.read()

img = cv2.resize(img, (640, 480))
hi, wi = 480, 640
# keep looping
while True:
    img = me.get_frame_read().frame

    #_, img = cap.read()
    frame = cv2.resize(img, (640, 480))
    # grab the current frame
    # frame = vs.read()
    # # handle the frame from VideoCapture or VideoStream
    # frame = frame[1] if args.get("video", False) else frame
    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if frame is None:
        break
    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    xVal = 0
    yVal = 0
    zVal = 0

    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.rectangle(frame, (int(x)-int(radius), int(y)-int(radius)),
                          ((int(x)+int(radius)), (int(y)+int(radius))), (255, 0, 255), 3, 1)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)

            area = int(radius)*int(radius)
            cv2.putText(frame, str(area), (50, 100),
                        cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 255), 3)

        cx, cy = x, y  # the 0 means multi faces

        area = int(radius)*int(radius)
        # print(area)  # how far the drone from u

        xVal = int(xPID.update(cx))  # error distance btween center
        yVal = int(yPID.update(cy))  # error distance btween center
        zVal = int(zPID.update(area))  # error distance btween center
        # print(zVal)
        imgPlotX = myPlotX.update(xVal)
        imgPlotY = myPlotY.update(yVal)
        imgPlotZ = myPlotZ.update(zVal)

        #img = xPID.draw(img, [cx, cy])
        #img = yPID.draw(img, [cx, cy])

        imageStacked = cvzone.stackImages(
            [imgPlotX, imgPlotY, imgPlotZ], 2, 0.75)
        cv2.imshow("Stacked", imageStacked)
    # else:
    #     imageStacked = cvzone.stackImages([frame], 1, 0.75)
    #me.send_rc_control(0, -zVal, 0, 0)
    #me.send_rc_control(0, 0, -yVal, 0)
    me.send_rc_control(0, -zVal, -yVal, xVal)
    #print(0, -zVal, -yVal, xVal)
    # update the points queue
    pts.appendleft(center)
    # loop over the set of tracked points
    for i in range(1, len(pts)):
        # if either of the tracked points are None, ignore
        # them
        if pts[i - 1] is None or pts[i] is None:
            continue
        # otherwise, compute the thickness of the line and
        # draw the connecting lines
        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

    # img, bboxs = detector.findFaces(img, draw=True)

    # show the frame to our screen
    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break
# if we are not using a video file, stop the camera video stream
# if not args.get("video", False):
#     vs.stop()
# # otherwise, release the camera
# else:
#     vs.release()
# close all windows
cv2.destroyAllWindows()
