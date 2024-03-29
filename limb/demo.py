""""
DEMO SCRIPT
demonstrates tentacle functionality
"""
from time import sleep
# import TargetPos
from utilities.classes import TargetPos
from sympy import *
from utilities import servo, smart, hand
import utilities.servoDict as servoDict
from utilities.keyboard import controlWithKeyboard
# INITIALIZATION


def demo(demoKeyboardControl=False, demoExploreWorkspace=False, demoMoveAround=False, demoMoveTo=False):
    systemSTATE = servoDict.initialize()
    if demoKeyboardControl:
        print("demoKeyboardControl()")
        controlWithKeyboard(systemSTATE)
    if demoMoveAround:
        print("demoMoveAround()")
        demoMoveAround(systemSTATE)
    if demoExploreWorkspace:
        # implement later: moveTo spherical points within workspace, via producing all combinations of angles given numSegments
        print("exploreWorkspace()")
    if demoMoveTo:
        # position relative ot the central servo
        target = TargetPos(2, 1, 3)
        print(f"moveTo(target={target})")
        targetAngles = smart.calculateTargetAngles(
            systemSTATE.servoDict, target)
        servo.batchSetAngles(systemSTATE.servoDict, targetAngles)

    servo.shutdown(systemSTATE.servoDict)

# SEQUENCES


def demoMoveAround(systemSTATE):
    print("demoMoveAround()")
    anglesDict = {
        "home": {"lr": 0, "ud": 0},
        "left": {"lr": 90, "ud": 0},
        "right": {"lr": -90, "ud": 0},
        "up": {"lr": 0, "ud": 90},
        "down": {"lr": 0, "ud": -90},
        "upleft": {"lr": 90, "ud": 90},
        "upright": {"lr": -90, "ud": 90},
        "downleft": {"lr": 90, "ud": -90},
        "downright": {"lr": -90, "ud": -90},
    }

    movements = [
        "home", "left",
        "home", "right",
        "home", "up",
        "home", "down",
        "home", "upleft",
        "home", "upright",
        "home", "downleft",
        "home", "downright",
        "home"
    ]

    for segment in range(1, len(systemSTATE.numSegments)+1):
        for movement in movements:
            servo.batchSetAngles(systemSTATE.servoDict, {
                [segment]: {
                    "lr": anglesDict[movement]["lr"],
                    "ud": anglesDict[movement]["ud"]
                }
            })
            sleep(1)


# demo(demoMoveAround=True)
demo(demoKeyboardControl=True)  # , demoMoveTo=True)
