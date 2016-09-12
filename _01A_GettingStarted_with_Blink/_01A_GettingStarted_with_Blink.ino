//A first sketch to blink and LED

//Declare which pin is connected to the LED
//Use the Teensy Reference Card and the board schematics to
//determine the pin number
const int redLEDpin = 21;

elapsedMillis blinktimer;

boolean LEDstate = 0;

void setup() {
  // put your setup code here, to run once:
  pinMode(redLEDpin, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(blinktimer >= 500){
    blinktimer = 0;
    LEDstate = !LEDstate;
    digitalWrite(redLEDpin, LEDstate);
  }
}
