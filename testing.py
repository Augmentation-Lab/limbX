from limb import driver
from limb.utilities import servo
from time import sleep

driver.initialize()

batchAngles11 = {
    1: {
        "lr": 90,
        "bf": 90
    }
}
batchAngles12 = {
    1: {
        "lr": 0,
        "bf": 0
    }
}
batchAngles21 = {
    2: {
        "lr": 90,
        "bf": 90
    }
}
batchAngles22 = {
    2: {
        "lr": 0,
        "bf": 0
    }
}

servo.batchSetAngles(driver.systemSTATE.servoDict, batchAngles11)
sleep(1)
servo.batchSetAngles(driver.systemSTATE.servoDict, batchAngles12)
sleep(1)
servo.setAllAngles(driver.systemSTATE.servoDict, 10)


driver.shutdown()