#include <Servo.h>
Servo lrServo;
Servo udServo;

void setup() {
  // put your setup code here, to run once:
  while (!Serial) {
    Serial.begin(9600);
  }
  Serial.println("Initializing...");
  lrServo.attach(9);  // attaches the servo on pin 9 to the servo object
  udServo.attach(10);
  reset();
}

void reset() {
  lrServo.write(10);
  udServo.write(10);
}

void set_speed(String lr, float speed) {
  if (lr == "l") {
    lrServo.write(0);
  }
  if (lr == "r") {
    udServo.write(0);
  }
}

void loop()
{
//  Serial.println("test");
//  if (Serial.available() > 0)
//  {
//    String input = "";
//    input = Serial.readString();
//    if (input == "a")
//    {
//      Serial.println("left");
//      lrServo.write(90);
//    }
//    else if (input == "d")
//    {
//      Serial.println("right");
//      lrServo.write(-90);
//    }
//    else if (input == "w")
//    {
//      Serial.println("up");
//      udServo.write(90);
//    }
//    else if (input == "s")
//    {
//      Serial.println("down");
//      udServo.write(-90);
//    }
//    
//  }

//    String input = Serial.readString();
//    Serial.println(input);
  while(Serial.available())  
  {  
//    Serial.println("serial available");

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

  delay(1);
}
//https://forum.arduino.cc/t/controlling-direction-of-continuous-servos-over-serial/65345/6
