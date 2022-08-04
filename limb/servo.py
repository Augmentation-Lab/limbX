"""
SERVO SCRIPT
low level functions for servo control
refs: https://www.instructables.com/Servo-Motor-Control-With-Raspberry-Pi/,
https://docs.onion.io/omega2-maker-kit/maker-kit-servo-controlling-servo.html
"""

import RPi.GPIO as GPIO
from time import sleep
from collections import defaultdict

class Servo:
    def __init__(self, name, pin, minAngle=0, maxAngle=180):
        print(f"Initializing servo {name} on pin {pin}")
        GPIO.setup(pin, GPIO.OUT)
        self.name = name
        self.pin = pin
        self.minAngle = minAngle
        self.maxangle = maxAngle
        self.currentAngle = 0
        self.pwm = GPIO.PWM(pin, 50) # 50 Hz
        self.pwm.start(0)

    def pausePWM(self):
        print(f"pausePWM(servo={self.name})")
        GPIO.output(self.pin, False)
        self.pwm.ChangeDutyCycle(0)

    def setAngle(self, angle):
        print(f"setAngle(servo={self.pin}, angle={angle})")
        # check against max and min angles
        if angle < self.minAngle:
            angle = self.minAngle
        elif angle > self.maxAngle:
            angle = self.maxAngle
        duty = angle / 18 + 2
        GPIO.output(self.pin, True)
        self.pwm.ChangeDutyCycle(duty)
        sleep(1)
        self.pausePWM()
        self.currentAngle = angle

    def shutdown(self):
        print(f"Shutting down servo {self.name} on pin {self.pin}")
        self.pwm.stop()

def initialize(servoPins):
    servoDict = defaultdict()
    GPIO.setmode(GPIO.BOARD)
    for segment in servoPins.keys():
        for axis in servoPins[segment].keys():
            print(f"intializing segment={segment}, axis={axis}")
            servoDict[segment][axis] = Servo(f"{segment}_{axis}", servoPins[segment][axis])
    # omit return?
    return servoDict

def shutdown(servoDict):
    for servo in servoDict.values():
        servo.shutdown()
    GPIO.cleanup()

def testStart(servoDict):
    setAllAngles(servoDict, 90)
    sleep(1)
    setAllAngles(servoDict, 0)

def moveSegment(servoDict, segment, angles):
    lrServo = servoDict[segment]["lr"]
    udServo = servoDict[segment]["ud"]
    lrServo.setAngle(angles["lr"])
    udServo.setAngle(angles["ud"])

def setAllAngles(servoDict, angle):
    for servo in servoDict.values():
        servo.setAngle(angle)

def batchSetAngles(servoDict, batchAngles):
    """
    batchAngles is a dictionary of angles to set
    {
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