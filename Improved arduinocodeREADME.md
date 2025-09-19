#include <Servo.h>
Servo myservo;
int currentPos = 90;

void setup() {
  Serial.begin(9600);
  myservo.attach(9);
  myservo.write(currentPos);
}

void loop() {
  if (Serial.available() > 0) {
    int val = Serial.parseInt();
    if (val >= 0 && val <= 180 && val != currentPos) {  // only move if angle changed
      currentPos = val;
      myservo.write(currentPos);
    }
    while (Serial.available() > 0) Serial.read();
  }
}
