#!/usr/bin/python

import cv2
import math
import time
import servoControl

class Eye:
    """
    A class to store location and dimension
    attributes for eyes.
    """
    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.midx = x + w/2
        self.midy = y + h/2

def largestIndex(items):
    """
    Given a list of objects with a width attribute
    'w', returns the index of the object with the
    largest width.
    """
    largestIndex = 0;
    largest = 0
    for index, item in enumerate(items):
        if item.w > largest:
            largest = item.w
            largestIndex = index
    return largestIndex

def run(camera_mode, l_eye_file, r_eye_file):
    """
    Main function to begin camera capture, detect
    eyes, and calcualte the angle of the largest
    pair of eyes.
    """
    # Initialize Mahri's servos
    servoControl.Initialize()

    # Set up the video feed on second camera available
    cap = cv2.VideoCapture(camera_mode)

    # Define video resolution
    cap.set(3, 480)
    cap.set(4, 360)

    # Point to haarcascades for eye detection
    right_eye_cascade = cv2.CascadeClassifier(r_eye_file)
    left_eye_cascade = cv2.CascadeClassifier(l_eye_file)

    while 1:
        # Grab an image from camera and detect eyes in the image
        ret, frame = cap.read()
        rightEyes = right_eye_cascade.detectMultiScale(frame, scaleFactor=1.2, minSize=(10,10))
        leftEyes = left_eye_cascade.detectMultiScale(frame, scaleFactor=1.2, minSize=(10,10))

        # Find largest right eye and draw a rectangle around it
        rightEyeObjects = []
        if len(rightEyes):
            for (x, y, w, h) in rightEyes:
                rightEyeObjects.append(Eye(x, y, w, h))
            largestRightEye = rightEyeObjects[largestIndex(rightEyeObjects)]
            cv2.rectangle(frame, (largestRightEye.x, largestRightEye.y), (largestRightEye.x+largestRightEye.w, largestRightEye.y+largestRightEye.h), (0, 0, 255))
        
        # Find largest left eye and draw a rectangle around it
        leftEyeObjects = []
        if len(leftEyes):
            for (x, y, w, h) in leftEyes:
                leftEyeObjects.append(Eye(x, y, w, h))
            largestLeftEye = leftEyeObjects[largestIndex(leftEyeObjects)]
            cv2.rectangle(frame, (largestLeftEye.x, largestLeftEye.y), (largestLeftEye.x+largestLeftEye.w, largestLeftEye.y+largestLeftEye.h), (0, 0, 255))

        # Calculate the angle of the face using the relative position of the eyes
        if len(rightEyes)>0 and len(leftEyes)>0:
            xDistance = largestLeftEye.midx - largestRightEye.midx
            yDistance = largestRightEye.midy - largestLeftEye.midy

            try:
                angle = math.degrees(math.asin(float(yDistance)/xDistance))
                servoControl.setMahriAngle(angle)
                print angle
                print "\n"
            except:
                pass

        # Show the frame
        cv2.imshow('frame',frame)

        # Wait for an escape key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # Unmount GPIO pins
            servoControl.cleanup()

            # Break the while loop to end video capture
            break

    # When escape key is pressed, end the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run(0, '/home/kghite/opencv/data/haarcascades/haarcascade_righteye_2splits.xml', '/home/kghite/opencv/data/haarcascades/haarcascade_lefteye_2splits.xml')