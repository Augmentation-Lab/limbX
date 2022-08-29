from .classes import SystemState
from .servo import initialize as servoInitialize
import yaml


def initialize():
    with open("./limb/config.yml") as f:
        configData = yaml.safe_load(f)

    systemSTATE = SystemState()
    # get config from config.yml
    servoPins = configData["servoPins"]
    systemSTATE.servoDict = servoInitialize(servoPins)
    if systemSTATE.check_initialized() is False:
        raise Exception("System not initialized.")
    return systemSTATE
