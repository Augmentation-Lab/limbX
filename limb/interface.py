"""
INTERFACE SCRIPT
human interface script that integrates wink, voice, and joystick commands
"""

import client, driver
from utilities import vision

while True:
    button_press = True # get button press state from hardware
    command_spoken = True
    # WINK
    if button_press:
        client.capture_photo()

    # VOICE
    if command_spoken:
        client.capture_photo()

    # JOYSTICK