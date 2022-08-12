# limbX

### Directory Structure
```
limbX
├── README.md
├── demo.py - demonstrates limb functionality
├── archived (hidden) - archived scripts
├── data - stores camera data from hmd RPi
└── limb
    ├── config.yml - config file with hardware specifications
    ├── driver.py - executes high-level control commands
    ├── classes.py - defines global classes
    ├── client.py - receives data from Tobii
    ├── hand.py - controls hand
    ├── servo.py - executes low level servo control
    ├── smart.py - calculates control sequences
    └── vision.py - uses ml to process camera data
```

### Open Questions
- Currently all state information is stored in classes.py and passed down via mmain.py- should we use globals instead?
- Easy / automatic way to trigger release signal (e.g. grabbing coffee cup out of tentacle claw)
- Should grab and release have targetObj data inputs to help optimize process?

### Computer Vision
1. On command triggered from glasses: send image + eye gaze from Tobii to RPi.
2. Segment image into object regions.
3. Crop image to only include eye-tracked object without bg.
4. Tentacle collects images of environment at different angles.
For each image:
5. Use SIFT to map features from cropped image to tentacle image.
6. Segment tentacle image into object regions.
7. Select the object region containing the most mapped points if number of mapped points exceeds threshold.
8. Find the x,y,z position of the center of the selected object region.
9. Average these positions as hybrid data.
10. Trigger control system to calculate and execute control sequence given targetRelPos.


### Smart Algorithm
```
INPUTS
servoDict = {
    1: {
        "lr": Servo(name="1_lr", pin=1),
        "bf": Servo(name="1_bf", pin=2)
    },
    2: {
        "lr": Servo(name="2_lr", pin=3),
        "bf": Servo(name="2_bf", pin=4)
    },
    3: {
        "lr": Servo(name="3_lr", pin=5),
        "bf": Servo(name="3_bf", pin=6)
    }
}
relativeObjPos = TargetPos(x=10,y=20,z=5)
```
```
OUTPUTS
servoTargetAngles = {
    1: {
        "lr": -10,
        "bf": 15
    },
    2: {
        "lr": 20,
        "bf": 25
    },
    3: {
        "lr": 15,
        "bf": 90
    }
}
```