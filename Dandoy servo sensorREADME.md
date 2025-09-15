/*
  Smart Trash Can with Ultrasonic Sensor (HC-SR04) and Servo (SG90)
  - Opens lid when object is detected within 20 cm
  - Closes lid when no object is near
  - Filters out invalid / too far readings
*/

#include <Servo.h>

// Servo setup
Servo servo;
const int servoPin = 9;
const int openAngle = 0;     // lid open
const int closeAngle = 90;   // lid closed

// Ultrasonic sensor setup
const int trigPin = 5;
const int echoPin = 6;
long distance, averageDistance;
long averDist[3];

// Thresholds
const int distanceThreshold = 20;  // cm
const int maxValidDistance = 200;  // ignore noise beyond 200 cm

void setup() {
  Serial.begin(9600);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  servo.attach(servoPin);
  servo.write(closeAngle);   // start closed
  delay(100);                // let sensor stabilize
}

void loop() {
  // Measure distance 3 times for stability
  for (int i = 0; i < 3; i++) {
    distance = readDistance();
    averDist[i] = distance;
    delay(10);
  }

  // Average distance
  averageDistance = (averDist[0] + averDist[1] + averDist[2]) / 3;

  // Debug info
  Serial.print("Average Distance: ");
  Serial.print(averageDistance);
  Serial.println(" cm");

  // Ignore invalid / too far values
  if (averageDistance > maxValidDistance) {
    Serial.println("Out of range, ignoring...");
    delay(500);
    return;
  }

  // Servo control
  if (averageDistance <= distanceThreshold) {
    servo.write(openAngle);   // open lid
    delay(1500);              // stay open briefly
  } else {
    servo.write(closeAngle);  // close lid
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

  // Measure echo with timeout (60 ms = ~10m max)
  long duration = pulseIn(echoPin, HIGH, 60000);

  if (duration == 0) {
    return 999;  // no echo
  }

  float distance = duration / 58.0;  // convert to cm
  return distance;
}
