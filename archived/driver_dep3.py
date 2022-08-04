"""
DRIVER SCRIPT
executes control system
"""

# IMPORTS & CLASSES

import servo, smart
from classes import systemSTATE

# INITIALIZATION

def initialize():
    servoPins = systemSTATE.servoPins
    servo.initialize(servoDict, servoPins)
    
# CONTROL SYSTEM

def calculateCtrlSeq(targetRelPos):
    # calculate control sequence necessary to move grabber to target
    # targetRelPos in the form: {'x': 0, 'y': 0, 'z': 0}
    ctrlSeq = smart.calculateCtrlSeq(systemSTATE.servoAngles, targetRelPos)
    return ctrlSeq

def executeCtrlSeq(ctrlSeq):

    pass

def shutdown():
    servo.shutdown()