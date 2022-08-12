"""
SMART SCRIPT
calculates control sequences
"""
from sympy import *

<<<<<<< HEAD
=======
# Lenghts of the segments in meters
SEG_1 = 0.8
SEG_2 = 0.4
SEG_3 = 0.2

# NOTE:
# x-axis is left-right
# y-axis is forward backward
# z-axis is up down
CALIBRATE = {
    # the position of the tip of the first stage relative to the central servo when the servo is at a preset bend amount
    "seg1": {
        "x": 1,
        "y": 2,
        "z": 3,
        "preset": {
            "lr": 40,
            "ud": 40
        }
    },
    "seg2": {
        "hi": "okay"
    }
}

def getV1(targetAngles, targetRelPos):
    """
    INPUT:
    targetAngles: dictionary of angles to set
    targetRelPos: 3D vector describing the location to go to from the central servo to the destination
    OUTPUT:
    targetAngles: the angles to set, with the first stage "filled in"
    v1: the location of our first stage
    """

    # top right quadrant
    if(targetRelPos.x >= 0 and targetRelPos.z >= 0):
        v1 = Matrix([CALIBRATE["seg1"]["x"], CALIBRATE["seg1"]["y"], CALIBRATE["seg1"]["z"]])
        targetAngles[0] = {"central": 35}
        targetAngles[1] = {
            "lr": CALIBRATE["seg1"]["preset"]["lr"],
            "ud": CALIBRATE["seg1"]["preset"]["ud"]
        }
    # bottom right quadrant
    elif(targetRelPos.x >= 0 and targetRelPos.z < 0):
        v1 = Matrix([CALIBRATE["seg1"]["x"], CALIBRATE["seg1"]["y"], -CALIBRATE["seg1"]["z"]])

        targetAngles[0] = {"central": 70}
        targetAngles[1] = {
            "lr": CALIBRATE["seg1"]["preset"]["lr"],
            "ud": CALIBRATE["seg1"]["preset"]["ud"]
        }
    # top left quadrant
    elif(targetRelPos.x < 0 and targetRelPos.z >= 0):
        v1 = Matrix([-CALIBRATE["seg1"]["x"], CALIBRATE["seg1"]["y"], CALIBRATE["seg1"]["z"]])
        targetAngles[0] = {"central": 90}
        targetAngles[1] = {
            "lr": CALIBRATE["seg1"]["preset"]["lr"],
            "ud": CALIBRATE["seg1"]["preset"]["ud"]
        }
    # bottom left quadrant
    elif(targetRelPos.x < 0 and targetRelPos.z < 0):
        v1 = Matrix([-CALIBRATE["seg1"]["x"], -CALIBRATE["seg1"]["y"], -CALIBRATE["seg1"]["z"]])
        targetAngles[0] = {"central": 105}
        targetAngles[1] = {
            "lr": CALIBRATE["seg1"]["preset"]["lr"],
            "ud": CALIBRATE["seg1"]["preset"]["ud"]
        }
    else:
        raise Exception("Invalid targetRelPos")
    return targetAngles, v1


>>>>>>> e81d43f1840d09cc4e7d40f6771e3135d770a0bd
def calculateTargetAngles(servoDict, targetRelPos):
    """
    a 3D vector describing the location to go to from the tip of the first stage
    targetRelPos in the form:
    TargetPos(x=10,y=20,z=5)

    servoDict in the form:
    {
        1: {
            "lr": Servo(name="1_lr", pin=1),
            "bf": Servo(name="1_bf", pin=2)
        },
        2: {
            "lr": Servo(name="2_lr", pin=3),
            "bf": Servo(name="2_bf", pin=4)
        },
        3: {
            "lr": Servo(name="3_lr", pin=5),
            "bf": Servo(name="3_bf", pin=6)
        }
    }

    access angle via:
    angle = servoDict[segment][axis].currentAngle
    or use the following to get a dictionary of angles:

    servoAngles = {
        segment : {
            axis : servoDict[segment][axis].currentAngle for axis in servoDict[segment].keys()
        } for segment in servoDict.keys()
    }

    targetAngles in the form:
    {
        0: {
            "central": 90
        }
        1: {
            "lr": -10,
            "bf": 15
        },
        2: {
            "lr": 20,
            "bf": 25
        },
        3: {
            "lr": 15,
            "bf": 90
        }
    }
    """

    targetAngles = {}
    # get v_1 (starting from central servo) and set corresponding angles
    targetAngles, v1 = getV1(targetAngles, targetRelPos)
    print(targetAngles)
    print(v1)
    print("HI")
    #targetAngles, v1 = getV2(targetAngles, targetRelPos)


    # Reset the central servo and first stage servo
    intersec_point = getSphereIntersection(r_in=1, R_in=1.5, a_in=sqrt(2/3), b_in=sqrt(2/3), c_in=sqrt(2/3), w_in=[0, 1, 0])
    # r_in: length of segment 2
    # R_in: length of esgment 3
    # a_in, b_in, c_in: position of the object

    # get the angle between the tip of the first stage


    return targetAngles

<<<<<<< HEAD
"""
OUTPUTS
radius: gets the radius of the circle intersection of the two spheres: https://mathworld.wolfram.com/Sphere-SphereIntersection.html
dist: the distance to the center of the intersection from the center of the first sphere: https://mathworld.wolfram.com/Sphere-SphereIntersection.html
angles: the two angles that lead to the intersection of the two spheres
=======
def Calibrate():
    # iterate from 0 to 270 degrees on teh servo
    # print the current servo angle
    # note at what points the tentacle is at -45, 0, and 45 degrees from vertical

    # servo angle: corresponding tentacle angle
    return CALIBRATE

>>>>>>> e81d43f1840d09cc4e7d40f6771e3135d770a0bd

def getSphereIntersection(r_in, R_in, a_in, b_in, c_in, w_in):
    """
    INPUTS
    r: radius of the first sphere
    R: radius of the second sphere
    a: x-distance from the first sphere to the second sphere
    b: y-distance from the first sphere to the second sphere
    c: z-distance from the first sphere to the second sphere
    w: a 2D normalized vector representing the point on the circle to get

    OUTPUTS
    angles: the two angles that lead to the intersection of the two spheres
    """

    r, R, a, b, c = symbols('r R a b c')
    # d: distance from the center of the first sphere to the center of the second sphere
    d = sqrt(a**2 + b**2 + c**2)

    # dist: the distance to the center of the intersection from the center of the first sphere: https://mathworld.wolfram.com/Sphere-SphereIntersection.html
    dist = (d**2 - r**2 + R**2)/(2*d)
    dist = dist.subs([(r, r_in), (R, R_in), (a, a_in), (b, b_in), (c, c_in)])

    # radius: gets the radius of the circle intersection of the two spheres: https://mathworld.wolfram.com/Sphere-SphereIntersection.html
    radius = 1/(2*d)*sqrt(4*d**2*R**2 - (d**2 - r**2 + R**2)**2)
    radius = radius.subs([(r, r_in), (R, R_in), (a, a_in), (b, b_in), (c, c_in)])

    # vector from the origin to the center of the circle intersection
    v = Matrix([a_in, b_in, c_in])
    # The equation of the plane that is normal to this vector and also goes through this vector
    # Source: https://math.stackexchange.com/questions/753113/how-to-find-an-equation-of-the-plane-given-its-normal-vector-and-a-point-on-the
    x, y = symbols('x y')
    # plane equation: ax + by + cz = d -> z = (d - ax - by)/c
    plane_z = (v.dot(v) - v[0]*x - v[1]*y)/(v[2])
    # get the plane's z-point at the x-y we specify in w
    plane_z = plane_z.subs([(x, w_in[0]), (y, w_in[1])])

    # Get the vector representing the center of the circle intersection
    p = (v/v.norm())*dist
    # Project the center of the intersection circle onto the x-y plane
    p = Matrix([p[0], p[1], 0])

    # make sure that w_1^2 + w_2^2=1 -> 0 = 1 - w_1^2 - w_2^2 is satisfied
    assert 1 - w_in[0]**2 - w_in[1]**2 < 0.001
    assert w_in[2] == 0

    w1, w2, w3 = symbols('w1 w2 w3')
    # q: a point on the flat circle's intersection
    q = p + Matrix([w1, w2, w3])*radius

    # given a 2D coordinate, q, find the associated z-value when mapped onto the plane
    intersec_point = Matrix([q[0], q[1], plane_z])
    intersec_point = intersec_point.subs([(w1, w_in[0]), (w2, w_in[1]), (w3, w_in[2])])
    return intersec_point