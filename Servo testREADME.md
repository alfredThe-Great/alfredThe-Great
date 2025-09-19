#include <Servo.h>
Servo servo;

void setup() {
  servo.attach(9);   // Servo signal pin on D9
}

void loop() {
  // Sweep from 0 to 180
  for (int pos = 0; pos <= 180; pos += 10) {
    servo.write(pos);
    delay(500);
  }
  // Sweep back to 0
  for (int pos = 180; pos >= 0; pos -= 10) {
    servo.write(pos);
    delay(500);
  }
}
