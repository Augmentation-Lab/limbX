# from limb import driver
from limb.utilities import servo
from limb import driver
# from time import sleep
from collections import defaultdict
import yaml
import time
import keyboard

"""
complexCalibration (including dependencies):
{
    0: 135lr,
    1: 135lr,
    2: (135lr, 135bf),
    3: (135lr, 135bf)
}
mediumCalibration (including dependencies but assuming symmetry):
{
    0: 135lr,
    1: 135lr,
    2: 135lr,
    3: 135lr
}
simpleCalibration (excluding dependencies):
{
    0: 135lr,
    1: 135lr,
    2: (135lr, 135bf),
    3: (135lr, 135bf)
}
"""

"""
in the recursive form:
{
obj: {
    1: {
        angle:
        dependentAngles: obj
    },
    2: {
        angle:
        dependentAngles: obj
    },
    ...
    n: {
        angle:
        dependentAngles: obj
    }
}
"""

with open("limb/config.yml") as f:
    calibrationData = yaml.safe_load(f)
    calibrationDict = calibrationData["calibrationDict"]
    numSegmentsToCalib = calibrationData["numSegmentsToCalib"]
    servoDict = driver.systemSTATE.servoDict

class anglesObj():
    def __init__(self, segment, minAngle, maxAngle, interval):
        self.segment = segment
        self.minAngle = minAngle
        self.maxAngle = maxAngle
        self.interval = interval
        self.tangles = defaultdict()
        for i in range(self.minAngle, self.maxAngle + 1, self.interval):
            self.tangles[i] = {"sangle": None, "dependentAngles": defaultdict()}
    
    def setSangle(self, tangle, sangle):
        self.tangles[tangle]["sangle"] = sangle

class anglesDict():
    def __init__(self, numSegments, calibrationDict):
        self.numSegments = numSegments
        self.objects = defaultdict()
        for i in range(len(numSegments)):
            self.objects[i] = anglesObj(segment=i, minAngle=calibrationDict[i]["minAngle"], maxangle=calibrationDict[i]["maxAngle"], interval=calibrationDict[i]["angleInterval"])

def calibrate(servoDict, numSegments, calibrationDict):
    calibrationDict = anglesDict(numSegments, calibrationDict)
    for thisAngleObj in calibrationDict.objects.values():
        # move servo from minAngle to maxAngle iteratively
        thisServo = servoDict[thisAngleObj.segment]["lr"]
        print("thisServo: ", thisServo)
        tangleIndex = 0
        for thisSangle in range(thisAngleObj.minAngle, thisAngleObj.maxAngle + 1, thisAngleObj.interval):
            thisServo.setAngle(thisSangle)
            time.sleep(0.1)
            if keyboard.is_pressed('q'):
                thisTangle = list(thisAngleObj.tangles.keys())[tangleIndex]
                print(f"Segment {thisAngleObj.segment}, Tangle {tangleIndex}: Sangle {thisSangle}")
                thisAngleObj.setSangle(thisTangle, thisSangle)
                tangleIndex += 1
            if tangleIndex == len(thisAngleObj.tangles):
                break

calibrate(servoDict, numSegmentsToCalib, calibrationDict)