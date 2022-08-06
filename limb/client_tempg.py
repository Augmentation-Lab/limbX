import av
import cv2
import numpy as np
from tobiiglassesctrl import TobiiGlassesController
import matplotlib.pyplot as plt

# ipv4_address = "192.168.100.10"
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
                print("stopped")
                broken = True
                break
        if broken:
            break
    if broken:
        break

cv2.destroyAllWindows()

tobiiglasses.stop_streaming()
tobiiglasses.close()
