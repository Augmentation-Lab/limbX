"""
TENTACLE CAMERA SCRIPT
returns the 3D vector along which the target lies
"""

import numpy as np
from collections import defaultdict
from sympy import *

# Takes in two line segments that span the FOV of the camera at different, known distances
# INPUTS
# d1/2: the distance to the first/second line segment from the camera. note that d1 < d2. Also note that d2 is the distance away from the camera origin, not d1
# span1/2: the width spanned by the first/second line segment from end to end of the camera FOV. note that span1 < span2
# OUTPUTS
# fovAngle: The angle of the FOV
# fovDist: the FOV origin's distance from the camera


def getFovAngleDist(d1, d2, span1, span2):
    # The distance from the nearest plane (d1) to the FOV origin
    line_dist_fov = (span1*(d2-d1))/(span2-span1)
    # The angle of the FOV
    fovAngle = 2*np.arctan((span1/2)/line_dist_fov)
    # The distance from the camera origin to the FOV origin
    fovDist = line_dist_fov - d1
    return fovAngle, fovDist

# Takes in a point on the camera plane and outputs a vector from the FOV origin to the point on the camera plane
# IF you were to follow that real life vector, you would come across the target object at some point
# INPUT:
# r: ratio between a) the distance (in pixels) from the center of the image to the target position on the image and b) the distance (in pixels) from the center of the image to the end of the image (i.e. half the width of the image)
# OUTPUT:
# alpha: The angle between the vertical of the camera FOV (i.e. the angle bisector of the FOV) and the object of interest


def getPointAngle(r, fovDist, fovAngle):
    # omega: width of one side of the camera plane in real world units (i.e. half the total width)
    omega = fovDist * np.tan(fovAngle/2)
    # k: the length from the angle bisector the to the target object in real world units
    k = r*omega
    alpha = np.arctan(k/fovDist)
    # adjust for the target object being on either the left side or the right side of the FOV angle bisector
    return alpha


fovAngle, fovDist = getFovAngleDist(1, 3, 5/2, 4)

fovAngle  # fovAngle = 0.718
fovDist  # fovDist = 10/3

alpha = getPointAngle(1/3, fovDist, fovAngle)
alpha  # alpha = 0.124

# NOTE: THE BELOW FUNCTION ASSUMES WE ARE IN 2D. To use 3D, in whcih we have multiple FOV angles and such, we must
# solve for the equation of a 3D vector and a sphere. Only execute this once you have verified it works in 2D though.
# Given the "depth" (i.e. how far away it is), find the intersection of the circle around the camera and the vector (at angle alpha).
# This is the exact location of the target object.
# INPUT:
# objDist: The distnace the object is from the camera
# OUTPUT:
# Camera2Obj: The location of the object in 3D space relative to the camera


def getObjectLocation(objDist, alpha, fovDist):
    # Note that origin point (0, 0) is the camera's location
    # --!-- Solution 1 --!--
    # Calculate (the x-value of) the intersection of the semi-circle and the vector
    sol1 = (2*fovDist*cot(alpha) + sqrt(-4*fovDist**2+4 *
                                        objDist**2*cot(alpha)**2 + 4*fovDist**2))/(2*(cot(alpha)**2+1))
    # --!-- Solution 2 --!--
    # Equation of the circle around the camera (i.e. the possible places the target object can be)
    x, r = symbols('x r')
    circle_eq = sqrt(r**2 - x**2)
    circle_eq = circle_eq.subs([(r, objDist)])
    # Equation of the vector from the FOV origin through the target object
    vec_eq = 1/tan(alpha) * x - fovDist
    sol2 = solve(circle_eq - vec_eq, x)

    assert len(sol2) == 1
    assert sol1 - sol2[0] < 0.01

    # Calculate the y-value of the intersection of the semi-circle and the vector
    y = sqrt(objDist**2 - sol1**2)

    # Get the vector from the camera to the target object
    Camera2Obj = Matrix([sol1, y])
    return Camera2Obj


getObjectLocation(1, 0.01, 4)
