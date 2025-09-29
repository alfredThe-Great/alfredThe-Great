#include <Servo.h>

Servo myServo;

void setup() {
  myServo.attach(9); // Connect servo signal pin to D9
  myServo.write(90); // Stop servo at start
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    char command = Serial.read();

    if (command == 'L') {
      myServo.write(70);  // Rotate left (lower = faster)
    } 
    else if (command == 'R') {
      myServo.write(110); // Rotate right (higher = faster)
    } 
    else if (command == 'S') {
      myServo.write(90);  // Stop
    }
  }
}
