#include <Wire.h>
#include <DS1302.h>
#include <LiquidCrystal_I2C.h>

// RTC Module Pins
#define RST_PIN 8
#define DAT_PIN 7
#define CLK_PIN 6
DS1302 rtc(RST_PIN, DAT_PIN, CLK_PIN);

// LCD Setup
LiquidCrystal_I2C lcd(0x27, 16, 2);

// Buzzer and Button Pins
#define BUZZER 9
#define BTN_SET_CLOCK 2
#define BTN_ADJUST_UP 3
#define BTN_ADJUST_DOWN 4
#define BTN_SET_TIME 5

// Time Variables
int alarmHour = 7;
int alarmMinute = 30;
bool alarmOn = false;
bool settingTime = false;
int setHour, setMinute;
bool settingHour = true;

void setup() {
    Serial.begin(9600);
    
    rtc.halt(false);
    rtc.writeProtect(false);

    lcd.begin();
    lcd.backlight();
    lcd.clear();
    
    pinMode(BUZZER, OUTPUT);
    pinMode(BTN_SET_CLOCK, INPUT_PULLUP);
    pinMode(BTN_ADJUST_UP, INPUT_PULLUP);
    pinMode(BTN_ADJUST_DOWN, INPUT_PULLUP);
    pinMode(BTN_SET_TIME, INPUT_PULLUP);

    Serial.println("Alarm Clock Initialized");
}

void loop() {
    if (!settingTime) {
        displayCurrentTime();
        checkAlarm();

        if (digitalRead(BTN_SET_CLOCK) == LOW) {
            enterTimeSettingMode();
        }
    } else {
        handleTimeSetting();
    }

    if (digitalRead(BTN_SET_CLOCK) == LOW && alarmOn) {
        stopAlarm();
    }

    delay(200);
}

// Display Current Time
void displayCurrentTime() {
    DS1302::DateTime now = rtc.getDateTime();
    lcd.setCursor(0, 0);
    lcd.print("Time: ");
    lcd.print(formatDigit(now.hour));
    lcd.print(":");
    lcd.print(formatDigit(now.minute));
    lcd.print(":");
    lcd.print(formatDigit(now.second));

    lcd.setCursor(0, 1);
    lcd.print("Alarm: ");
    lcd.print(formatDigit(alarmHour));
    lcd.print(":");
    lcd.print(formatDigit(alarmMinute));
}

// Check Alarm Trigger
void checkAlarm() {
    DS1302::DateTime now = rtc.getDateTime();
    if (now.hour == alarmHour && now.minute == alarmMinute && !alarmOn) {
        Serial.println("ALARM TRIGGERED!");
        alarmOn = true;
    }

    if (alarmOn) {
        digitalWrite(BUZZER, HIGH);
    }
}

// Enter Time Setting Mode
void enterTimeSettingMode() {
    settingTime = true;
    DS1302::DateTime now = rtc.getDateTime();
    setHour = now.hour;
    setMinute = now.minute;
    
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Set Time:");
    updateLCD();
}

// Handle Time Setting
void handleTimeSetting() {
    if (digitalRead(BTN_ADJUST_UP) == LOW) {
        if (settingHour) setHour = (setHour + 1) % 24;
        else setMinute = (setMinute + 1) % 60;
        updateLCD();
        delay(300);
    }

    if (digitalRead(BTN_ADJUST_DOWN) == LOW) {
        if (settingHour) setHour = (setHour - 1 + 24) % 24;
        else setMinute = (setMinute - 1 + 60) % 60;
        updateLCD();
        delay(300);
    }

    if (digitalRead(BTN_SET_TIME) == LOW) {
        if (settingHour) {
            settingHour = false;
        } else {
            rtc.setDateTime(2025, 3, 13, setHour, setMinute, 0);
            settingTime = false;
            settingHour = true;
            lcd.clear();
        }
        updateLCD();
        delay(300);
    }
}

// Update LCD During Time Setting
void updateLCD() {
    lcd.setCursor(0, 1);
    lcd.print(" ");
    lcd.print(formatDigit(setHour));
    lcd.print(":");
    lcd.print(formatDigit(setMinute));
    lcd.print(settingHour ? " H" : " M");
}

// Stop Alarm
void stopAlarm() {
    digitalWrite(BUZZER, LOW);
    alarmOn = false;
    Serial.println("ALARM STOPPED!");
}

// Format Time Digits (0-9 -> "09")
String formatDigit(int num) {
    return (num < 10) ? "0" + String(num) : String(num);
}
