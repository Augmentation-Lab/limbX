import utilities.servoDict as servoDict
import time
import cv2
from utilities import servo
cap = cv2.VideoCapture(0)
systemSTATE = servoDict.initialize()

print("Setup complete")
servo.batchSetAngles(systemSTATE.servoDict, {1: {"lr":210}})
#servo.batchSetAngles(systemSTATE.servoDict, {2: {"lr":270}})
#servo.batchSetAngles(systemSTATE.servoDict, {3: {"lr":270}})
time.sleep(100)





# logic such that we are capturing the video for each movement
# for i in range(numberofdatapoints): # for each data point we are going to take a video
for s1_angle in list(range(60,210,stepsize)):
	for s2_angle in list(range(0,270, stepsize)):
		for s3_angle in list(range(0,270,stepsize)):
			cap = cv2.VideoCapture(0)
			fourcc = cv2.VideoWriter_fourcc(*'XVID') 
			height = int(cap.get(4))
			width = int(cap.get(3))
			#fps = int(cap.get(cv2.CAP_PROP_FPS))
			# Creating a VideoWriter output variable
			out = cv2.VideoWriter(f'data_{s1_angle, s2_angle, s3_angle}.mp4', fourcc, 30.0, (width, height))
			anglemovement=True
			while(anglemovement):
				_, frame = cap.read()
				out.write(frame)
				cv2.imshow('frame', frame)
				moving_limb(s1_angle, s2_angle, s3_angle)
				time.sleep(5)
				anglemovement = False
				if cv2.waitKey(1) & 0xFF == ord('q'):
					break
