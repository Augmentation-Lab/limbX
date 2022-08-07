#include <Servo.h>
Servo lrServo;
Servo udServo;

// Joystick pins
int VRx = A0;
int VRy = A1;
int SW = 2;

// initial joystick values
int xPosition = 0;
int yPosition = 0;
int SW_state = 0;
int mapX = 0;
int mapY = 0;

// whether the joystick starts in 0 mode or 1 mode (determines which sdet of pins to start on)
bool joystickToggle = false;
// basically means that the user starts with the joystick at a default, non-zero state
int lastFramePressed = 2;
// How long to wait after a moveTo()
float servoWait = 800;

// what is the mid point of the servo (also where to start the servos at)
int defPos[2][2] = {{135, 135}, {135, 135}};
// this tracks the absolute position of the servos denoted in the servos array
// this should go [lr, ud]
float absPos[2][2];

// how many degrees to change the degree in moveDir frame
int INCREMENT = 20;
// how long a frame is in milliseconds
float WAIT_AFTER_INCREMENT = 100;

// which servo group is active (i.e. the first set of servos, the second set, etc.)
int activeServoGroup = 0;
int servos[2][2] = {{5,6}, {9,10}};

void setup() {
  Serial.begin(9600); 
  
  pinMode(VRx, INPUT);
  pinMode(VRy, INPUT);
  pinMode(SW, INPUT_PULLUP); 

  Serial.println("Initializing...");
  lrServo.attach(servos[activeServoGroup][0]);
  udServo.attach(servos[activeServoGroup][1]);
  reset();
}

float getJoystickX() {
  float xPosition = analogRead(VRx);
  float mapX = map(xPosition, 0, 1023, -512, 512);
  return mapX;
}

float getJoystickY() {
  float yPosition = analogRead(VRy);
  float mapY = map(yPosition, 0, 1023, -512, 512);
  return mapY;
}

bool getJoystickClicked() {
  bool clicked = digitalRead(SW);
  return !clicked;
}


void reset() {
  Serial.println("Resetting");
  activeServoGroup = 0;
  moveTo("lr", defPos[0][0]);
  moveTo("ud", defPos[0][1]);
  activeServoGroup = 1;
  moveTo("lr", defPos[1][0]);
  moveTo("ud", defPos[1][1]);

  activeServoGroup = 0;
}

bool pass(){
  return true;
}

float getServoPos(String servoPair){
  if(servoPair == "lr"){
    return absPos[activeServoGroup][0];
  } else if(servoPair == "ud"){
    return absPos[activeServoGroup][1];
  }
}

void setServoPos(String servoPair, float deg){
  Serial.println(servoPair);
  Serial.println(deg);
  if(servoPair == "lr"){
    absPos[activeServoGroup][0] = deg;
  } else if(servoPair == "ud"){
    absPos[activeServoGroup][1] = deg;
  }
}


void moveTo(String servoPair, float deg){
  if(servoPair == "lr"){
    lrServo.write(deg);
  } else if(servoPair == "ud") {
    udServo.write(deg);
  }
  setServoPos(servoPair, deg);
  delay(servoWait);
}

void moveDir(String servoPair, String dir){
  Servo servo;
  float currPos;
  if(servoPair == "lr"){
    servo = lrServo;
    currPos = getServoPos("lr");
  } else if(servoPair == "ud"){
    servo = udServo;
    currPos = getServoPos("ud");
  }
  int newLocation;
  if(dir == "clockwise"){
    newLocation = max(currPos - INCREMENT, 0);
  } else if (dir == "counterclockwise") {
    newLocation = min(currPos + INCREMENT, 270);
  }
  servo.write(newLocation);
  setServoPos(servoPair, newLocation);

  delay(WAIT_AFTER_INCREMENT);
}

void loop() {
  float xPosition = getJoystickX();
  float yPosition = getJoystickY();

  bool joystickIsPressed = getJoystickClicked();
  if(!joystickToggle){
    activeServoGroup = 0;
  } else {
    activeServoGroup = 1;
  }

  lrServo.attach(servos[activeServoGroup][0]);
  udServo.attach(servos[activeServoGroup][1]);

  if(!joystickIsPressed && (lastFramePressed == 1)) {
    joystickToggle = !joystickToggle;
  }
  else if(xPosition > 256){
    // NOTE THAT THIS IS NON-BLOCKING. YOU MUST DELAY UNTIL IT IS ABLE TO COMPLETE ITS ROTATION... SO AMYBE A GOOD 2 SECONDS
    moveDir("lr", "clockwise");
  } else if(xPosition < -256){
    moveDir("lr", "counterclockwise");
  } else if(yPosition > 256){
    moveDir("ud", "clockwise");
  } else if(yPosition < -256){
    moveDir("ud", "counterclockwise");
  } else {
    pass();
  }
  lastFramePressed = joystickIsPressed;

  delay(100); 
}
