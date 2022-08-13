"""
INTERFACE SCRIPT
human interface script that integrates wink, voice, and joystick commands
"""

import keyboard

import client, vision #, driver
from utilities.classes import TargetObj
import time
from tobiiglassesctrl import TobiiGlassesController
from utilities import tcamera

ipv4_address = "192.168.71.50"
tobiiglasses = TobiiGlassesController(ipv4_address)

client.initialize(tobiiglasses)

# def begin_command(imgFolderPath):
#     """
#     commands in the form:
#     [{"grab": targetObj}]
#     [{"release": targetObj}]
#     [{"move": targetRelPos}, {"release": TargetObj}]
#     [{"move": targetRelPos}, {"grab": TargetObj}]
#     """
#     targetObj = TargetObj(imgData="snapshot.jpg") # actually just imgPath
#     # targetObj.objLabel = vision.get_obj_label(targetObj)
#     # espeak.synth("Object identified: " + targetObj.objLabel)
#     # temporary pre depth camera
#     vision.run_vision(f"{imgFolderPath}/query.png", f"{imgFolderPath}/target.png", eyeGaze)

lastLeftData = None
lastRightData = None
winkStatus = None
eyeDataHistory = {"left": [], "right": []}

def runInterface(): 

    while True:

        # button_press = True # get button press state from hardware
        # command_spoken = True

        leftData = str(tobiiglasses.get_data()['left_eye'])
        rightData = str(tobiiglasses.get_data()['right_eye'])
        eyeDataHistory["left"].append(leftData)
        eyeDataHistory["right"].append(rightData)
        # capture gaze data
        gazePosition = tobiiglasses.get_data()['gp']
        
        if len(eyeDataHistory["left"]) > 3:
            eyeDataHistory["left"].pop(0)
            eyeDataHistory["right"].pop(0)

            print("set: ", set(eyeDataHistory["right"]))
            print("len: ", len(set(eyeDataHistory["right"])))
            if len(set(eyeDataHistory["right"])) == 1:
                # print("right set 1")
                if len(set(eyeDataHistory["left"])) > 1:
                    # print("right set > 1")
                    winkStatus = "rightWink"
            if len(set(eyeDataHistory["left"])) == 1:
                # print("left set 1")
                if len(set(eyeDataHistory["right"])) > 1:
                    # print("right set > 1")
                    winkStatus = "leftWink"

            # WINK
            if winkStatus == "rightWink":
                print("RIGHT WINK RECOGNIZED")
                imgFolderPath, eyeData = client.capturePhoto(tobiiglasses, ipv4_address)
                # rpi capture photo
                tcamera.capturePhoto()
                # targetObj = TargetObj(imgData="snapshot.jpg") # actually just imgPath
                queryTargetcenter = vision.run_vision(f"{imgFolderPath}/query.png", f"{imgFolderPath}/target.png", eyeData)
                # implement controls
                winkStatus = None

                return queryTargetcenter
                
                time.sleep(10)

            time.sleep(0.5)

        # if keyboard.is_pressed('q'):
        #     tobiiglasses.stop_streaming()
        #     tobiiglasses.close()


        # # VOICE
        # if command_spoken:
        #     client.capture_photo()

        # # JOYSTICK
        