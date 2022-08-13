"""
DRIVER SCRIPT
executes control system
"""

# IMPORTS & CLASSES

from time import sleep
import asyncio
from collections import defaultdict
import servo, smart
from classes import SystemState, Params
        
# GLOBALS

# updateInterval = 0.1
numSegments = 1
servoPins = {
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

servo.initialize(servoPins)
servo.testStart()
    
# CONTROL SYSTEM

systemSTATE = SystemState()

def calculateCtrlSeq(targetRelPos):
    # calculate control sequence necessary to move grabber to target
    # targetRelPos in the form: {'x': 0, 'y': 0, 'z': 0}
    ctrlSeq = smart.calculateCtrlSeq(systemSTATE.servoAngles, targetRelPos)
    return ctrlSeq

def executeCtrlSeq(ctrlSeq):

    pass

# def updateSystemSTATE():
#     # updates the global state every updateInterval seconds
#     systemSTATE.servoAngles = getServoAngles()
#     sleep(updateInterval)

# # not-used
# def getServoAngles():
#     # get servo angles from system state
#     servoAngles = {
#         1: {
#             "lr": -90,
#             "ud": 180
#         },
#         2: {
#             "lr": 70,
#             "ud": 45
#         },
#         3: {
#             "lr": 120,
#             "ud": 60
#         }
#     }
#     return servoAngles

# def processInput(inputData):
#     # process input data to generate command
#     # inputData is compressed schema of object 
    
#     pass

# MAIN

# while True:
#     asyncio.run(updateSystemSTATE())
    
#     # add delay?


# SHUTDOWN
servo.shutdown()