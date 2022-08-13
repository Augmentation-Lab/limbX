"""
TENTACLE CAMERA SCRIPT
(future: takes an image from the camera, runs computer vision, and)
returns the 3D vector along which the target lies
"""

import numpy as np
from collections import defaultdict
import subprocess

def capturePhoto():
    # subprocess.Popen(['sh', 'take_photo.sh']) # stops checking button state if take too long to upload photo
    # careful with absolute paths
    print("Taking photo...")
    subprocess.Popen(['raspistill', '-o', '/home/caineardayfio/limbX/integrated/data/query.png'])
    print("Photo taken.")

def calculateVector(fov={'x': 60, 'y': 45}, targetXYRadius={'x': 10, 'y': 10}, imgRadius={'x': 640, 'y': 480}):
    # calculate the x and y angles of the vector
    zoffset = defaultdict()
    def calculateAngle(axis):
        ratio = (targetXYRadius[axis])/imgRadius[axis]
        angle = np.arctan(ratio * np.tan(fov[axis]))
        zoffset[axis] = imgRadius[axis]/np.tan(fov[axis])
        return angle
    
    vector = {'xAngle': calculateAngle("x"), 'yAngle': calculateAngle("y"), 'zOffset': None}
    assert zoffset["x"] == zoffset["y"], "x and y zoffsets are not equal"
    vector['zOffset'] = zoffset["x"]

    return vector
    