#include <Servo.h>
Servo lrServo;
Servo udServo;

int VRx = A0;
int VRy = A1;
int SW = 2;

int xPosition = 0;
int yPosition = 0;
int SW_state = 0;
int mapX = 0;
int mapY = 0;

bool joystick = true;
bool joystickToggle = false;
bool lastFrameClick = true;
float servoWait = 800;


int lrServo1 = 5;
int udServo1 = 6;

int lrServo2 = 9;
int udServo2  = 10;

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
  lrServo.write(100); // should be 135
  udServo.write(100); // should be 135
}

void loop() {
  float xPosition = getJoystickX();
  float yPosition = getJoystickX();
  bool SW_state = getJoystickClicked();
  if(joystickToggle){
    lrServo.attach(lrServo1);  // attaches the servo on pin 9 to the servo object
    udServo.attach(udServo1);
  } else {
    lrServo.attach(lrServo2);  // attaches the servo on pin 9 to the servo object
    udServo.attach(udServo2);
  }
  Serial.println(joystickToggle);
  if(joystick){    
    if(SW_state && !lastFrameClick) {
      joystickToggle = !joystickToggle;
    }
    else if(xPosition > 256){
      lrServo.write(270);// NOTE THAT THIS IS NON-BLOCKING. YOU MUST DELAY UNTIL IT IS ABLE TO COMPLETE ITS ROTATION... SO AMYBE A GOOD 2 SECONDS
      delay(servoWait);
    } else if(xPosition < -256){
      lrServo.write(0);
      delay(servoWait);
    } else if(yPosition > 256){
      udServo.write(0);
      delay(servoWait);
    } else if(yPosition < -256){
      udServo.write(270);
      delay(servoWait);
    } else {
      reset();
      //delay(servoWait);
    }
    
    lastFrameClick = SW_state;
    
  }

  else {
    String input = Serial.readString();
    Serial.println(input);
    if (input == "l")
    {
      Serial.println("left");
      lrServo.write(90);
    }
    else if (input == "r")
    {
      Serial.println("right");
      lrServo.write(-90);
    }
    else if (input == "u")
    {
      Serial.println("up");
      udServo.write(90);
    }
    else if (input == "d")
    {
      Serial.println("down");
      udServo.write(-90);
    }
  }

  delay(100); 
}