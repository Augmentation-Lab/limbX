"""
SERVO SCRIPT
executes low level servo control
refs: https://www.instructables.com/Servo-Motor-Control-With-Raspberry-Pi/,
https://docs.onion.io/omega2-maker-kit/maker-kit-servo-controlling-servo.html
"""

#import RPi.GPIO as GPIO
from time import sleep
from collections import defaultdict
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)

class Servo:
    def __init__(self, name, pin, minAngle=0, maxAngle=270):
        print(f"Initializing servo {name} on pin {pin}")
        self.name = name
        self.pin = pin
        self.minAngle = minAngle
        self.maxAngle = maxAngle
        self.currentAngle = 0

    def setAngle(self, angle):
        print(f"setAngle(servo_name={self.name}, servo_pin={self.pin}, angle={angle})")
        # check against max and min angles
        if angle < self.minAngle:
            angle = self.minAngle
        elif angle > self.maxAngle:
            angle = self.maxAngle

        kit.servo[self.pin].angle = angle
        self.currentAngle = angle
        sleep(1)

def initialize(servoPins):
    servoDict = defaultdict()
    for segment in servoPins.keys():
        servoDict[segment] = defaultdict()
        for axis in servoPins[segment].keys():
            print(f"intializing segment={segment}, axis={axis}")
            servoDict[segment][axis] = Servo(f"{segment}_{axis}", servoPins[segment][axis])
    # omit return?
    return servoDict

def shutdown(servoDict):
    print("shutting down...")

def setAllAngles(servoDict, angle):
    for servo in servoDict.values():
        for axis in servo.values():
            axis.setAngle(angle)

def batchSetAngles(servoDict, batchAngles):
    """
    batchAngles is a dictionary of angles to set
    {
        0: {
            "central": 90
        }
        1: {
            "lr": 90,
            "ud": 2
        },
        2: {
            "lr": 3,
            "ud": 4
        },
        3: {
            "lr": 5,
            "ud": 6
        }
    }
    """
    for segment in batchAngles.keys():
        for axis in batchAngles[segment].keys():
            servoDict[segment][axis].setAngle(batchAngles[segment][axis])

