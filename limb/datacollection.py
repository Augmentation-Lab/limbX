# implementing the last few things
import cv2
import time
import utilities.servoDict as servoDict
from utilities import servo
systemSTATE = servoDict.initialize()
fullMove = 1
#s1_angle = 60 # Segment 1 moves from 60 - 120 range
#s2_angle = 0 # Segment 2 moves from 0 to 270
#s3_angle = 0 # Segment 3 moves from 0 to 270
stepsize = 30 # this means that we are changing the angle by 30 degrees
# setting the angles of the servos to zero initially
#servo.batchSetAngles(systemSTATE.servoDict, {1: {"lr":60}})
#servo.batchSetAngles(systemSTATE.servoDict, {2: {"lr":0}})
#servo.batchSetAngles(systemSTATE.servoDict, {3: {"lr":0}})


print("Setup complete")
time.sleep(5)
print("Testing starts now.")
for j in range(60,210,30):
	for i in range(0,270,30):
		for k in range(0,270,30):
			print(j,i,k)
			framecount = 0
			cap = cv2.VideoCapture(0)
			_, frame = cap.read()
			height, width, _ = frame.shape
			# Define the VideoWriter
			fourcc = cv2.VideoWriter_fourcc(*'XVID') 
			out = cv2.VideoWriter(f'limb/videodata/movement_seg1_{j}_seg2_{i}_seg3_{k}.avi', fourcc,30.0, (width, height))
			
			while(cap.isOpened()):
				ret, frame = cap.read()
				if ret:
					framecount += 1
					out.write(frame)
					cv2.imshow('frame', frame)
					#time.sleep(2)
					if framecount == 50:
						out.write(frame)
						cv2.imshow('frame', frame)
						servo.batchSetAngles(systemSTATE.servoDict, {1: {"lr":j}})
						servo.batchSetAngles(systemSTATE.servoDict, {2: {"lr":i}})
						servo.batchSetAngles(systemSTATE.servoDict, {3: {"lr":k}})
					if framecount == 200:
						#time.sleep(1)
						break
				else: 
					break

			cap.release()
			out.release() 
			cv2.destroyAllWindows()	
	
	
	
	
	
