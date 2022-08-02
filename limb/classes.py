class Params():
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class SystemState():
    def __init__(self, **kwargs):
        self.handPosition = {'x': 0, 'y': 0, 'z': 0}
        self.currentTarget = None
        self.currentCtrlSeq = None
        self.__dict__.update(kwargs)