#include <Servo.h>  // Servo motor library

// Pin Definitions
#define RED_LED 5
#define YELLOW_LED 6
#define PLASTIC_SENSOR A0
#define METAL_SENSOR A1
#define METAL_SENSOR_2 A2

Servo servoPlastic; // Servo for plastic bin
Servo servoMetal;   // Servo for metal bin

int posPlastic = 165;  // Default position for plastic bin servo
int posMetal = 158;    // Default position for metal bin servo

void setup() {
    // Attach servos
    servoPlastic.attach(11);  // Plastic bin servo on pin 11
    servoMetal.attach(12);    // Metal bin servo on pin 12

    // LED setup
    pinMode(RED_LED, OUTPUT);
    pinMode(YELLOW_LED, OUTPUT);

    // Sensor input pins
    pinMode(PLASTIC_SENSOR, INPUT_PULLUP);
    pinMode(METAL_SENSOR, INPUT_PULLUP);
    pinMode(METAL_SENSOR_2, INPUT_PULLUP);

    // Start Serial Monitor
    Serial.begin(9600);

    // Set LED to default (off)
    resetLED();
}

void loop() {
    int plasticDetected = digitalRead(PLASTIC_SENSOR);
    int metalDetected = digitalRead(METAL_SENSOR);
    int metalDetected2 = digitalRead(METAL_SENSOR_2);

    Serial.println("Plastic Sensor: " + String(plasticDetected));
    Serial.println("Metal Sensor 1: " + String(metalDetected));
    Serial.println("Metal Sensor 2: " + String(metalDetected2));

    // Plastic bin logic
    if (plasticDetected == LOW && metalDetected == LOW) {
        moveServo(servoPlastic, posPlastic, 90);
        indicateApproval();  // Yellow LED for approved object
        delay(2500);
        moveServo(servoPlastic, 90, posPlastic);
        resetLED();
    } 

    // Metal bin logic
    else if (metalDetected2 == HIGH) {
        moveServo(servoMetal, posMetal, 90);
        indicateApproval();  // Yellow LED for approved object
        delay(2500);
        moveServo(servoMetal, 90, posMetal);
        resetLED();
    } 

    // If object is neither plastic nor metal
    else {
        indicateRejection();  // Red LED for unapproved object
    }
}

// Function to move servo smoothly
void moveServo(Servo &servo, int startPos, int endPos) {
    if (startPos > endPos) {
        for (int pos = startPos; pos >= endPos; pos--) {
            servo.write(pos);
            delay(1);
        }
    } else {
        for (int pos = startPos; pos <= endPos; pos++) {
            servo.write(pos);
            delay(1);
        }
    }
}

// Function to indicate approval with Yellow LED
void indicateApproval() {
    digitalWrite(RED_LED, LOW);
    digitalWrite(YELLOW_LED, HIGH);
}

// Function to indicate rejection with Red LED
void indicateRejection() {
    digitalWrite(RED_LED, HIGH);
    digitalWrite(YELLOW_LED, LOW);
}

// Function to reset LEDs (both off)
void resetLED() {
    digitalWrite(RED_LED, LOW);
    digitalWrite(YELLOW_LED, LOW);
}
