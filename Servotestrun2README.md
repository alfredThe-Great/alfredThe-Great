#include <Servo.h>
Servo servo;

void setup() {
  Serial.begin(9600);
  servo.attach(9);
  servo.write(90);  // stop at start
}

void loop() {
  if (Serial.available()) {
    int value = Serial.parseInt(); // read value from python
    if (value >= 0 && value <= 180) {
      servo.write(value);
      Serial.print("Set speed: ");
      Serial.println(value);
    }
  }
}
