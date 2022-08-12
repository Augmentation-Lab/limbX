""""
DEMO SCRIPT
demonstrates tentacle functionality
"""
import driver
from time import sleep

def demo(demoMoveSegments=False, demoExploreWorkspace=False, demoGrab=False, demoRelease=False, demoWaveHello=False):
    if demoMoveSegments: moveSegments()
    if demoExploreWorkspace: exploreWorkspace()
    if demoGrab: grab()
    if demoRelease: release()
    if demoWaveHello: waveHello()
    driver.shutdown()

demo(demoMoveSegments=True, demoGrab=True, demoRelease=True)

# SINGLE MOVES

def moveTo(targetRelPos):
    print("moveTo(target={target})")
    driver.move(targetRelPos)

def grab():
    print("grab()")
    driver.grab()

def release():
    print("release()")
    driver.release()

# SEQUENCES

def moveSegments():
    print("demoSegments()")
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

def exploreWorkspace():
    driver.resetAngles()
    # implement later: moveTo spherical points within workspace, via producing all combinations of angles given numSegments
    print("exploreWorkspace()")

def waveHello():
    # implement later
    print("waveHello()")


# only implementable in integration with UI
# def moveAndGrab(targetObj):
#     print(f"moveAndGrab(object={targetObj})")
#     driver.executeCommands([{"move": targetObj}, {"grab": targetObj}])

# def moveAndRelease(targetObj):
#     print(f"moveAndRelease(object={targetObj})")
#     driver.executeCommands([{"move": targetObj}, {"release": targetObj}])
