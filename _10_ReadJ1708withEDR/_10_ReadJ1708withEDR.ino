//Reading data from CAN and displaying it on a serial port

//Declare which pin is connected to the LED
//Use the Teensy Reference Card and the board schematics to
//determine the pin number
#define greenLED  14 //2 for SSS2, 14 for EDR
#define redLEDpin 5


//set up a timer to toggle the LEDs so the delay function isn't needed.
elapsedMillis LEDtoggleTimer;
elapsedMillis TXTimer;


//Keep track of the LED state
boolean ledState = false;
boolean greenLEDstate = false;


void setup() {
  // put your setup code here, to run once:
  pinMode(redLEDpin, OUTPUT);
  pinMode(greenLED, OUTPUT);
  pinMode(22, INPUT_PULLUP);

  boolean greenLEDstate = true;
  boolean redLEDstate = true;
  boolean LEDstate = true;
  digitalWrite(greenLED, greenLEDstate);
  
  Serial1.begin(9600);
  Serial1.setRX(27);
  Serial1.setTX(26);
 
 
  
  //try to wait for the Serial bus to come up for 1 second
  delay(1000);
  Serial.println(F("Teensy 3.6 J1708 Receive Test."));

  //print a header
  Serial.print(F("Count,uSec,ID,DLC"));
  for (uint8_t i = 1; i < 9; i++) { //label the byte columns according to J1939
    char byteDigits[7]; //declare a byte display array
    sprintf(byteDigits, ",B%i", i);
    Serial.print(byteDigits);
  }
  Serial.println();

}

void loop() {
  // put your main code here, to run repeatedly:
  while (Serial1.available()) {
    char c = Serial1.read();
    Serial.print(c);
//    char characterHex[8];
//    sprintf(characterHex, "%02X ", c);
//    Serial.println(characterHex);
  }

 
  
  if (TXTimer > 240){
    TXTimer = 0;
    byte digit = random();
    Serial.println("Test Message");
  }
  
  digitalWrite(redLEDpin, !digitalRead(22));
 
  
  if (LEDtoggleTimer >= 1000) {
    LEDtoggleTimer = 0; //reset the timer
    ledState = !ledState; // Toggle values
    digitalWrite(LED_BUILTIN, ledState);
  }

}
