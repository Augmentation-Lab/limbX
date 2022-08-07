"""
CLIENT SCRIPT
receives data from Tobii glasses
"""

import cv2
import av
from tobiiglassesctrl import TobiiGlassesController
import driver, vision
from utilities.classes import TargetObj

def capture_photo():

    ipv4_address = "192.168.71.50"

    tobiiglasses = TobiiGlassesController(ipv4_address)
    video = av.open("rtsp://%s:8554/live/scene" % ipv4_address, "r")

    tobiiglasses.start_streaming()
    broken = False
    for packet in video.demux():
        for frame in packet.decode():
            if isinstance(frame,av.video.frame.VideoFrame):
                #print(frame.pts)
                img = frame.to_ndarray(format='bgr24')
                height, width = img.shape[:2]
                data_gp  = tobiiglasses.get_data()['gp']
                if data_gp['ts'] > 0:
                    cv2.circle(img,(int(data_gp['gp'][0]*width),int(data_gp['gp'][1]*height)), 60, (0,0,255), 6)
                    # cv2.imshow('Tobii Pro Glasses 2 - Live Scene',img)
                    cv2.imwrite("snapshot.jpg", img)
                    print("Saved snapshot.jpg and stopped streaming.")
                    begin_command()
                    broken = True
                    break
            if broken:
                break
        if broken:
            break

    # cv2.destroyAllWindows()

    tobiiglasses.stop_streaming()
    tobiiglasses.close()

def begin_command():
    """
    commands in the form:
    [{"grab": targetObj}]
    [{"release": targetObj}]
    [{"move": targetRelPos}, {"release": TargetObj}]
    [{"move": targetRelPos}, {"grab": TargetObj}]
    """
    targetObj = TargetObj(imgData="snapshot.jpg") # actually just imgPath
    targetObj.objLabel = vision.get_obj_label(targetObj)
    targetObj.relPos = vision.get_rel_pos(targetObj)
    driver.executeCommands([{"move": targetObj.relPos}])