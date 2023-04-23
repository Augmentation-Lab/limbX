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
datapoints = 0

print("Setup complete")
time.sleep(5)
print("Testing starts now.")
cap = cv2.VideoCapture(0)
_, frame = cap.read()
width = int(cap.get(3))
height = int(cap.get(4))
fourcc = cv2.VideoWriter_fourcc(*'XVID') 
out = cv2.VideoWriter('movement.avi', fourcc, 30.0, (width, height))
stopcondition = False

while(cap.isOpened() and not stopcondition):
	
	#_, frame = cap.read()
	
	#height, width, _ = frame.shape
	ret, frame = cap.read()
	if ret:
		out.write(frame)
		cv2.imshow('frame', frame)
		for j in range(60,240,30):
			time.sleep(5)
			for i in range(0,310,30):
				time.sleep(5)
				for k in range(0,310,30):
					print(j,i,k)
					text = "Angles: {}".format(j,i,k)
					cv2.putText(frame, text, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
					datapoints += 1
					servo.batchSetAngles(systemSTATE.servoDict, {1: {"lr":j}})
					servo.batchSetAngles(systemSTATE.servoDict, {2: {"lr":i}})
					servo.batchSetAngles(systemSTATE.servoDict, {3: {"lr":k}})
					if datapoints == 405:
						break
					time.sleep(5)
		if j == 210 and i == 270 and k == 270:
			stopcondition == True
		if cv2.waitKey(1) == ord('q'): 
			break		
	else: 
		break
				
cap.release()
out.release() 
cv2.destroyAllWindows()	
	
	
	
	
	
