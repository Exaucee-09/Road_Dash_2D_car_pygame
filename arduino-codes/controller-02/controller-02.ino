const int joyXPin1 = A0;
const int joyYPin1 = A1;
const int joyXPin2 = A2;
const int joyYPin2 = A3;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int joyX1 = analogRead(joyXPin1);
  int joyY1 = analogRead(joyYPin1);
  int joyX2 = analogRead(joyXPin2);
  int joyY2 = analogRead(joyYPin2);

  Serial.print(joyX1);
  Serial.print(",");
  Serial.print(joyY1);
  Serial.print(",");
  Serial.print(joyX2);
  Serial.print(",");
  Serial.print(joyY2);
  Serial.println("");
  delay(100);
}