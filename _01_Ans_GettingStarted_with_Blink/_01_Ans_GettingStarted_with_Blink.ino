//A first sketch to blink and LED

//Declare which pin is connected to the LED
//Use the Teensy Reference Card and the board schematics to
//determine the pin number
const uint8_t redLEDpin = 21;

elapsedMillis blinkCounter;

boolean ledState = false;

void setup() {
  // put your setup code here, to run once:
  pinMode(redLEDpin, OUTPUT);
  blinkCounter = 0;
}

void loop() {
  // put your main code here, to run repeatedly:
  if (blinkCounter >= 100){
    blinkCounter = 0;
    ledState = !ledState;
    digitalWrite(redLEDpin, ledState); 
  }
}
