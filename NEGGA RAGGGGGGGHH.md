#include <Servo.h>

// Sensor pins
const int metalSensor = 22;
const int plasticInductiveSensor = 23;
const int plasticCapacitiveSensor = 24;

// Plastic Bin RGB LED pins
const int plasticRed = 25;
const int plasticGreen = 26;

// Metal Bin RGB LED pins
const int metalRed = 27;
const int metalGreen = 28;

// Servo motor pins
const int metalServoPin = 29;
const int plasticServoPin = 30;

// Servo objects
Servo metalServo;
Servo plasticServo;

void setup() {
  // Set sensor pins as inputs
  pinMode(metalSensor, INPUT);
  pinMode(plasticInductiveSensor, INPUT);
  pinMode(plasticCapacitiveSensor, INPUT);

  // Set RGB LED pins as outputs
  pinMode(plasticRed, OUTPUT);
  pinMode(plasticGreen, OUTPUT);
  pinMode(metalRed, OUTPUT);
  pinMode(metalGreen, OUTPUT);

  // Attach servos
  metalServo.attach(metalServoPin);
  plasticServo.attach(plasticServoPin);

  // Set initial servo positions (bins closed)
  metalServo.write(0);
  plasticServo.write(0);

  // Turn off all LEDs initially
  digitalWrite(plasticRed, LOW);
  digitalWrite(plasticGreen, LOW);
  digitalWrite(metalRed, LOW);
  digitalWrite(metalGreen, LOW);
}

void loop() {
  bool isMetal = digitalRead(metalSensor);
  bool isPlasticInductive = digitalRead(plasticInductiveSensor);
  bool isPlasticCapacitive = digitalRead(plasticCapacitiveSensor);

  // **Priority: Metal Detection First**
  if (isMetal) {
    // Turn on yellow LED for metal bin
    digitalWrite(metalRed, HIGH);
    digitalWrite(metalGreen, HIGH);
    digitalWrite(plasticRed, LOW);
    digitalWrite(plasticGreen, LOW);
    
    // Open metal bin
    metalServo.write(90);
    delay(2000);
    metalServo.write(0);
  }
  // **If no metal is detected, check for plastic**
  else if (isPlasticInductive || isPlasticCapacitive) {
    // Turn on yellow LED for plastic bin
    digitalWrite(plasticRed, HIGH);
    digitalWrite(plasticGreen, HIGH);
    digitalWrite(metalRed, LOW);
    digitalWrite(metalGreen, LOW);
    
    // Open plastic bin
    plasticServo.write(90);
    delay(2000);
    plasticServo.write(0);
  }
  // **If no valid object is detected**
  else {
    // Turn on red LEDs for both bins (unrecognized object)
    digitalWrite(plasticRed, HIGH);
    digitalWrite(plasticGreen, LOW);
    digitalWrite(metalRed, HIGH);
    digitalWrite(metalGreen, LOW);
  }

  delay(500); // Small delay before the next cycle
}
