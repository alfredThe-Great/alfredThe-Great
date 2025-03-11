#include <Servo.h>

Servo sorterServo;

const int sensorPin = 2;  // Inductive proximity sensor pin
const int irSensorPin = 3; // IR sensor pin (optional, can be removed)
const int servoPin = 9;   // Servo motor pin

void setup() {
    pinMode(sensorPin, INPUT);
    pinMode(irSensorPin, INPUT);
    sorterServo.attach(servoPin);
    sorterServo.write(90);  // Neutral position
    Serial.begin(9600);
}

void loop() {
    int metalDetected = digitalRead(sensorPin);
    int objectPresent = digitalRead(irSensorPin); // Check if an object is present

    if (objectPresent == HIGH) { // If an object is detected
        delay(500); // Small delay to stabilize reading

        if (metalDetected == HIGH) {  
            Serial.println("Metal detected!");
            sorterServo.write(0);  // Move servo to Metal Bin
        } else {
            Serial.println("Plastic or other non-metal detected!");
            sorterServo.write(180); // Move servo to Non-Metal Bin
        }

        delay(1000); // Wait for sorting action
        sorterServo.write(90); // Reset to neutral position
    }

    delay(500); // Small delay before next reading
}
