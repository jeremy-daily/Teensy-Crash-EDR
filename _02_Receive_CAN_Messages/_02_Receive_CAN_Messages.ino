//Reading data from CAN and displaying it on a serial port

//Include the CAN libraries for the Teensy microprocessor
#include <FlexCAN.h>
#include <kinetis_flexcan.h>

//Declare which pin is connected to the LED
//Use the Teensy Reference Card and the board schematics to 
//determine the pin number
const int redLEDpin = 21;

//initiate the CAN library at 250kbps
FlexCAN CANbus(250000);

//Set up the CAN data structure
CAN_message_t rxmsg;

//set up a counter for each received message
unsigned long int rxCount = 0;

//set up a timer to toggle the LEDs so the delay function isn't needed.
elapsedMillis LEDtoggleTimer;

//Keep track of the LED state
boolean ledState = false;

void setup() {
  // put your setup code here, to run once:
  pinMode(redLEDpin,OUTPUT);

  //start the CAN access
  CANbus.begin();

  //try to wait for the Serial bus to come up for 1 second
  delay(1000);
  Serial.println(F("Hello Teensy 3.2 CAN Receive Test."));

 
    
}

void loop() {
  // put your main code here, to run repeatedly:

 
  

  if (LEDtoggleTimer >=50){
     CANbus.read(rxmsg);
      rxCount++;
      Serial.println(rxmsg.id); 
    
    
    LEDtoggleTimer = 0; //reset the timer
    ledState = !ledState; // Toggle values
    digitalWrite(redLEDpin,ledState);
  }
  
}
