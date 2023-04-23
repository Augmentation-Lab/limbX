"""
SERVO SCRIPT
executes low level servo control
refs: https://www.instructables.com/Servo-Motor-Control-With-Raspberry-Pi/,
https://docs.onion.io/omega2-maker-kit/maker-kit-servo-controlling-servo.html
"""

from time import sleep
from collections import defaultdict
import math
from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)


class Servo:
    def __init__(self, name, pin, minAngle=0, maxAngle=270, defaultAngle=135):
        self.pin = pin
        # self.currentAngle = kit.servo[self.pin].angle
        self.startingAngle = kit.servo[self.pin].angle
        print(
            f"Initializing servo {name} on pin {pin}. Hardware at 0 degrees, servo currently at {self.startingAngle} degrees.")
        self.name = name
        self.minAngle = minAngle
        self.maxAngle = maxAngle
        self.currentAngle = defaultAngle
        self.defaultAngle = defaultAngle
        kit.servo[self.pin].angle = defaultAngle
        sleep(2)

    def __repr__(self):
        return (f"Servo {self.name} on pin {self.pin} at angle {self.currentAngle}")

    # Speed is in degrees/second. The hardware is limited to about 400 degrees/second without a load.
    def setAngle(self, angle, speed=90):
        print(
            f"setAngle(servo_name={self.name}, servo_pin={self.pin}, angle={angle})")
        # check against max and min angles
        if angle < self.minAngle:
            angle = self.minAngle
        elif angle > self.maxAngle:
            angle = self.maxAngle

        # The amount of angle movement we want is 35 degrees
        # We are moving up to 8 degrees per second
        # We will move every 0.5 seconds ("Our frame rate")
        # This means we will move 4 degrees in those 0.5 seconds
        # We will move, in total, 35/4 times
        # We round this down to 8 times, with 1 on the end where we move the remaining distance

        angleDiff = angle - self.currentAngle
        frameTime = 0.1
        angleMovePerFrame = frameTime * speed
        intermediateAngle = self.currentAngle
        totalMoves = abs(angleDiff/angleMovePerFrame)
        # If they want to mvoe to,,.. say... 180.01 degrees, we don't count this as a move because it'd be "between frames". So we just do the last bit all at once near the end
        fullMoves = math.floor(totalMoves)
        for move in range(fullMoves):
            if angleDiff > 0:
                intermediateAngle += angleMovePerFrame
            else:
                intermediateAngle -= angleMovePerFrame
            print("currAngle", kit.servo[self.pin].angle)
            kit.servo[self.pin].angle = intermediateAngle
            sleep(frameTime)
        kit.servo[self.pin].angle = angle
        self.currentAngle = angle


def initialize(servoPins):
    servoDict = defaultdict()
    for segment in servoPins.keys():
        servoDict[segment] = defaultdict()
        for axis in servoPins[segment].keys():
            print(f"intializing segment={segment}, axis={axis}")
            servoDict[segment][axis] = Servo(
                f"{segment}_{axis}", servoPins[segment][axis])
    return servoDict


def shutdown(servoDict):
    # This turns the servos all back to their "default position", so that when you turn the
    # rpi back on and all the servos go back to their default position, it (ideally) won't actually move the servos really at all

    # If you don't shutdown, and say... the servo's were at 270 before the rpi last shut down, then in the init script,
    # It'll turn the servo to the default position (say 180) super duper quickly, which may damage the servo or the tentacle.
    # and the init script really does need to move to a default position at the beginning because, if it doesn't, then it has no clue
    # where the servo *actually* is

    # If you do shutdown, then the servo will slowly and, in a controlled fashion, will go back to the default position.
    # Now, when you turn the rpi back on, if you haven't changed teh default position, it won't have any uncontrolled movement when it "wakes up"
    for servo in servoDict.values():
        for axis in servo.values():
            axis.setAngle(axis.defaultAngle)
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
