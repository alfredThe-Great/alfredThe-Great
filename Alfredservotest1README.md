#include <Servo.h>
Servo servo;

int pos = 90; // start at center
int stepSize = 2; // movement step

void setup() {
  Serial.begin(9600);
  servo.attach(9); // connect servo to pin 9
  servo.write(pos);
}

void loop() {
  if (Serial.available()) {
    char command = Serial.read();

    if (command == 'L') {  // move left
      pos -= stepSize;
      if (pos < 0) pos = 0;
      servo.write(pos);
    }
    else if (command == 'R') {  // move right
      pos += stepSize;
      if (pos > 180) pos = 180;
      servo.write(pos);
    }
  }
}
