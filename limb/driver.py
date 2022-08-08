"""
DRIVER SCRIPT
integrates /limb scripts to execute control
"""

# IMPORTS & CLASSES

# from blinker import Signal
import yaml
from time import sleep
from limb.utilities.classes import SystemState, Params, TargetObj, TargetPos
from limb.utilities import servo, smart, hand

# INITIALIZATION

def initialize():

    # is this global appropriate?
    global systemSTATE

    with open("limb/config.yml") as f:
        configData = yaml.safe_load(f)
        print("configData", configData)

    systemSTATE = SystemState()
    # get config from config.yml
    servoPins = configData["servoPins"]
    print("servoPins", servoPins)
    systemSTATE.servoDict = servo.initialize(servoPins)
    if systemSTATE.check_initialized() is False:
        raise Exception("System not initialized.")

def shutdown():

    servo.shutdown(systemSTATE.servoDict)
    # should we clean up state here?

def executeCommands(commands):
    """
    commands in the form:
    [{"grab": targetObj}]
    [{"release": targetObj}]
    [{"move": targetRelPos}, {"release": TargetObj}]
    [{"move": targetRelPos}, {"grab": TargetObj}]
    """

    for command in commands:
        commandType = command.keys()[0]
        commandData = command[commandType]

        if commandType == "move":
            assert isinstance(commandData, TargetPos)
            move(commandData)
        
        if commandType == "release":
            # assert isinstance(commandData, TargetObj)
            # release(commandData)
            release()
        
        if commandType == "grab":
            # assert isinstance(commandData, TargetObj)
            # grab(commandData)
            grab()

# all commands modular s.t. possible to directly trigger from different interfaces

def move(targetRelPos):
    targetAngles = smart.calculateTargetAngles(systemSTATE.servoDict, targetRelPos)
    servo.batchSetAngles(targetAngles)

def release():
    hand.release()

def grab():
    hand.grab()

# def release(targetObj):
#     hand.release(targetObj)

# def grab(targetObj):
#     hand.grab(targetObj)

def resetAngles():
    servo.setAllAngles(systemSTATE.servoDict, 0)

def moveSegment(segment, angles):
    servo.moveSegment(systemSTATE.servoDict, segment, angles)

