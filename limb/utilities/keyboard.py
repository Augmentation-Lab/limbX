from . import servo
from . import hand
import yaml
from time import sleep
with open("limb/config.yml") as f:
    calibrationConfig = yaml.safe_load(f)['calibrationDict']


def controlWithKeyboard(systemSTATE):
    while True:
        command = input("Ardayf.io $ ")
        if command == "exit":
            break
        elif command == "grab":
            hand.release()
        elif command == "release":
            hand.release()
        elif command == "shimmy":
            servo.batchSetAngles(systemSTATE.servoDict, {0: {
                "central": 135
            }, 1: {
                "lr": 135,
                "ud": 135
            }, 2: {
                "lr": 135,
                "ud": 135
            }})
            sleep(5)
            servo.batchSetAngles(systemSTATE.servoDict, {0: {
                "central": 135
            }, 1: {
                "lr": 90,
                "ud": 90
            }, 2: {
                "lr": 90,
                "ud": 90
            }})
            sleep(5)
            servo.batchSetAngles(systemSTATE.servoDict, {0: {
                "central": 135
            }, 1: {
                "lr": 135,
                "ud": 135
            }, 2: {
                "lr": 135,
                "ud": 135
            }})
            sleep(5)
            servo.batchSetAngles(systemSTATE.servoDict, {0: {
                "central": 135
            }, 1: {
                "lr": 180,
                "ud": 180
            }, 2: {
                "lr": 180,
                "ud": 180
            }})
        elif len(command) == 0:
            continue
        elif command == "help":
            print("""Exmaple command:
1 45 45 corresponds to move the first segment to 45 degrees in the lr direction and 45 degrees in the ud direction
central 30 corresponds to move the central servo to 30 degrees)""")
            continue
        # check if the command consists entirely of special characters
        try:
            command = command.split(" ")
            segment = command[0]
            if segment == "central":
                angle = float(command[1])
                servo.batchSetAngles(systemSTATE.servoDict, {calibrationConfig['central']['servoIdx']: {
                    "central": angle
                }})
            else:
                servoLR = float(command[1])
                servoUD = float(command[2])
                servo.batchSetAngles(systemSTATE.servoDict, {calibrationConfig['seg' + segment]["servoIdx"]: {
                    "lr": servoLR, "ud": servoUD}})
        except Exception as e:
            print(f"Invalid command: {e}")
