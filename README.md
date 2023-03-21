# Tello-Human-Computer-Interaction
>The demo GIF you see on the down below are mostly shoot by drone camera

## Pre-requisite

### hardware
* Tello Drone/ Tello EDU/ Robomaster TT any of them is fine (the reason is the repo here only apply AP mode. If you wanna learn [swarm project]() plz go to another repo)

### python module
```
# python 3.7 or higher
# pip install
djitellopy2==2.3 or djitellopy==2.4
cvzone==1.5.6
PyAudio==0.2.11
vosk==0.3.43
```
## Pre-knowledges for code
* Shows you how to control drones with djitellopy api (`flying_demo.py`)

* Shows you how to get the image from the drone (`image_demo.py`)

## Chapter 1. Face Tracking Drone
* Drone follows user's face with mediapipe framework and PID controller (`FaceTrackingDrone.py`)
* ## ![Alt Text](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExODhlOWI1ZDY2YmMzYWZiYWI2ZWNkNGE3Njc5MGRkYzA2NWJhMjI1OSZjdD1n/Xk6Yj8LhScHJOyzdYq/giphy.gif)
## Chapter 2. Selfie Drone
* Human armpose interaction while drone tracking human body automatically (`SelfieDrone.py`)
* ![Alt Text](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNDc4ZGVkYWZjNTBlNzU5YWY3YTI4ZGExZThjZmM0MTQzM2UzY2YxOSZjdD1n/4kmzzzdDzIydQY3Xkm/giphy-downsized-large.gif)
## Chapter 3. Hand Gesture Control
* Drone control with finger gesture (`HandGestureDrone.py`)
* You can basicly define your own gestures, here I use finger node detection from mediapipe model. However, You can also train your own NN model.
* ![Alt Text](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM2MwNWFmZjA3ZDQwOWQ4Zjg3OWRmYzQ0ZjU2YWMyYWM3NmQyYThmNyZjdD1n/vd3AIxSkZ17tIwMN3a/giphy-downsized-large.gif)
## Chapter 4. Voice Command Control
* Drone control with voice command (`VoiceControlDrone.py`)
* Applied vosk model to recognize the voice command with en-us model. You can chose your own language forsure
* [Demo](https://drive.google.com/file/d/1aFfdLqqMBPBpYO7S0scrgZGfiFBR6_Xl/view?usp=share_link)
## Chapter 5.   Drone Tracking Drone Control
* Applied HSV recogniztion to detect the color marker.
* Tracked the marker with PID controller (`DroneTrackDrone.py`)
* ![Alt Text](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExYmUzZTJkMDcwYzcwZGM2ZDdmODY0M2U0ZDE2OTVjMGMxYTM2OTQ5NiZjdD1n/RSqhVEIsTpisBJ3E1N/giphy-downsized-large.gif)

* ![Alt Text](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZjJhNmE2ZTM4NTYxZWQ5Y2JmY2Y0Yzk1ZDdmZTE3Y2JlODRkODkwYyZjdD1n/x43hEFaOaxsUrO4fmC/giphy-downsized-large.gif)
