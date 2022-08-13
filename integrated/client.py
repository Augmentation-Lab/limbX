"""
CLIENT SCRIPT
receives data from Tobii glasses
"""

import cv2
import av
from tobiiglassesctrl import TobiiGlassesController
import time
from datetime import datetime

def initialize(tobiiglasses):
    tobiiglasses.start_streaming()
    print("Please wait ...")
    time.sleep(1.0)

def capture_photo(tobiiglasses, ipv4_address):
    broken = False
    video = av.open("rtsp://%s:8554/live/scene" % ipv4_address, "r")
    for packet in video.demux():
        for frame in packet.decode():
            if isinstance(frame,av.video.frame.VideoFrame):
                #print(frame.pts)
                img = frame.to_ndarray(format='bgr24')
                img_wgaze = frame.to_ndarray(format='bgr24')
                height, width = img.shape[:2]
                data_gp  = tobiiglasses.get_data()['gp']
                if data_gp['ts'] > 0:
                    cv2.circle(img_wgaze,(int(data_gp['gp'][0]*width),int(data_gp['gp'][1]*height)), 60, (0,0,255), 6)
                    # cv2.imshow('Tobii Pro Glasses 2 - Live Scene',img)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    # imgFolderPath = f"data/{timestamp}"
                    # temporary
                    imgFolderPath = f"data/test"
                    cv2.imwrite(f"{imgFolderPath}/target.png", img)
                    cv2.imwrite(f"{imgFolderPath}/target_wgaze.png", img_wgaze)
                    print(f"Saved {imgFolderPath}/target.png and stopped streaming.")
                    broken = True
                    break
            if broken:
                break
        if broken:
            break

    return imgFolderPath, data_gp