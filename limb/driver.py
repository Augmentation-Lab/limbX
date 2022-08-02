"""
DRIVER SCRIPT
executes control system
"""

# IMPORTS & CLASSES

from time import sleep
import asyncio
from collections import defaultdict
import servo, ml
from classes import SystemState, Params
        
# GLOBALS

updateInterval = 0.1
numSegments = 1
servoDict = {
    1: {
        "lr": 1,
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

# INITIALIZATION

servo.intiailize(servoDict)
servo.testStart()
    
# CONTROL SYSTEM

systemSTATE = SystemState()

def updateSystemSTATE():
    # updates the global state every updateInterval seconds
    systemSTATE.handPosition = getHandPosition()
    sleep(updateInterval)

# not-used
def getHandPosition():
    # methods to get current position? IMU data?
    handPosition = {'x': 0, 'y': 0, 'z': 0}   
    return handPosition
    
def calculateCtrlSeq(target):
    # calculate control sequence necessary to move grabber to target
    # target in the form: {'x': 0, 'y': 0, 'z': 0}
    controlSequence = ml.calculateCtrlSeq(systemSTATE.handPosition, target)
    return controlSequence

def controlSegment(segment, target):

    pass

def processInput(inputData):
    # process input data to generate command
    # inputData is compressed schema of object 
    
    pass

segmentMap = defaultdict()
segmentMap[1] = {}

# MAIN

while True:
    asyncio.run(updateSystemSTATE())
    
    # add delay?


# SHUTDOWN
servo.shutdown()