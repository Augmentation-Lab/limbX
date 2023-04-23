from gpiozero import MCP3008
import RPi.GPIO as GPIO
import time

# GLOBAL VARIABLES
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
		segment = 1
	elif s1_val == 1:
		segment = 0
	elif s2_val == 1: 
		segment = 2
	else:
		segment = 0
		
	return segment
	
def base_rotate():
	pass
	
def moving_limb(state, x_val, y_val, sel):
	pass

# This controls the magnet based on whether the button is pressed.
def magnet_on_off():
	if butt.value == 1.0:
		GPIO.output(magnetpin, True)
	else: 
		GPIO.output(magnetpin,False)
		
## EXECUTION + LOGIC ## 
try:
	while running:
		## Segment
		seg = switching_states() ## this sets the segment that we want to control. 
		
		## BASE
		base_val = potentionmeter.value
		# print(base_val)
		# base_rotate(base_val)
		
		## JOYSTICK 
		vx_val = vx.value
		vy_val = vy.value
		sel_val = sel.value	
		# moving_limb(seg, vx_val, vy_val, sel_val)
		
		# Controlling the Magnet
		magnet_on_off()
				
		
except KeyboardInterrupt(): # need this for GPIO control
	GPIO.output(magnetpin,False) 
	GPIO.cleanup()
GPIO.cleanup()
		
		
#print(s1.value, s2.value)
# print(vx.value, vy.value, sel.value, pot.value)		
pause()	         
