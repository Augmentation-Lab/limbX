import RPi.GPIO as GPIO
import subprocess
import time
import re
from string import *
import button

GPIO.setmode(GPIO.BOARD)
ledPin = 12
buttonPin = 16
GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# initialization
for i in range(10):
    GPIO.output(ledPin, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(ledPin, GPIO.LOW)
    time.sleep(0.1)

video_recording = False
livestreaming = False
while True:
    button_count = button.get_button_state()
    if button_count != None:
        print(button_count)
    else: pass
    
    if button_count == 1:
        if not video_recording and not livestreaming:
            # execute photo script
            print("Taking photo...")
            subprocess.Popen(['sh', 'take_photo.sh']) # stops checking button state if take too long to upload photo
            print("Photo taken.")
        elif video_recording:
            print("Stopping video...")
#             subprocess.call(['pkill', 'raspivid'])
            subprocess.call(['sudo', 'sh', 'pkill.sh']) # maybe replace with individual commands if doesn't work on boot
            out = proc.communicate()[0]
            print("out", out, type(out))
            filename = re.sub("\D", "", out.decode('utf-8'))
            print("filename", filename)
            subprocess.call(['sh', 'stop_video.sh', filename])
            print("Video stopped.")
            video_recording = False
        elif livestreaming:
            print("Stopping livestream...")
#             subprocess.call(['sudo', 'sh', 'pkill.sh'])
#             subprocess.call(['pkill', 'raspivid'])
            subprocess.call(['sudo', 'sh', 'stop_livestream.sh'])
            print("Livestream stopped.")
            video_recording = False
    elif button_count == 2:
        # execute video script
        print("Starting video...")
        proc = subprocess.Popen(['sh', 'take_video.sh'], stdout=subprocess.PIPE)
        print("Video started...")
        video_recording = True
    elif button_count == 3:
        # execute livesream
        print("Starting livestream...")
        livestreaming = True
        subprocess.Popen(['sh', 'take_livestream.sh'])
        print("Livestream started...")
        
