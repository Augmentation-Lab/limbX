"""
JOYSTICK SCRIPT
using a joystick to fine-control the tentacle

COMMANDS
pressfor3seconds: grab / release
noPress: segment 0 (lr)
press1x: segment 1 (lr, bf)
press2x: segment 2 (lr, bf)
press3x: segment 3 (lr, bf)
"""

import driver

def fineControl(segment, angles):
    driver.moveSegment(segment, angles)

while True:
    
    segment, direction = input("segment, direction: ").split(",")