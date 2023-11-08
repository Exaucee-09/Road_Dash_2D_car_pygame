int joystickX, joystickY, joystickSwitch; 

void setup() {
  Serial.begin(9600); 
}

void loop() {
  joystickX = analogRead(A0);
  joystickY = analogRead(A1);
  joystickSwitch = analogRead(A2);
  Serial.print(joystickX);
  Serial.print(",");
  Serial.print(joystickY);
  Serial.print(",");
  if (joystickSwitch> 100) {
    Serial.print("0");
  } else {
    Serial.print("1");
  }
  Serial.println();
  delay(50);
}

