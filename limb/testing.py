import driver
from utilities import servo
from time import sleep

driver.initialize()

batchAngles11 = {
    1: {
        "lr": 90,
        "ud": 90
    }
}
batchAngles12 = {
    1: {
        "lr": 0,
        "ud": 0
    }
}
batchAngles21 = {
    2: {
        "lr": 90,
        "ud": 90
    }
}
batchAngles22 = {
    2: {
        "lr": 0,
        "ud": 0
    }
}

# servo.testStart(driver.systemSTATE.servoDict)
servo.batchSetAngles(driver.systemSTATE.servoDict, batchAngles11)
sleep(1)
servo.batchSetAngles(driver.systemSTATE.servoDict, batchAngles12)
sleep(1)
servo.batchSetAngles(driver.systemSTATE.servoDict, batchAngles21)
sleep(1)
servo.batchSetAngles(driver.systemSTATE.servoDict, batchAngles22)