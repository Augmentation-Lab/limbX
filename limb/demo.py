""""
DEMO SCRIPT
demonstrates tentacle functionality
"""
import driver
from time import sleep
# import TargetPos
from utilities.classes import TargetPos
from sympy import *

def demo(demoMoveAround=False, demoExploreWorkspace=False, demoGrab=False, demoRelease=False, demoWaveHello=False, demoMoveTo=False):
    driver.initialize()
    if demoMoveAround:
        demoMoveAround()
    if demoExploreWorkspace:
        driver.resetAngles()
        # implement later: moveTo spherical points within workspace, via producing all combinations of angles given numSegments
        print("exploreWorkspace()")
    if demoGrab:
        print("grab()")
        driver.grab()
    if demoRelease:
        print("release()")
        driver.release()
    if demoWaveHello:
        # implement later
        print("waveHello()")
    if demoMoveTo:
        # position relative ot the central servo
        target = TargetPos(2,1,3)
        print(f"moveTo(target={target})")
        #driver.move(target)
        driver.moveCentral(135)
        sleep(5)
        #driver.moveCentral(270)
    driver.shutdown()

# SEQUENCES

def demoMoveAround():
    print("demoMoveAround()")
    driver.resetAngles()
    anglesDict = {
        "home": {"lr": 0, "bf": 0},
        "left": {"lr": 90, "bf": 0},
        "right": {"lr": -90, "bf": 0},
        "up": {"lr": 0, "bf": 90},
        "down": {"lr": 0, "bf": -90},
        "upleft": {"lr": 90, "bf": 90},
        "upright": {"lr": -90, "bf": 90},
        "downleft": {"lr": 90, "bf": -90},
        "downright": {"lr": -90, "bf": -90},
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

    for segment in range(1, len(driver.systemSTATE.numSegments)+1):
        for movement in movements:
            driver.moveSegment(segment, anglesDict[movement])
            sleep(1)

demo(demoMoveTo=True)