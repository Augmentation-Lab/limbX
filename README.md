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
2. Segment object of interest using eye gaze & image. Label object.
3. Tentacle collects images of environment at different angles.
4. When SIFT produces a match, find the x,y,z position of the center of the object.
5. Trigger control system to calculate and execute control sequence given targetRelPos.

### Smart Algorithm
```
INPUTS
servoDict = {
    1: {
        "lr": Servo(name="1_lr", pin=1),
        "ud": Servo(name="1_ud", pin=2)
    },
    2: {
        "lr": Servo(name="2_lr", pin=3),
        "ud": Servo(name="2_ud", pin=4)
    },
    3: {
        "lr": Servo(name="3_lr", pin=5),
        "ud": Servo(name="3_ud", pin=6)
    }
}
relativeObjPos = TargetPos(x=10,y=20,z=5)
```
```
OUTPUTS
servoTargetAngles = {
    1: {
        "lr": -10,
        "ud": 15
    },
    2: {
        "lr": 20,
        "ud": 25
    },
    3: {
        "lr": 15,
        "ud": 90
    }
}
```