#include <Servo.h>

Servo sorterServo;

const int trigPin = 6;  // HC-SR04 Trig pin
const int echoPin = 7;  // HC-SR04 Echo pin
const int sensorPin = 2; // Inductive proximity sensor
const int servoPin = 9;  // Servo motor pin

void setup() {
    pinMode(trigPin, OUTPUT);
    pinMode(echoPin, INPUT);
    pinMode(sensorPin, INPUT);
    sorterServo.attach(servoPin);
    sorterServo.write(90);  // Default (neutral) position
    Serial.begin(9600);
}

// Function to measure distance using HC-SR04
float getDistance() {
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    
    long duration = pulseIn(echoPin, HIGH);
    float distance = duration * 0.034 / 2;  // Convert to cm
    return distance;
}

void loop() {
    float distance = getDistance();

    if (distance < 10) {  // If object is detected within 10 cm
        Serial.println("Object detected!");
        delay(500);  // Small delay to stabilize reading

        int metalDetected = digitalRead(sensorPin); // Check for metal

        if (metalDetected == HIGH) {  
            Serial.println("Metal detected!");
            sorterServo.write(0);  // Move to Metal Bin
        } else {
            Serial.println("Plastic or other non-metal detected!");
            sorterServo.write(180); // Move to Non-Metal Bin
        }

        delay(1000);  // Wait while sorting
        sorterServo.write(90); // Reset to neutral position

        // **Wait until object is removed before running again**
        while (getDistance() < 10) {
            delay(100); // Keep checking until object is removed
        }
    }
}
