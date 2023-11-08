int joystickX, joystickY, joystickSwitch; // Corrected variable name from 'joystick' to 'joystickSwitch'
int joystickSwitchPin = 7;

void setup() {
  Serial.begin(9600); // Added a semicolon at the end of the statement
}

void loop() {
  joystickX = analogRead(A0);
  joystickY = analogRead(A1);
  joystickSwitch = digitalRead(joystickSwitchPin); // Corrected variable name

  Serial.print(joystickX);
  Serial.print(",");
  Serial.print(joystickY);
  Serial.print(",");
  Serial.println(joystickSwitch);
  
  delay(50);
}
