"""
DRIVER SCRIPT
integrates all scripts and executs control system
"""

# IMPORTS & CLASSES

from blinker import Signal
import yaml
from time import sleep
from classes import SystemState, Params, SignalTarget, TargetPos
import servo, smart, client,  final.vision as vision, hand

# is this global appropriate?
global systemSTATE

# INITIALIZATION

def initialize():

    with open("config.yml") as f:
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

def executeCommand(signal):

    assert signal.type in ["move", "release", "moveAndGrab", "moveAndRelease"], "signal.type is invalid"

    # PROCESS SIGNAL

    if signal.type == "move":
        # assert isinstance(signal.target, SignalTarget), "signal.target is invalid"
        # assert signal.target.imgData is None, "unnecessary imgData in signal.target"
        # assert signal.target.objLabel is None, "unnecessary objLabel in signal.target"
        # assert signal.target.relPos is not None, "signal.target.relPos is invalid"
        assert isinstance(signal.target, TargetPos), "signal.target is invalid"
        print("SIGNAL: move")
        move(signal.target)
        
    if signal.type == "release":
        print("SIGNAL: release")
        # does any signal information need to be passed into release?
        hand.release()

    if signal.type == "moveAndRelease":
        assert isinstance(signal.target, TargetPos), "signal.target is invalid"
        print("SIGNAL: moveAndRelease")
        moveAndRelease(signal.target)

    if signal.type == "moveAndGrab": 
        assert isinstance(signal.target, SignalTarget), "signal.target is invalid"
        targetRelPos = vision.get_target_rel_pos(signal.target)
        assert isinstance(targetRelPos, TargetPos), "targetRelPos is invalid"
        print("SIGNAL: moveAndGrab")
        moveAndGrab(targetRelPos)

# all commands modular s.t. possible to directly trigger from different interfaces

def move(targetRelPos):
    targetAngles = smart.calculateTargetAngles(systemSTATE.servoDict, targetRelPos)
    servo.batchSetAngles(targetAngles)

def moveAndRelease(targetRelPos):
    move(targetRelPos)
    hand.release()
    pass

def moveAndGrab(targetRelPos):
    move(targetRelPos)
    hand.grab()

