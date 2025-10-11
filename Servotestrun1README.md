#include <Servo.h>

Servo servo;
int pos = 90; // Start centered

void setup() {
  Serial.begin(9600);
  servo.attach(9);  // servo signal pin
  servo.write(pos);
}

void loop() {
  if (Serial.available()) {
    int angle = Serial.parseInt(); // read the incoming angle
    if (angle >= 0 && angle <= 180) {
      servo.write(angle);
      delay(15); // small delay for servo movement
    }
  }
}
