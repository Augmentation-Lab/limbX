# Imports & Classes

import RPi.GPIO as GPIO
from time import sleep
from collections import default dict

class Params():
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        
# Globals

updateInterval = 0.1
numSegments = 1

# Initialization

GPIO.setmode(GPIO.BOARD)
lrServoPin = 12
udServoPin = 11

GPIO.setup(lrServoPin, GPIO.OUT)

pwm = GPIO.PWM(lrServoPin, 50)
pwm.start(0)

def pausePWM():
    GPIO.output(servo, False)
    pwm.ChangeDutyCycle(0)

def SetAngle(servo, angle):
    duty = angle / 18 + 2
    GPIO.output(servo, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    pausePWM()
    
def testStart():
    SetAngle(lrServoPin, 90)
    sleep(1)
    SetAngle(lrServoPin, 0)
    
# Control System

state = Params()

def update():
    # updates the global state every updateInterval seconds
    state.currentPosition = getCurrentPosition()
    sleep(updateInterval)
        
segmentMap = defaultdict()
segmentMap[1] =

# def getCurrentPosition():
#     # methods to get current position? IMU data?
#     return currentPosition
    
def calculateControls(target):
    # calculate control sequence necessary to move grabber to target
    controlSequece = getControlSequence()
    return controlSequence

def controlSegment(segment, target):
    

pwm.stop()
GPIO.cleanup()