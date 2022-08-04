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
int INCREMENT = 5;
// how long a frame is in milliseconds
float WAIT_AFTER_INCREMENT = 75;

// which servo group is active (i.e. the first set of servos, the second set, etc.)
int activeServoGroup = 0;
int servos[2][2] = {{5,6}, {9,10}};

void setup() {
  Serial.begin(9600); 
  
  pinMode(VRx, INPUT);
  pinMode(VRy, INPUT);
  pinMode(SW, INPUT_PULLUP); 

  Serial.println("Initializing...");
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
  return clicked;
}


void reset() {
  Serial.println("Resetting"); 
  moveTo("lr", defPos[activeServoGroup][0]);
  moveTo("ud", defPos[activeServoGroup][1]);
}

bool pass(){
  return true;
}

float getServoPos(char servoPair[]){
  if(servoPair == "lr"){
    return absPos[activeServoGroup][0];
  } else if(servoPair == "ud"){
    return absPos[activeServoGroup][1];
  }
}

void setServoPos(char servoPair[], float deg){
  if(servoPair == "lr"){
    absPos[activeServoGroup][0] = deg;
  } else if(servoPair == "ud"){
    absPos[activeServoGroup][1] = deg;
  }
}


void moveTo(char servoPair[], float deg){
  if(servoPair == "lr"){
    lrServo.write(deg);
    absPos[activeServoGroup][0] = deg;
  } else if(servoPair == "ud") {
    udServo.write(deg);
    absPos[activeServoGroup][1] = deg;
  }
  delay(servoWait);
}

void moveDir(char servoPair[], char dir[]){
  Servo servo;
  float currPos;
  if(servoPair == "lr"){
    servo = lrServo;
    currPos = getServoPos("lr");
  } else if(servoPair == "ud"){
    servo = udServo;
    currPos = getServoPos("ud");
  }
  if(dir == "clockwise"){
    float newLocation = max(currPos - INCREMENT, 0);
  } else if (dir == "counterclockwise") {
    float newLocation = min(currPos + INCREMENT, 270);
  }
  servo.write(newLocation);
  setServoPos(servoPair, newLocation);
  delay(WAIT_AFTER_INCREMENT);
}

void loop() {
  float xPosition = getJoystickX();
  float yPosition = getJoystickX();
  bool SW_state = getJoystickClicked();
  if(joystickToggle){
    activeServoGroup = 0;
  } else {
    activeServoGroup = 1;
  }

  if(SW_state && (lastFramePressed == 0)) {
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
  lastFramePressed = !SW_state;

  delay(100); 
}
