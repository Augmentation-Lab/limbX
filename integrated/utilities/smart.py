"""
SMART SCRIPT
calculates control sequences
"""
from sympy import *

# Lenghts of the segments in meters
SEG_2 = 1
SEG_3 = 1.5

# NOTE:
# x-axis is left-right
# y-axis is forward backward
# z-axis is up down
"""
the position of the tip of the first stage relative to the central servo when the servo is at a preset bend amount
The first stage only operates at 4 distinct angles.
As such, in our callibration, we just "tense" the tentaclea fixed amount and rotate it around the central servo.
lr and ud represent the initial "tensed" values of the servos
x, y, and z represent the distance (in meters) from the central servo to the tip of the first stage
"""
CALIBRATE = {
    "seg1": {
        "x": 1,
        "y": 1/3,
        "z": 2,
        "preset": {
            "lr": 40,
            "ud": 45
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
    v1:
        Type: Matrix
        Description: the location of our first stage
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
        v1 = Matrix([-CALIBRATE["seg1"]["x"], CALIBRATE["seg1"]["y"], -CALIBRATE["seg1"]["z"]])
        targetAngles[0] = {"central": 105}
        targetAngles[1] = {
            "lr": CALIBRATE["seg1"]["preset"]["lr"],
            "ud": CALIBRATE["seg1"]["preset"]["ud"]
        }
    else:
        raise Exception("Invalid targetRelPos")
    return targetAngles, v1


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
    targRelPos = Matrix([targetRelPos.x, targetRelPos.y, targetRelPos.z])
    targetAngles = {}
    # get v1 (vector from central servo to the tip of stage 1) and set corresponding angles
    targetAngles, v1 = getV1(targetAngles, targetRelPos)

    # get v2 (vector from the tip of stage 1 to tip of stage 2) and set corresponding angles
    v2 = getSphereIntersection(R_in=SEG_2, r_in=SEG_3, a_in=(targRelPos - v1)[0], b_in=(targRelPos - v1)[1], c_in=(targRelPos - v1)[2], theta_in=pi)

    # get v3 (vector from the tip of stage 2 to tip of stage 3) and set corresponding angles
    v3 = targRelPos - (v1 + v2)

    v1_len = v1.norm().evalf()
    v2_len = v2.norm().evalf()
    v3_len = v3.norm().evalf()

    # Length of v1 == Length of the first segment
    assert v1_len == sqrt(CALIBRATE["seg1"]["x"]**2 + CALIBRATE["seg1"]["y"]**2 + CALIBRATE["seg1"]["z"]**2).evalf()
    # Length of v2 == Length of the second segment
    assert v2_len - SEG_2 < 0.001
    # Length of v2 == Length of the second segment
    assert v3_len - SEG_3 < 0.001
    # the end effector intended position == end effector actual position
    assert (targRelPos - (v1 + v2 + v3)).norm() < 0.001

    return targetAngles


def getSphereIntersection(R_in, r_in, a_in, b_in, c_in, theta_in):
    """
    INPUTS
    R:
        description: radius of the first sphere
        application: length from tip of first segment to tip of the second segment
    r:
        description: radius of the second sphere
        application: length from tip of second segment to tip of the third segment
    a, b, c:
        description: x/y/z-distance from the first sphere to the second sphere
        application: the x/y/z-distance from the tip of the first stage to the tip of the last stage (i.e. the target position)
    theta: an angle of the circle intersection, this uniquely defines the intersec_point

    OUTPUTS
    intersec_point:
        Type: Matrix
        Description: a point on the intersection between the two spheres
        Purpose: the point, relrative to the tip of the first stage, where the tip of stage two should go to and the base of stage 3 should start
    """
    R, r, a, b, c = symbols('R r a b c')
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
    v = (v/v.norm())*dist


    # The equation of the plane that is normal to this vector and also goes through this vector
    # Source: https://math.stackexchange.com/questions/753113/how-to-find-an-equation-of-the-plane-given-its-normal-vector-and-a-point-on-the
    x, y = symbols('x y')
    # plane equation: ax + by + cz = d -> z = (d - ax - by)/c
    plane_z = (v.dot(v) - v[0]*x - v[1]*y)/(v[2])
    # Project the center of the intersection circle onto the x-y plane
    p = Matrix([v[0], v[1], 0])
    """
    ### EEEEEEK EVERYTHING BELOW HERE IS WRONG
    The problem is that I tried projecting the point from the center of the intersection circle onto the x-y plane,
    # and then drawing a circle on the x-y plane around this projected point,
    # and then projecting back up to the plane
    # I expected tehse new points projected onto the plane would project onto the plane as a circle of the specified radius at the specified position
    # Unfortunately, this is not correct. Projecting a circle up onto the plane gives you an oblong shape that is vaguely circle-like,
    # but most definitely not a circle!!!

    # The new strategy is to get the plane that we had before, get a random vector on the plane, normalize it,
    # then find it's complement, and then get linear combinations of these two vectors based on an input theta


    # make sure that w_1^2 + w_2^2=1 -> 0 = 1 - w_1^2 - w_2^2 is satisfied
    assert 1 - w_in[0]**2 - w_in[1]**2 < 0.001
    assert w_in[2] == 0

    w1, w2, w3 = symbols('w1 w2 w3')
    # q: a point on the flat circle's intersection
    q = p + Matrix([w1, w2, w3])*radius

    # given a 2D coordinate, q, find the associated z-value when mapped onto the plane
    intersec_point = Matrix([q[0], q[1], plane_z])
    intersec_point = intersec_point.subs([(w1, w_in[0]), (w2, w_in[1]), (w3, w_in[2])])
    """

    # We want to generate two new "basis-vectors", q and s, for generating our circle around the intersection point
    # First, get a new point on the plane that is distinct from v
    inter = p + Matrix([1, 1, 0])
    q = Matrix([inter[0], inter[1], plane_z.subs([(x, inter[0]), (y, inter[1])])])
    # make q a vector perpendicular to v
    q = q - v
    q = q/q.norm()
    # get a vector perpendicular to both q and v
    s = v.cross(q)
    s = s/s.norm()

    # circ: create a vector, relative to v, that represents a point on the intersection circle
    # (by being a trigonometric linear combination of our two normalized vectors)
    circ = (q*cos(theta_in) + s*sin(theta_in))*radius
    intersec_point = v + circ
    return intersec_point