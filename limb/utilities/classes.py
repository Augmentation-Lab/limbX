"""
CLASSES
defines global classes
"""


class Params():
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class TargetPos():
    def __init__(self, x=None, y=None, z=None):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"TargetPos(x={self.x}, y={self.y}, z={self.z})"


class GazePoint():
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y


class TargetObj():
    # likely removing objLabel as part of the vision mechanism
    def __init__(self, imgData=None, gazePoint=GazePoint(), objLabel=None, relPos=TargetPos(), **kwargs):
        self.imgData = imgData
        self.gazePoint = gazePoint
        self.objLabel = objLabel
        self.relPos = relPos
        self.__dict__.update(kwargs)


class SystemState():
    def __init__(self, **kwargs):
        self.servoDict = None
        # self.currentTarget = None
        # self.currentCtrlSeq = None
        self.initialized = False
        self.__dict__.update(kwargs)

    def check_initialized(self):
        if self.servoDict is None:
            print("System not initialized.")
            self.initialized = False
        else:
            print("System initialized.")
            self.initialized = True
        return self.initialized
