"""
SMART SCRIPT
calculates control sequences
"""
from sympy import *
import math
import yaml
import utilities.servoDict as servoDictFunc

with open("limb/config.yml") as f:
    calibrationConfig = yaml.safe_load(f)['calibrationDict']
with open("limb/calibration.yml") as f:
    calibrationData = yaml.safe_load(f)
systemSTATE = servoDictFunc.initialize()

# Lenghts of the segments in meters
SEG_2 = 1
SEG_3 = 1.5

# The number of angles between 0 and 2pi to look at in order to minimize error between
# the calibrated servo angles and the optimal servo angles
#NUM_ANGLES = 6

# NOTE:
# x-axis is left-right
# y-axis is forward backward
# z-axis is up down
# alpha angle is the angle from the z-axis, starting clockwise from the POV of the positive x-axis (standing from the right side of the graph)
# beta is angle from the x-axis, starting counterclockwise from the POV of the positive z-axis (standing from a "bird's eye view")


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
            v1 = Matrix([calibrationData["seg1"]["x"],
                        calibrationData["seg1"]["y"], calibrationData["seg1"]["z"]])
            targetAngles[calibrationConfig["central"]["servoIdx"]] = {
                "central": calibrationData["central"]["tr"]}
            targetAngles[calibrationConfig["seg1"]["servoIdx"]] = {
                "lr": calibrationData["seg1"]["preset"]["lr"],
                "ud": calibrationData["seg1"]["preset"]["ud"]
            }
            quadrant = "tr"
        # bottom right quadrant
        elif(targetRelPos.x >= 0 and targetRelPos.z < 0):
            v1 = Matrix([calibrationData["seg1"]["x"], calibrationData["seg1"]
                        ["y"], -calibrationData["seg1"]["z"]])

            targetAngles[calibrationConfig["central"]["servoIdx"]] = {
                "central": calibrationData["central"]["br"]}
            targetAngles[calibrationConfig["seg1"]["servoIdx"]] = {
                "lr": calibrationData["seg1"]["preset"]["lr"],
                "ud": calibrationData["seg1"]["preset"]["ud"]
            }
            quadrant = "br"
        # top left quadrant
        elif(targetRelPos.x < 0 and targetRelPos.z >= 0):
            v1 = Matrix([-calibrationData["seg1"]["x"], calibrationData["seg1"]
                        ["y"], calibrationData["seg1"]["z"]])
            targetAngles[calibrationConfig["central"]["servoIdx"]] = {
                "central": calibrationData["central"]["tl"]}
            targetAngles[calibrationConfig["seg1"]["servoIdx"]] = {
                "lr": calibrationData["seg1"]["preset"]["lr"],
                "ud": calibrationData["seg1"]["preset"]["ud"]
            }
            quadrant = "tl"
        # bottom left quadrant
        elif(targetRelPos.x < 0 and targetRelPos.z < 0):
            v1 = Matrix([-calibrationData["seg1"]["x"], calibrationData["seg1"]
                        ["y"], -calibrationData["seg1"]["z"]])
            targetAngles[calibrationConfig["central"]["servoIdx"]] = {
                "central": calibrationData["central"]["bl"]}
            targetAngles[calibrationConfig["seg1"]["servoIdx"]] = {
                "lr": calibrationData["seg1"]["preset"]["lr"],
                "ud": calibrationData["seg1"]["preset"]["ud"]
            }
            quadrant = "bl"
        else:
            raise Exception("Invalid targetRelPos")
        return targetAngles, v1, quadrant

    # get v1 (vector from central servo to the tip of stage 1) and set corresponding angles
    targetAngles, v1, quadrant = getV1(targetAngles, targetRelPos)

    # for theta in range(0, NUM_ANGLES):
    # get v2 (vector from the tip of stage 1 to tip of stage 2) and set corresponding angles
    v2 = getSphereIntersection(R_in=SEG_2, r_in=SEG_3, a_in=(
        targRelPos - v1)[0], b_in=(targRelPos - v1)[1], c_in=(targRelPos - v1)[2], theta_in=pi)
    # get v3 (vector from the tip of stage 2 to tip of stage 3) and set corresponding angles
    v3 = targRelPos - (v1 + v2)

    v1_len = v1.norm().evalf()
    v2_len = v2.norm().evalf()
    v3_len = v3.norm().evalf()

    # Length of v1 == Length of the first segment
    assert v1_len == sqrt(
        calibrationData["seg1"]["x"]**2 + calibrationData["seg1"]["y"]**2 + calibrationData["seg1"]["z"]**2).evalf()
    # Length of v2 == Length of the second segment
    assert v2_len - SEG_2 < 0.001
    # Length of v2 == Length of the second segment
    assert v3_len - SEG_3 < 0.001
    # the end effector intended position == end effector actual position
    assert (targRelPos - (v1 + v2 + v3)).norm() < 0.001

    def vec2angles(vec):
        # alpha:
        #   Description: the angle from the z-axis to vec
        #   Purpose: which servo combination best suits the second stage.
        #   we wish to find a servo combination such that it's ifrst angle is as close to alpha as possible
        #   Note: v \dot [0; 0; 1] = |v| cos(alpha) -> alpha = acos(v/|v| \dot [0; 0; 1])
        alpha = acos((vec/vec.norm()).dot(Matrix([0, 0, 1])))
        alpha = math.degrees(alpha)

        # beta:
        #   Description: the angle from the x-axis to vec projected onto the x-y axis
        #   Purpose: which servo combination best suits the second stage.
        #   we wish to find a servo combination such that it's second angle is as close to beta as possible
        #   Note: [vec(0), vec(1), 0] \dot [1; 0; 0] = |[vec(0), vec(1), 0]| cos(beta) -> beta = acos([vec(0), vec(1), 0]/|[vec(0), vec(1), 0]| \dot [1; 0; 0])
        beta = acos((Matrix([vec[0], vec[1], 0]) /
                     (Matrix([vec[0], vec[1], 0]).norm())).dot(Matrix([1, 0, 0])))
        beta = math.degrees(beta)

        # The dot product is always the closest angle between the two lines,
        # however, say we have a vector that is just a littlebit counterclockwise of the z-axis, then
        # we would want alpha to be denoted 359 degrees rather than 1 degree. Because 1 degree is already defined
        # to be the thing a little bit clockwise of teh z-axis. Same goes for beta.

        if(vec[1] < 0):
            alpha = 360 - alpha
        if(vec[1] < 0):
            beta = 360 - beta
        return alpha, beta

    # Making sure our coordinate system makes sense, where a vector like [1, -1, 1] -> (alpha ~ 305, beta ~ 315)
    v_test = Matrix([1, -1, 1])
    alpha_test, beta_test = vec2angles(v_test)
    assert (alpha_test - 305.3) < 0.1
    assert (beta_test - 315.0) < 0.1

    alpha, beta = vec2angles(v2)

    # servoAngle:
    #  Description: the set of servo angles that most closely achieves [alpha, beta]
    #  Purpose: which servo combination best suits the second stage.
    #  we wish to find a servo combination such that it's angles are as close to [alpha, beta] as possible
    #  loop through the key value pairs in the dictionary calibrationData['seg2']
    #  NOTE: In the future, we should find the closest servo angles by some type of lienar interpolation (our function is actualAngle -> servoAngle, which is R^2 -> R^2)
    # the index of the servo angle that yields the closest actual angle to [alpha, beta]
    minError = None  # {'index': 0, 'error': 1}
    if(quadrant != "tr"):
        raise Exception("quadrant is not tr")

    for option, servoActualCombo in calibrationData["seg2"][quadrant].items():
        actualAngle = servoActualCombo[1]
        error = (actualAngle[0] - alpha)**2 + (actualAngle[1] - beta)**2
        if minError == None:
            minError = {'index': option, 'error': error}
        else:
            if error < minError['error']:
                minError = {'index': option, 'error': error}

    # This is the ideal servo angle based on the actual servo angel that would be achieved
    # as a pair of tuples like htis [(180, 90), (71, 57)]
    validCombo = calibrationData["seg2"][quadrant][minError['index']]
    # ideal servo angles
    servoAngles = validCombo[0]
    # the actual angle outcome we would expect if we were to move to this servo angle
    actualAngles = validCombo[1]
    targetAngles[calibrationConfig["seg2"]["servoIdx"]] = {
        "lr": servoAngles[0],
        "ud": servoAngles[1]
    }

    alpha, beta = vec2angles(v3)
    # move the third segment around until it's angle is as close to [alpha, beta] as possible
    # use the visual last mile script to actually achieve this
    '''
    This code can be used IF we have calibration values for segment 3
    Because it is probhitive to obtaint these values (and we're going to be adjusting the last segment anyways to get that <2cm precision),
    we instead assume we only have calibration values for segment2
    alpha, beta = vec2angles(v3)
    # the index of the servo angle that yields the closest actual angle to [alpha, beta] AND the second segment's existing angle values
    minError = None  # {'index': 0, 'error': 1}
    for option, servoActualCombo in calibrationData["seg3"]["servoActualAngle"][quadrant].items():
        # servoActualCombo = [(180, 90), (71, 57), (33, 31)]
        seg2Calibrate = servoActualCombo[0]
        actualAngle = servoActualCombo[2]
        # the error betwenn the calibreated actual angle and the target actual angle
        errorAngle = (actualAngle[0] - alpha)**2 + (actualAngle[1] - beta)**2
        # Get the error between the calibrated servo angles for segment 2 and the actual servo angles of segment 2
        errorSeg2 = (seg2Calibrate[0] - servoAngles[0]
                     )**2 + (seg2Calibrate[1] - servoAngles[1])**2
        error = errorAngle + errorSeg2
        if minError == None:
            minError = {'index': option, 'error': error}
        else:
            if error < minError['error']:
                minError = {'index': option, 'error': error}
    '''

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
    radius = radius.subs(
        [(r, r_in), (R, R_in), (a, a_in), (b, b_in), (c, c_in)])

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
    q = Matrix([inter[0], inter[1], plane_z.subs(
        [(x, inter[0]), (y, inter[1])])])
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
