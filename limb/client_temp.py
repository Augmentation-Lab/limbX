"""
working demo of getting photo from Tobiii
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
# import vision, driver

address = "192.168.71.50"
#address = "fe80::76fe:48ff:ff00:ff00"
cap = cv2.VideoCapture("rtsp://%s:8554/live/scene" % address)

# Check if camera opened successfully
if (cap.isOpened()== False):
  print("Error opening video stream or file")

# Read until video is completed
while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True:

    # Display the resulting frame
    # cv2.imshow('Tobii Pro Glasses 2 - Live Scene',frame)
    cv2.imwrite("snapshot.jpg", frame)
    # img = cv2.imread(frame)
    # plt.imshow(img)
    break

# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()


# on signal received
# which side should we do object labeling on?
# targetObj = TargetObj(imgData=signal["imgData"], objLabel=signal["objLabel"])

# targetObj = TargetObj(imgData=signal["imgData"])
# targetObj.objLabel = vision.get_obj_label(targetObj)
# targetObj.relPos = vision.get_rel_pos(targetObj)
# driver.executeCommands([{"move": targetObj.relPos}])