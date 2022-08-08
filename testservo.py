from adafruit_servokit import ServoKit

import time

kit = ServoKit(channels=16)

for i in range(16):
    kit.servo[i].angle = 180

time.sleep(1)

for i in range(16):
    kit.servo[i].angle = 0
