"""
TENTACLE CAMERA SCRIPT
(future: takes an image from the camera, runs computer vision, and)
returns the 3D vector along which the target lies
"""

import numpy as np
from collections import defaultdict

# depracated implementation
# def calculateVector(fov={'x': 60, 'y': 45}, targetXY={'x': 0, 'y': 0}, imgRadius={'x': 640, 'y': 480}):
#     # calculate the x and y angles of the vector
#     def calculateAngle(axis):
#         ratio = (imgRadius["axis"]-targetXY["axis"])/imgRadius["axis"]
#         angle = np.arcsin(ratio, np.sin(fov["axis"]))
#         return angle
    
#     hypoteneus = np.sqrt(targetXY["x"]**2 + targetXY["y"]**2)
#     fov["diagonal"] = np.sqrt(fov["x"]**2 + fov["y"]**2)
#     vector = {'x': calculateAngle("x"), 'y': calculateAngle("y"), 'z': hypoteneus/np.sin(fov["diagonal"])}
#     return vector

def calculateVector(fov={'x': 60, 'y': 45}, targetXYRadius={'x': 10, 'y': 10}, imgRadius={'x': 640, 'y': 480}):
    # calculate the x and y angles of the vector
    zoffset = defaultdict()
    def calculateAngle(axis):
        ratio = (targetXYRadius["axis"])/imgRadius["axis"]
        angle = np.arctan(ratio * np.tan(fov["axis"]))
        zoffset["axis"] = imgRadius["axis"]/np.tan(fov["axis"])
        return angle
    
    assert zoffset["x"] == zoffset["y"], "x and y zoffsets are not equal"
    
    vector = {'xAngle': calculateAngle("x"), 'yAngle': calculateAngle("y"), 'zOffset': zoffset["x"]}
    return vector