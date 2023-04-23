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
        elif len(command) == 0:
            continue
        elif command == "grab":
            hand.release()
        elif command == "release":
            hand.release()
        elif command == "straight":
            servo.setAllAngles(systemSTATE.servoDict, 135)
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
            sleep(2)
            servo.batchSetAngles(systemSTATE.servoDict, {0: {
                "central": 70
            }, 1: {
                "lr": 90,
                "ud": 90
            }, 2: {
                "lr": 90,
                "ud": 90
            }})
            sleep(2)
            servo.batchSetAngles(systemSTATE.servoDict, {0: {
                "central": 200
            }, 1: {
                "lr": 135,
                "ud": 135
            }, 2: {
                "lr": 135,
                "ud": 135
            }})
            sleep(2)
            servo.batchSetAngles(systemSTATE.servoDict, {0: {
                "central": 135
            }, 1: {
                "lr": 180,
                "ud": 180
            }, 2: {
                "lr": 180,
                "ud": 180
            }})
        elif command == "help":
            print("""Exmaple command:
$ 1 lr 50
    move the first segment to 45 degrees in the lr direction
$ 0 central 90
    move the central servo to 30 degrees
$ grab
$ release
$ shimmy
$ straight""")
            continue
        else:
            # check if the command consists entirely of special characters
            try:
                command = command.split(" ")
                segment = int(command[0])
                servoName = command[1]
                angle = float(command[2])
                servo.batchSetAngles(systemSTATE.servoDict, {segment: {
                    servoName: angle
                }})
            except Exception as e:
                print(f"Invalid command: {e}")
