#include <Servo.h>

// Pin Definitions
#define redpin 5
#define yellowpin 6
#define plasticsensor A0
#define metalsensor A1

#define redpin_M 7
#define yellowpin_M 8
#define metalsensor_M A2

Servo myservo;   // Plastic bin servo
Servo myservo_M; // Metal bin servo

int pos = 165;   // Default plastic bin position
int pos_M = 158; // Default metal bin position

void setup() {
    myservo.attach(11);
    myservo_M.attach(12);
    
    pinMode(redpin, OUTPUT);
    pinMode(yellowpin, OUTPUT);
    
    pinMode(redpin_M, OUTPUT);
    pinMode(yellowpin_M, OUTPUT);
    
    pinMode(plasticsensor, INPUT_PULLUP);
    pinMode(metalsensor, INPUT_PULLUP);
    pinMode(metalsensor_M, INPUT_PULLUP);
    
    Serial.begin(9600);

    // Default LED state (OFF)
    digitalWrite(redpin, LOW);
    digitalWrite(yellowpin, LOW);
    digitalWrite(redpin_M, LOW);
    digitalWrite(yellowpin_M, LOW);
}

void loop() {
    int sensor_read_plastic = digitalRead(plasticsensor);
    int sensor_read_metal = digitalRead(metalsensor);
    int sensor_read_metaletal2 = digitalRead(metalsensor_M);

    Serial.println("Plastic Sensor: " + String(sensor_read_plastic));
    Serial.println("Metal Sensor: " + String(sensor_read_metal));
    Serial.println("Metal Sensor 2: " + String(sensor_read_metaletal2));

    // **Plastic Bin Logic**
    if ((sensor_read_plastic == 0) && (sensor_read_metal != 1)) {
        digitalWrite(redpin, HIGH);   // Red when detecting
        delay(500);

        for (pos = 160; pos >= 90; pos--) {
            myservo.write(pos);
            delay(1);
        }

        digitalWrite(redpin, LOW);
        digitalWrite(yellowpin, HIGH); // Yellow when classification is done
        delay(2500);

        for (pos = 90; pos <= 160; pos++) {
            myservo.write(pos);
            delay(1);
        }

        digitalWrite(yellowpin, LOW);
    } else {
        myservo.write(pos);
    }

    // **Metal Bin Logic**
    if (sensor_read_metaletal2 == 1) {
        digitalWrite(redpin_M, HIGH);   // Red when detecting
        delay(500);

        for (pos_M = 160; pos_M >= 90; pos_M--) {
            myservo_M.write(pos_M);
            delay(1);
        }

        digitalWrite(redpin_M, LOW);
        digitalWrite(yellowpin_M, HIGH); // Yellow when classification is done
        delay(2500);

        for (pos_M = 90; pos_M <= 160; pos_M++) {
            myservo_M.write(pos_M);
            delay(1);
        }

        digitalWrite(yellowpin_M, LOW);
    } else {
        myservo_M.write(pos_M);
    }
}
