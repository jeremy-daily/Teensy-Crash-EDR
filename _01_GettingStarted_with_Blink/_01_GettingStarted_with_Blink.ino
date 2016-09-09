//A first sketch to blink and LED

//Declare which pin is connected to the LED
//Use the Teensy Reference Card and the board schematics to
//determine the pin number
const int redLEDpin = 21;



void setup() {
  // put your setup code here, to run once:
  pinMode(redLEDpin, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(redLEDpin, HIGH);
  delay(500);
  digitalWrite(redLEDpin, LOW);
  delay(500);
}
