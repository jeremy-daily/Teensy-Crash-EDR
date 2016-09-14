//Reading data from CAN and displaying it on a serial port

//Include the CAN libraries for the Teensy microprocessor
#include <FlexCAN.h>
//#include <kinetis_flexcan.h>

//Declare which pin is connected to the LED
//Use the Teensy Reference Card and the board schematics to 
//determine the pin number
const int redLEDpin = 21;

//initiate the CAN library at 250kbps
FlexCAN CANbus(250000);

//Set up the CAN data structure
static CAN_message_t rxmsg;

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
  rxmsg.timeout = 0;
  
  //try to wait for the Serial bus to come up for 1 second
  delay(1000);
  Serial.println(F("Teensy 3.2 CAN Receive Test."));

  //print a header
  Serial.print(F("Count,uSec,ID,DLC"));
  for (uint8_t i = 1; i<9;i++){ //label the byte columns according to J1939
    char byteDigits[7]; //declare a byte display array
    sprintf(byteDigits,",B%i",i);
    Serial.print(byteDigits); 
  }
  Serial.println();
    
}

void loop() {
  // put your main code here, to run repeatedly:
  if(CANbus.read(rxmsg)){
    rxCount++;
    
    uint32_t ID = rxmsg.id;
    uint8_t len = rxmsg.len;
    
    char timeCountIDandDLCdigits[40]; 
    sprintf(timeCountIDandDLCdigits,"%10i,%10i,\'%08X,%1i",rxCount,micros(),ID,len);
    Serial.print(timeCountIDandDLCdigits); 
      
    for (uint8_t i = 0; i<len;i++){ 
      char byteDigits[12]; 
      sprintf(byteDigits,",\'%02X",rxmsg.buf[i]);
      Serial.print(byteDigits); 
    }
    Serial.println();
  }
  
  if (LEDtoggleTimer >=100){
    LEDtoggleTimer = 0; //reset the timer
    ledState = !ledState; // Toggle values
    digitalWrite(redLEDpin,ledState);
  }
  
}
