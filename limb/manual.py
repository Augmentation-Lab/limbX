from gpiozero import MCP3008
import RPi.GPIO as GPIO
import time
import utilities.servoDict as servoDict
from utilities import servo
systemSTATE = servoDict.initialize()

# GLOBAL VARIABLES
# Largest joystick range produces this angle of movement
fullMove = 1
# General variables
segment = 0 #segment that you are controlling
running = True # for testing purposes
# magnet pins
magnetpin = 19
butt_pin = 6 # for magnet button
# controller pins
x_pin = 2
y_pin = 3
sel_pin = 1
# toggle pins
s1_pin = 4
s2_pin = 5

## INSTANTIATION OF ANALOG-TO-DIGITIAL DEVICES
potentionmeter = MCP3008(0)
vy = MCP3008(y_pin)
vx = MCP3008(x_pin)
sel = MCP3008(sel_pin)
# for the toggle states
s1 = MCP3008(s1_pin)
s2 = MCP3008(s2_pin)	
# Magnetbutton
butt = MCP3008(butt_pin) # If Button connected to positive terminal, if pressed it is 1, otherwise, 0
# setting up GPIO pins (Magnet)
GPIO.setmode(GPIO.BCM)
GPIO.setup(magnetpin,GPIO.OUT)

## DEFINING FUNCTIONS ##
def switching_states(): # check this, not very precise! 
	# might be better to use ceiling and floor for threshold. round appears to be kind of unreliable at the moment
	s1_val = round(s1.value)
	s2_val = round(s2.value)
	if s1_val == 0 and s2_val == 0: 
		segment = 2
	elif s1_val == 1:
		segment = 1
	elif s2_val == 1: 
		segment = 3
	else:
		segment = 1
		
	return segment
	
def base_rotate(p_val):
	print("debug:", {0: {"central": p_val*360}})
	# servo.batchSetAngles(systemSTATE.servoDict, {0: {"central": (p_val*270)-135}})

def moving_limb(segment, x_val, y_val):
	x_movePerc = x_val - 0.5 if abs(x_val - 0.5) > 0.1 else 0
	y_movePerc = y_val - 0.5 if abs(y_val - 0.5) > 0.1 else 0
	if abs(x_movePerc + y_movePerc) > 0:
		angleChange = {"lr": x_movePerc*fullMove, "ud": y_movePerc*fullMove}
		print("angleChange:", angleChange)
		for axis in ["lr", "ud"]:
			print("dsjklfjds:", segment)
			print("debug:", {segment: {axis: float(systemSTATE.servoDict[segment][axis].currentAngle + angleChange[axis])}})
			servo.batchSetAngles(systemSTATE.servoDict, {segment: {axis: float(systemSTATE.servoDict[segment][axis].currentAngle + angleChange[axis])}})

# This controls the magnet based on whether the button is pressed.
def magnet_on_off():
	print("debug", butt.value)
	if butt.value == 1.0:
		GPIO.output(magnetpin, True)
	else: 
		GPIO.output(magnetpin,False)
		
## EXECUTION + LOGIC ## 
vx_val = 0
vy_val = 0
try:
	while running:
		## Segment
		seg = switching_states() ## this sets the segment that we want to control. 
		
		## Move base
		# if abs(potentiometer.value - base_val) > 0.1:
			# base_rotate(potentiometer.value)
			
		## POTENTIOMETER
		# base_val = potentionmeter.value
		
		# Move limb
		# print(vx.value)
		# if abs(vx.value - vx_val) + abs(vy.value - vy_val) > 0.1:
		moving_limb(seg, vx.value, vy.value)
		
		## JOYSTICK 
		vx_val = vx.value
		vy_val = vy.value
		sel_val = sel.value	
		
		# Controlling tehe Magnet
		#magnet_on_off()
		
		
except KeyboardInterrupt(): # need this for GPIO control
	GPIO.output(magnetpin,False) 
	GPIO.cleanup()
GPIO.cleanup()
		
		
#print(s1.value, s2.value)
# print(vx.value, vy.value, sel.value, pot.value)		
pause()	         
