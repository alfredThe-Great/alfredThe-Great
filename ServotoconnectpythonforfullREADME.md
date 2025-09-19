#include <Servo.h>

Servo myservo;  
int pos = 90;  // start at center

void setup() {
  Serial.begin(9600);   // Serial communication with Python
  myservo.attach(9);    // Servo signal wire on pin D9
  myservo.write(pos);   // initialize servo at center
}

void loop() {
  if (Serial.available() > 0) {
    int val = Serial.parseInt();   // read number from Python
    if (val >= 0 && val <= 180) {  // valid servo range
      pos = val;
      myservo.write(pos);
    }

    // clear extra bytes
    while (Serial.available() > 0) {
      Serial.read();
    }
  }
}
