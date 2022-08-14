"""
SMART SCRIPT
calculates control sequences
"""
from sympy import *
import math
# Lenghts of the segments in meters
SEG_2 = 1
SEG_3 = 1.5

# NOTE:
# x-axis is left-right
# y-axis is forward backward
# z-axis is up down
"""
servoIdx: the index of the servos for that segment (the same as the key in config.yml)
central:
    The angles for the 4 quadrants of the central servo
seg1:
    the position of the tip of the first stage relative to the central servo when the servo is at a preset bend amount
    The first stage only operates at 4 distinct angles.
    As such, in our callibration, we just "tense" the tentaclea fixed amount and rotate it around the central servo.
    lr and ud represent the initial "tensed" values of the servos
    x, y, and z represent the distance (in meters) from the central servo to the tip of the first stage
seg2:
    key-value paris are the degrees of the servos, followed by the angle (alpha and beta) achieved by the tentacle at those servo degrees
    Note that alpha is the angle taken forward from the z-axis (it becomes >180 when you cross into the negative x-axis)
    Beta is the angle taken counter clockwise from the x-axis
    When we calibrate seg2, we put it in the top right default position and then measure the angles of the servos
seg3:
    servoActualAngle consists of 3 ordered pairs
    The first pair is the servo angle for the second segment
    The second pair is the servo angle for the third segment
    The third pair is the actual angle the third segment is at
    The structure used for the first pair of angles is the same as thast in seg2
    The structure used for the second pair of angles is the same as thast in seg2,
    in that we are getting the angle measures relative to vertical (not the previous segment) as well the x-axis (again, not the previous segment)
"""

CALIBRATE = {
    "central": {
        "servoIdx": 0,
        "bl": 90,
        "br": 135,
        "tl": 155,
        "tr": 180
    },
    "seg1": {
        "servoIdx": 1,
        "x": 1,
        "y": 1/3,
        "z": 2,
        "preset": {
            "lr": 40,
            "ud": 45
        }
    },
    "seg2": {
        "servoIdx": 2,
        "servoActualAngle": {
            0: [(90, 90), (-90,-40)],
            1: [(90, 135), (-39, 34)],
            2: [(90, 180), (23,23)],
            3: [(135, 90), (35, 23)],
            4: [(135, 135), (32,41)],
            5: [(135, 180), (12,203)],
            6: [(180, 90), (18,233)],
            7: [(180, 135), (18,235)],
            8: [(180, 180), (77,22)],
        }
    },
    "seg3": {
        "servoIdx": 3,
        "servoActualAngle": {
            0: [(190, 135), (90, 90), (90, 30)],
            1: [(90, 90), (90, 135), (90, 135)],
            2: [(90, 90), (90, 180), (90, 180)],
            3: [(90, 135), (135, 90), (135, 90)],
            4: [(90, 135), (135, 135), (135, 135)],
            5: [(90, 135), (135, 180), (135, 180)],
            6: [(135, 90), (180, 90), (180, 90)],
            7: [(135, 90), (180, 135), (180, 135)],
            8: [(135, 90), (180, 180), (180, 180)],
        }
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
        targetAngles[CALIBRATE["central"]["servoIdx"]] = {"central": CALIBRATE["central"]["tr"]}
        targetAngles[CALIBRATE["seg1"]["servoIdx"]] = {
            "lr": CALIBRATE["seg1"]["preset"]["lr"],
            "ud": CALIBRATE["seg1"]["preset"]["ud"]
        }
    # bottom right quadrant
    elif(targetRelPos.x >= 0 and targetRelPos.z < 0):
        v1 = Matrix([CALIBRATE["seg1"]["x"], CALIBRATE["seg1"]["y"], -CALIBRATE["seg1"]["z"]])

        targetAngles[CALIBRATE["central"]["servoIdx"]] = {"central": CALIBRATE["central"]["br"]}
        targetAngles[CALIBRATE["seg1"]["servoIdx"]] = {
            "lr": CALIBRATE["seg1"]["preset"]["lr"],
            "ud": CALIBRATE["seg1"]["preset"]["ud"]
        }
    # top left quadrant
    elif(targetRelPos.x < 0 and targetRelPos.z >= 0):
        v1 = Matrix([-CALIBRATE["seg1"]["x"], CALIBRATE["seg1"]["y"], CALIBRATE["seg1"]["z"]])
        targetAngles[CALIBRATE["central"]["servoIdx"]] = {"central": CALIBRATE["central"]["tl"]}
        targetAngles[CALIBRATE["seg1"]["servoIdx"]] = {
            "lr": CALIBRATE["seg1"]["preset"]["lr"],
            "ud": CALIBRATE["seg1"]["preset"]["ud"]
        }
    # bottom left quadrant
    elif(targetRelPos.x < 0 and targetRelPos.z < 0):
        v1 = Matrix([-CALIBRATE["seg1"]["x"], CALIBRATE["seg1"]["y"], -CALIBRATE["seg1"]["z"]])
        targetAngles[CALIBRATE["central"]["servoIdx"]] = {"central": CALIBRATE["central"]["bl"]}
        targetAngles[CALIBRATE["seg1"]["servoIdx"]] = {
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
            "ud": Servo(name="1_ud", pin=2)
        },
        2: {
            "lr": Servo(name="2_lr", pin=3),
            "ud": Servo(name="2_ud", pin=4)
        },
        3: {
            "lr": Servo(name="3_lr", pin=5),
            "ud": Servo(name="3_ud", pin=6)
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
            "ud": 15
        },
        2: {
            "lr": 20,
            "ud": 25
        },
        3: {
            "lr": 15,
            "ud": 90
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

    def vec2angles(vec):
        # theta:
        #   Description: the angle from the z-axis to vec
        #   Purpose: which servo combination best suits the second stage.
        #   we wish to find a servo combination such that it's ifrst angle is as close to theta as possible
        #   Note: v \dot [0; 0; 1] = |v| cos(theta) -> theta = acos(v/|v| \dot [0; 0; 1])
        theta = acos( (vec/vec.norm()).dot(Matrix([0, 0, 1])) )
        theta = math.degrees(theta)

        # phi:
        #   Description: the angle from the x-axis to vec projected onto the x-y axis
        #   Purpose: which servo combination best suits the second stage.
        #   we wish to find a servo combination such that it's second angle is as close to phi as possible
        #   Note: [vec(0), vec(1), 0] \dot [1; 0; 0] = |[vec(0), vec(1), 0]| cos(phi) -> phi = acos([vec(0), vec(1), 0]/|[vec(0), vec(1), 0]| \dot [1; 0; 0])
        phi = acos( ( Matrix([vec[0], vec[1], 0])/(Matrix([vec[0], vec[1], 0]).norm()) ).dot(Matrix([1, 0, 0])) )
        phi = math.degrees(phi)

        # The dot product is always the closest angle between the two lines, therefore, it is always less than 180
        # this is fine for theta, but we need the full ROM for 360 degrees
        if(vec[0] < 0):
            phi = 360 - phi
        return theta, phi

    theta, phi = vec2angles(v2)

    # servoAngle:
    #  Description: the set of servo angles that most closely achieves [theta, phi]
    #  Purpose: which servo combination best suits the second stage.
    #  we wish to find a servo combination such that it's angles are as close to [theta, phi] as possible
    #  loop through the key value pairs in the dictionary CALIBRATE['seg2']
    #  NOTE: In the future, we should find the closest servo angles by some type of lienar interpolation (our function is actualAngle -> servoAngle, which is R^2 -> R^2)

    # the index of the servo angle that yields the closest actual angle to [theta, phi]
    minError = None # {'index': 0, 'error': 1}
    for option, servoActualCombo in CALIBRATE["seg2"]["servoActualAngle"].items():
        actualAngle = servoActualCombo[1]
        error = (actualAngle[0] - theta)**2 + (actualAngle[1] - phi)**2
        if minError == None:
            minError = {'index': option, 'error': error}
        else:
            if error < minError['error']:
                minError = {'index': option, 'error': error}

    # This is the ideal servo angle based on the actual servo angel that would be achieved
    # as a pair of tuples like htis [(180, 90), (71, 57)]
    validCombo = CALIBRATE["seg2"]["servoActualAngle"][minError['index']]
    servoAngles = validCombo[0]
    actualAngles = validCombo[1]
    targetAngles[CALIBRATE["seg2"]["servoIdx"]] = {
        "lr": servoAngles[0],
        "ud": servoAngles[1]
    }

    theta, phi = vec2angles(v3)
    # the index of the servo angle that yields the closest actual angle to [theta, phi] AND the second segment's existing angle values
    minError = None # {'index': 0, 'error': 1}
    for option, servoActualCombo in CALIBRATE["seg3"]["servoActualAngle"].items():
        # servoActualCombo = [(180, 90), (71, 57), (33, 31)]
        seg2Calibrate = servoActualCombo[0]
        actualAngle = servoActualCombo[2]
        # the error betwenn the calibreated actual angle and the target actual angle
        errorAngle = (actualAngle[0] - theta)**2 + (actualAngle[1] - phi)**2
        # Get the error between the calibrated servo angles for segment 2 and the actual servo angles of segment 2
        errorSeg2 = (seg2Calibrate[0] - servoAngles[0])**2 + (seg2Calibrate[1] - servoAngles[1])**2
        error = errorAngle + errorSeg2
        if minError == None:
            minError = {'index': option, 'error': error}
        else:
            if error < minError['error']:
                minError = {'index': option, 'error': error}

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