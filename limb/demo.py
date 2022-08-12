""""
DEMO SCRIPT
demonstrates tentacle functionality
"""
import driver
from time import sleep
# import TargetPos
from utilities.classes import TargetPos

anglesDict = {
    "home": {"lr": 0, "bf": 0},
    "left": {"lr": 90, "bf": 0},
    "right": {"lr": -90, "bf": 0},
    "forward": {"lr": 0, "bf": 90},
    "backward": {"lr": 0, "bf": -90},
    "forwardleft": {"lr": 90, "bf": 90},
    "forwardright": {"lr": -90, "bf": 90},
    "backwardleft": {"lr": 90, "bf": -90},
    "backwardright": {"lr": -90, "bf": -90},
}

def demo(
    demoWaveHello=False,
    demoNod=False,
    demoShake=False,
    demoDance=False,
    demoMoveAround=False, 
    demoExploreWorkspace=False,
    demoGrab=False,
    demoRelease=False,
    demoMoveTo=False):

    driver.initialize()
    if demoMoveAround:
        demoMoveAround()
    if demoWaveHello:
        demoWaveHello()

    # if demoExploreWorkspace:
    #     # implement later: moveTo spherical points within workspace, via producing all combinations of angles given numSegments
    #     pass
    # if demoGrab:
    #     driver.grab()
    # if demoRelease:
    #     driver.release()
    # if demoMoveTo:
    #     target = TargetPos(1,2,0)
    #     driver.move()


    driver.shutdown()

# SEQUENCES

def demoMoveAround():
    print("demoMoveAround()")
    driver.resetAngles()

    movements = [
        "home", "left",
        "home", "right",
        "home", "forward",
        "home", "backward",
        "home", "forwardleft",
        "home", "forwardright",
        "home", "backwardleft",
        "home", "backwardright",
        "home"
    ]

    for segment in range(1, len(driver.systemSTATE.numSegments)+1):
        for movement in movements:
            driver.moveSegment(segment, anglesDict[movement])
            sleep(1)

def demoWaveHello():
    print("demoWaveHello()")
    driver.resetAngles()

    movements = [
        "left", "right",
        "left", "right",
        "left", "right"
    ]

    for movement in movements:
        driver.moveSegment(1, anglesDict[movement])
        sleep(1)


def demoNod():
    print("demoNod()")
    driver.resetAngles()

    movements = [
        "forward", "backward",
        "forward", "backward",
        "forward", "backward"
    ]

    for movement in movements:
        driver.moveSegment(1, anglesDict[movement])
        sleep(1)


def demoNod():
    print("demoNod()")
    driver.resetAngles()

    movements = [
        "forward", "backward",
        "forward", "backward",
        "forward", "backward"
    ]

    for movement in movements:
        driver.moveSegment(1, anglesDict[movement])
        sleep(1)

def demoDance():
    print("demoDance()")
    driver.resetAngles()

    movements = [
        "forward", "backward",
        "left", "right",
        "forward", "backward",
        "left", "right"
    ]

    for segment in range(1, len(driver.systemSTATE.numSegments)+1):
        for movement in movements:
            driver.moveSegment(1, anglesDict[movement])
            sleep(1)
        sleep(1)

demo(demoMoveAround=True, demoWaveHello=True, demoNod=True, demoDance=True)