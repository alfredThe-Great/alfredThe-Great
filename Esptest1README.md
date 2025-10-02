#define LED_BUILTIN 33   // onboard flash LED is GPIO33

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH); // LED ON
  delay(1000);
  digitalWrite(LED_BUILTIN, LOW);  // LED OFF
  delay(1000);
}
