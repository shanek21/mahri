#!/usr/bin/python

import cv2
import math
import time

class Face:
    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.midx = x + w/2
        self.midy = y + h/2

class RightEye:
    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.midx = x + w/2
        self.midy = y + h/2

class LeftEye:
    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.midx = x + w/2
        self.midy = y + h/2

def largestIndex(items):
    largestIndex = 0;
    largest = 0
    for index, item in enumerate(items):
        if item.w > largest:
            largest = item.w
            largestIndex = index
    return largestIndex

def run():
    # Set up the video feed on second camera available
    cap = cv2.VideoCapture(1)

    # Define video resolution
    cap.set(3, 480)
    cap.set(4, 360)

    # Point to haarcascades for eye detection
    right_eye_cascade = cv2.CascadeClassifier('/home/skelly1/OpenCV/opencv-3.1.0/data/haarcascades/haarcascade_righteye_2splits.xml')
    left_eye_cascade = cv2.CascadeClassifier('/home/skelly1/OpenCV/opencv-3.1.0/data/haarcascades/haarcascade_lefteye_2splits.xml')

    # Run until code is exited
    while 1:
        # Grab an image from camera and detect eyes
        ret, frame = cap.read()
        rightEyes = right_eye_cascade.detectMultiScale(frame, scaleFactor=1.2, minSize=(10,10))
        leftEyes = left_eye_cascade.detectMultiScale(frame, scaleFactor=1.2, minSize=(10,10))

        # Find largest right eye and draw a rectangle around it
        rightEyeObjects = []
        if len(rightEyes):
            for (x, y, w, h) in rightEyes:
                rightEyeObjects.append(RightEye(x, y, w, h))
            largestRightEye = rightEyeObjects[largestIndex(rightEyeObjects)]
            cv2.rectangle(frame, (largestRightEye.x, largestRightEye.y), (largestRightEye.x+largestRightEye.w, largestRightEye.y+largestRightEye.h), (0, 0, 255))
        
        # Find largest left eye and draw a rectangle around it
        leftEyeObjects = []
        if len(leftEyes):
            for (x, y, w, h) in leftEyes:
                leftEyeObjects.append(LeftEye(x, y, w, h))
            largestLeftEye = leftEyeObjects[largestIndex(leftEyeObjects)]
            cv2.rectangle(frame, (largestLeftEye.x, largestLeftEye.y), (largestLeftEye.x+largestLeftEye.w, largestLeftEye.y+largestLeftEye.h), (0, 0, 255))

        # Calculate the angle of the face using the relative position of the eyes
        if len(rightEyes)>0 and len(leftEyes)>0:
            xDistance = largestLeftEye.midx - largestRightEye.midx
            yDistance = largestRightEye.midy - largestLeftEye.midy

            try:
                angle = math.asin(float(yDistance)/xDistance)
                print math.degrees(angle)
                print "\n"
            except:
                pass

        # Show the frame
        cv2.imshow('frame',frame)

        # Wait for an escape key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When escape key is pressed, end the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run()