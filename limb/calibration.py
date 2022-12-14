
from utilities import servo
from time import sleep
from collections import defaultdict
import yaml
import pyperclip
import utilities.servoDict as servoDictFunc
from utilities.keyboard import controlWithKeyboard
with open("limb/config.yml") as f:
    calibrationConfig = yaml.safe_load(f)['calibrationDict']
with open("limb/calibration.yml") as f:
    calibrationData = yaml.safe_load(f)
systemSTATE = servoDictFunc.initialize()

"""
CALIBRATION.YML
central:
    bl/br/tl/tr: The servo angles for the 4 quadrants of the central servo.
    The smart algorithm relies on the "45-degreeness" of all these values, in that it can assume that, for example,
    the tip of segment 1 at quadrant TR is the negative of the tip of segment 1 at quadrant BL
seg1:
    the position of the tip of the first stage relative to the central servo when the servo is at a preset bend amount
    The first stage only operates at 4 distinct angles.
    As such, in our callibration, we just "tense" the tentaclea fixed amount and rotate it around the central servo.
    lr and ud represent the initial "tensed" values of the servos
    x, y, and z represent the distance (in meters) from the central servo to the tip of the first stage
seg2:
    [(servoAngle of servo lr, servoAngle of servo ud), (actual angle alpha achieved by tentacle, actual angle beta achieved by tentacle)]
    When we calibrate seg2, we put it in the top right default position and then measure the angles of the servos
    MAJOR PROBLEM as the servo angles for seg2 in the top right position will almost certainly be different than those
    when the top left, bottom right, and bottom left positions. The options here are to have another 3 set of calibrations for the other
    3 base positions, or to od some complex math to figure this out. However, I don't quite know if this is true.... maybe rotating the central servo around
    does not actually change the angles
seg3:
    servoActualAngle consists of 3 ordered pairs
    The first pair is the servo angle for the second segment
    The second pair is the servo angle for the third segment
    The third pair is the actual angle the third segment is at
    The structure used for the first pair of angles is the same as thast in seg2
    The structure used for the second pair of angles is the same as thast in seg2,
"""


"""
How Calibration Should Work:
1. The central servo spins around and you stop it when it's real angle is
-45 degrees, 45 degrees, 135 degrees, and 225 degrees from horizontal (270 degrees total), where angle 0 is at the negative x-axis and we start clockwise

2. The first segment crunches until you tell it to stop. This is quadrant independent. This is the "curnch"
of the first segment throughout all quadrants (i.e. it has this "crunch" at -45, 45, 135, and 225 degrees)

3. Spin the central servo to the tr quadrant. Note that the specific quadrant chosen is actually irrelevant
This is because, the tip of the first segment is of equal distance ot the central servo at -45, 45, 135, and 225 degrees
Prompt the user to collect the vector from the the base to the end of the first segment

4. Move the tip of segment 1 to quadrant tr.

Allow the calibrator to move the tip of segment 2 freely until it
reaches the following checkpoints w.r.t. the (alpha, beta) angles (in the real world):
(45, 0)
(90, 0)
(0, 45)
(0, 90)
(45, 45)
These values depend on what values are possible to achieve by the tentacle.
They do not have to be perfect 45-degree angles
They merely need to be measurable angle values of the tip of the second segment.

5. Repeat step 4 for all 4 quadrants

"""

new_calibration = {}

"""
STEP #1
"""
print("Calibration Step #1")
print("We will now begin calibrating the central servo to find the angles at which it achieves -45, 45, 135, and 225 degrees")

# Spin the centrla servo between the min and max angle
centralConfig = calibrationConfig['central']
# The list of 4 servo angles at which we want our central servo to be at
quadrants = {'br': 0, 'tr': 0, 'tl': 0, 'bl': 0}
associated_angle = {'br': -45, 'tr': 45, 'tl': 135, 'bl': 225}
quad_keys = list(quadrants.keys())
confirm_no = 0
'''
for testAngle in range(centralConfig['minAngle'], centralConfig['maxAngle'] + 1, centralConfig['angleInterval']):
    servo.batchSetAngles(systemSTATE.servoDict, {centralConfig['servoIdx']: {
        "central": testAngle
    }})
    currentQuad = quad_keys[confirm_no]
    confirm = input(
        f"Current servo angle is {testAngle}. Does this achieve an angle of {associated_angle[currentQuad]} from horizontal (quadrant {currentQuad})? (y/n): ")
    if confirm in ["y", "Y"]:
        quadrants[quad_keys[confirm_no]] = testAngle
        confirm_no += 1
    if confirm_no == 4:
        break

if(confirm_no != 4):
    assert False
'''

new_calibration['central'] = quadrants
print("---- calibration.yml ----")
print(new_calibration)

"""
STEP #2 and #3
"""
print("Calibration Steps #2 and #3")
print("We will now begin measuring the 'crunch' in the first segment. We will then measure the tip position")


seg1Config = calibrationConfig['seg1']
confirm = input(
    f"Move the lr/ud servo angles until the tip of segment 1 is in a satisfactory position (likely able to reach most objects)? . Press enter to continue: ")
controlWithKeyboard(systemSTATE)
testAngles = input(
    f"At what angle measures was this achieved? (e.g. 1 3)")
measures = input(
    f"What is the vector (in meters) from the base of the central servo to the tip of segment 1? (e.g. 1 3 1)")

new_calibration['seg1'] = {}
new_calibration['seg1']['x'] = int(measures.split(" ")[0])
new_calibration['seg1']['y'] = int(measures.split(" ")[1])
new_calibration['seg1']['z'] = int(measures.split(" ")[2])

new_calibration['seg1']['preset'] = {
    "lr": testAngles.split(" ")[0], "ud": testAngles.split(" ")[1]}

print("---- calibration.yml ----")
print(new_calibration)

"""
Step #4
"""
print("Calibration Step #4")
print("We will now begin measuring the angles of the second segment")


seg2Config = calibrationConfig['seg2']
# All the possible real world angles we want to test for
targetAngles = [(45, 0), (90, 0), (0, 45), (0, 90), (45, 45)]
servoAnglesDir = {'tr': {}, 'bl': {}, 'tl': {}, 'br': {}}
for quadrant in servoAnglesDir.keys():
    count = 0
    for anglePair in targetAngles:
        try:
            confirm = input(
                f"Move the tip of segment 2 until it reaches the following angle pair: (alpha={anglePair[0]}, beta={anglePair[1]}). Press enter to continue: ")

            # Sandbox to allow the user to move about
            controlWithKeyboard(systemSTATE)
            servoAngles = input(
                f"What angle pair for the servo would you like for target angles (alpha={anglePair[0]}, beta={anglePair[1]})? (e.g. '45 30'): ")
            servoAngles = [servoAngles.split(
                ' ')[0], servoAngles.split(' ')[1]]
            # servoAngles: the servo angle they end at once they have moved the tip of segment 2 to the satisfactory position
            servoAnglesDict = [
                servoAngles, [anglePair[0], anglePair[1]]]
            servoAnglesDir[quadrant][count] = servoAnglesDict
            count += 1
            print(
                f"Calibration for target angles (alpha={anglePair[0]}, beta={anglePair[1]}) is now associated with servo angles ({servoAngles[0]}, {servoAngles[1]})")
        except Exception as e:
            print(f"Invalid command: {e}")

new_calibration['seg2'] = servoAnglesDir
print("---- calibration.yml ----")
print(new_calibration)
pyperclip.copy(str(new_calibration))
servo.shutdown(systemSTATE.servoDict)
