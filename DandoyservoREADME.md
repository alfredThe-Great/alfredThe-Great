/*
  Smart Trash Can with Ultrasonic Sensor and Servo
  Fixed version with debug output
*/

#include <Servo.h>

// Servo setup
Servo servo;
const int servoPin = 9;
const int openAngle = 0;
const int closeAngle = 90;

// Ultrasonic sensor setup
const int trigPin = 5;
const int echoPin = 6;
long distance, averageDistance;
long averDist[3];

// Distance threshold (cm)
const int distanceThreshold = 20;

void setup() {
  Serial.begin(9600);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  servo.attach(servoPin);
  servo.write(closeAngle);
  delay(100); // let the sensor stabilize
}

void loop() {
  // Measure 3 times
  for (int i = 0; i < 3; i++) {
    distance = readDistance();
    averDist[i] = distance;
    delay(10);
  }

  // Average distance
  averageDistance = (averDist[0] + averDist[1] + averDist[2]) / 3;
  Serial.print("Average Distance: ");
  Serial.println(averageDistance);

  // Servo control
  if (averageDistance <= distanceThreshold) {
    servo.write(openAngle);
    delay(1500);
  } else {
    servo.write(closeAngle);
    delay(500);
  }
}

// Function to read ultrasonic distance
float readDistance() {
  // Trigger pulse
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Measure echo with timeout (30ms = ~5m max)
  long duration = pulseIn(echoPin, HIGH, 30000);

  Serial.print("Duration: ");
  Serial.println(duration);

  if (duration == 0) {
    return 999; // no object detected (out of range)
  }

  float distance = duration / 58.0; // convert to cm
  return distance;
}
