"""
CLIENT SCRIPT
receives data from /hmd/server (master)
"""

#!/usr/bin/env python3

from bluedot.btcomm import BluetoothClient
from datetime import datetime
from time import sleep
from signal import pause

import vision, driver

def data_received(data):
    print("recv - {}".format(data))

print("Connecting")
c = BluetoothClient("pi4", data_received)

print("Sending")
try:
    while True:
        c.send("hi {} \n".format(str(datetime.now())))
        sleep(1)
finally:
    c.disconnect()


# on signal received
# which side should we do object labeling on?
# targetObj = TargetObj(imgData=signal["imgData"], objLabel=signal["objLabel"])

targetObj = TargetObj(imgData=signal["imgData"])
targetObj.objLabel = vision.get_obj_label(targetObj)
targetObj.relPos = vision.get_rel_pos(targetObj)
driver.executeCommands([{"move": targetObj.relPos}])