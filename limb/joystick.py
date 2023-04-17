import RPi.GPIO as GPIO
import time
from gpiozero import Button
GPIO.setmode(GPIO.BCM)
GPIO.setup(19,GPIO.OUT)
#GPIO.setup(15,GPIO.IN)

try:
	while True:
		#if GPIO.input(15):
		#	print("Pressed")
		GPIO.output(19, True)
		print("On")
		time.sleep(10)
		GPIO.output(19,False)
		print("Off")
		time.sleep(10)
# GPIO.output(26, False)
except KeyboardInterrupt():
	GPIO.cleanup()
