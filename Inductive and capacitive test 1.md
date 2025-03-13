#include <Servo.h>  // Servo motor library

// Pin Definitions for Plastic Bin LED
#define RED_LED_PLASTIC 5
#define YELLOW_LED_PLASTIC 6

// Pin Definitions for Metal Bin LED
#define RED_LED_METAL 7
#define YELLOW_LED_METAL 8

// Sensor Pins
#define PLASTIC_SENSOR A0
#define METAL_SENSOR A1
#define METAL_SENSOR_2 A2

// Servo Objects
Servo servoPlastic; // Plastic bin servo
Servo servoMetal;   // Metal bin servo

// Default Servo Positions
int posPlastic = 165;  // Default position for plastic bin servo
int posMetal = 158;    // Default position for metal bin servo

void setup() {
    // Attach servos
    servoPlastic.attach(11);  // Plastic bin servo on pin 11
    servoMetal.attach(12);    // Metal bin servo on pin 12

    // LED setup
    pinMode(RED_LED_PLASTIC, OUTPUT);
    pinMode(YELLOW_LED_PLASTIC, OUTPUT);
    pinMode(RED_LED_METAL, OUTPUT);
    pinMode(YELLOW_LED_METAL, OUTPUT);

    // Sensor input pins
    pinMode(PLASTIC_SENSOR, INPUT_PULLUP);
    pinMode(METAL_SENSOR, INPUT_PULLUP);
    pinMode(METAL_SENSOR_2, INPUT_PULLUP);

    // Start Serial Monitor
    Serial.begin(9600);

    // Set LEDs to default (off)
    resetLEDs();
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
        indicateApprovalPlastic();  // Yellow LED for plastic bin
        delay(2500);
        moveServo(servoPlastic, 90, posPlastic);
        resetLEDs();
    } 

    // Metal bin logic
    else if (metalDetected2 == HIGH) {
        moveServo(servoMetal, posMetal, 90);
        indicateApprovalMetal();  // Yellow LED for metal bin
        delay(2500);
        moveServo(servoMetal, 90, posMetal);
        resetLEDs();
    } 

    // If object is neither plastic nor metal
    else {
        indicateRejection();  // Red LED for both bins
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

// Functions to control LEDs
void indicateApprovalPlastic() {
    digitalWrite(RED_LED_PLASTIC, LOW);
    digitalWrite(YELLOW_LED_PLASTIC, HIGH);
}

void indicateApprovalMetal() {
    digitalWrite(RED_LED_METAL, LOW);
    digitalWrite(YELLOW_LED_METAL, HIGH);
}

void indicateRejection() {
    digitalWrite(RED_LED_PLASTIC, HIGH);
    digitalWrite(YELLOW_LED_PLASTIC, LOW);
    digitalWrite(RED_LED_METAL, HIGH);
    digitalWrite(YELLOW_LED_METAL, LOW);
}

void resetLEDs() {
    digitalWrite(RED_LED_PLASTIC, LOW);
    digitalWrite(YELLOW_LED_PLASTIC, LOW);
    digitalWrite(RED_LED_METAL, LOW);
    digitalWrite(YELLOW_LED_METAL, LOW);
}
