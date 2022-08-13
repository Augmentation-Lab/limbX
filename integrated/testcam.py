"""
test pipline: tobiiglasses -> object detection -> rpistill -> vector calculation
"""

from utilities import tcamera
import vision
import interface

def testCamera(fov, imgRadius):
    print("Begin testCamera")
    # start tobii listening
    queryTargetCenter = interface.runInterface()

    # transform queryTargetCenter
    targetXYRadius = {'x': queryTargetCenter[0]-imgRadius["x"], 'y': queryTargetCenter[1]-imgRadius["y"]}
    print("DEBUG targetXYRadius: ", targetXYRadius)
    vector = tcamera.calculateVector(fov=fov, targetXYRadius=targetXYRadius, imgRadius=imgRadius)
    return vector

testCamera(fov={'x': 27, 'y': 20.5}, imgRadius={'x': 2592/2, 'y': 1944/2})