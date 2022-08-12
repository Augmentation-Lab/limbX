"""
SERVO SCRIPT
low level functions for servo control
ref: https://www.instructables.com/Servo-Motor-Control-With-Raspberry-Pi/
"""

# are globals appropriate for this use case?
global GPIO
global pwm
global servoDict

import RPi.GPIO as GPIO
from time import sleep

# EXAMPLE
# servoDict = {
#     1: {
#         "lr": 1,
#         "bf": 2
#     },
#     2: {
#         "lr": 3,
#         "bf": 4
#     },
#     3: {
#         "lr": 5,
#         "bf": 6
#     }
# }

def intiailize(inputServoDict):
    print(f"initialize(inputServoDict={inputServoDict})")
    servoDict = inputServoDict
    GPIO.setmode(GPIO.BOARD)
    for segment in servoDict.keys():
        for servo in servoDict[segment].keys():
            print(f"intializing segment={segment}, servo={servo}")
            GPIO.setup(servoDict[segment][servo], GPIO.OUT)
            pwm = GPIO.PWM(servoDict[segment][servo], 50) # 50 Hz
            pwm.start(0)

def pausePWM(servo):
    print(f"pausePWM(servo={servo})")
    GPIO.output(servo, False)
    pwm.ChangeDutyCycle(0)

def setAngle(servo, angle):
    print(f"setAngle(servo={servo}, angle={angle})")
    duty = angle / 18 + 2
    GPIO.output(servo, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    pausePWM()
    
def testStart():
    print("testStart()")
    for segment in servoDict.keys():
        for servo in servoDict[segment].keys():
            print(f"testing segment={segment}, servo={servo}")
            setAngle(servoDict[segment][servo], 90)
    sleep(1)
    for segment in servoDict.keys():
        for servo in servoDict[segment].keys():
            setAngle(servoDict[segment][servo], 0)

            GPIO.setup(servoDict[segment][servo], GPIO.OUT)
            pwm = GPIO.PWM(servoDict[segment][servo], 50) # 50 Hz
            pwm.start(0)

def shutdown():
    pwm.stop()
    GPIO.cleanup()