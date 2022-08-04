# limbX

### Open Questions
- Currently all state information is stored in classes.py and passed down via mmain.py- should we use globals instead?
- Easy / automatic way to trigger release signal (e.g. grabbing coffee cup out of tentacle claw)
- Should grab and release have targetObj data inputs to help optimize process?


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

### Limb Components
onRPiStart - run Python GPIO script (main.py)

#### Scripts
main.py
objrec.py
classes.py
client.py
driver.py
ml.py
cainectrl.py

### HMD Components
onRPiStart - run Python script (main.py)

##### Scripts
main.py
objrec.py
classes.py
client.py
driver.py
ml.py
cainectrl.py
