"""
SMART SCRIPT
calculates control sequences
"""

def calculateTargetAngles(servoDict, targetRelPos):
    """
    relativeObjPos in the form:
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
    """
    servoAngles = {
        segment : {
            axis : servoDict[segment][axis].currentAngle for axis in servoDict[segment].keys()
        } for segment in servoDict.keys()
    }
    """
    targetAngles in the form:
    {
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
    return targetAngles
    