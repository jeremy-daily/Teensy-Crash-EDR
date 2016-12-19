/*
 * Hands-On Heavy Duty Protocols
 * 
 * Arduino Sketch to read data from CAN and display it on a serial port
 * Include the realtime clock functions inspired by the TimeTeensy3.ino example
 * 
 * Add capability to send request messages on J1939
 * 
 * Written By Dr. Jeremy S. Daily
 * The University of Tulsa
 * Department of Mechanical Engineering
 * 
 * 19 December 2016
 * 
 * Released under the MIT License
 *
 * Copyright (c) 2016        Jeremy S. Daily
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.//Reading data from CAN and displaying it on a serial port
 * 
 * This sketch was inspired buy the realtime clock functions inspired by the TimeTeensy3.ino example
 * 
 * Assignment:
 * 1. Add at least 5 new requests for J1939 PGNs that are on request only.   
 * 
 * 2. Add a serial display line with the Transmit buffer contents. Indicate TX or RX on the displayed line.
 *
 */


//Include the CAN libraries for the Teensy microprocessor
#include <FlexCAN.h>
#include <kinetis_flexcan.h>

#include <TimeLib.h>

const uint16_t PGNRequestList[28] = {
  65261, // Cruise Control/Vehicle Speed Setup
  65214, // Electronic Engine Controller 4
  65259, // Component Identification
  65242, // Software Identification
  65244, // Idle Operation
  65260, // Vehicle Identification
  65255, // Vehicle Hours

};

uint8_t pgnIndex = 0;

//Declare which pin is connected to the LED
//Use the Teensy Reference Card and the board schematics to determine the pin number
const uint8_t redLEDpin = 5;
const uint8_t greenLEDpin = 14;

//initiate the CAN library at 250kbps
FlexCAN CANbus(250000);

//Set up the CAN data structure
static CAN_message_t rxmsg;
static CAN_message_t txmsg; //Add another data structure

//set up a counter for each message
unsigned long int rxCount = 0;
uint32_t txCount = 0;

//set up a timer to toggle the LEDs so the delay function isn't needed.
elapsedMillis LEDtoggleTimer;
elapsedMillis CANRXTimer; //Keep track of how long its been since a CAN message was received
elapsedMillis displayTimer; //Only display data every so often.
elapsedMillis requestTimer; //The count of milliseconds between each request

//Keep track of microseconds
elapsedMicros microsecondsPerSecond;
elapsedMicros microsBetweenMessages;

const int millisBetweenRequests = 1000;

//Keep track of the LED states
boolean ledState = false;
boolean redLEDstate = false;
boolean greenLEDstate = true;


void setup() {
  // put your setup code here, to run once:

  pinMode(redLEDpin, OUTPUT);
  pinMode(greenLEDpin, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);

  //Set the LED display values.
  digitalWrite(LED_BUILTIN,ledState);
  digitalWrite(redLEDpin, redLEDstate); 
  digitalWrite(greenLEDpin, greenLEDstate); 
  
  //try to wait for the Serial bus to come up for 1 second
  delay(1000);
  Serial.println(F("Teensy 3.6 CAN Send Request Messages"));
  
  // set the Time library to use Teensy 3.0's RTC to keep time
  setSyncProvider(getTeensy3Time);
  if (timeStatus()!= timeSet) {
    Serial.println(F("Unable to sync with the RTC"));
  } else {
    Serial.println(F("RTC has set the system time"));
  }
  setSyncInterval(1);

  //Display current time. 
  char timeString[32];
  sprintf(timeString,"%04d-%02d-%02d %02d:%02d:%02d.%06d",year(),month(),day(),hour(),minute(),second(),uint32_t(microsecondsPerSecond));
  Serial.println(timeString);
    
  //start the CAN access
  CANbus.begin();
  rxmsg.timeout = 0;
  txmsg.timeout = 0;

  
  //try to wait for the Serial bus to come up for 1 second
  delay(1000);
  Serial.println(F("Teensy 3.6 CAN Receive Test with Request Messages."));
  
  //Set System Time
  if (timeStatus()!= timeSet) {
    Serial.println(F("Unable to sync with the RTC"));
  } 
  else {
    Serial.println(F("RTC has set the system time"));
  }
  
   //print a header
  Serial.print(F("     Count     micros YYYY-MM-DD HH:MM:SS.usec dT(us)   CAN ID DLC"));
  for (uint8_t i = 1; i<9;i++){ //label the byte columns according to J1939
    char byteDigits[4]; //declare a byte display array
    sprintf(byteDigits," B%i",i);
    Serial.print(byteDigits); 
  }

}

void loop() {
  // put your main code here, to run repeatedly:

   // Synchronize the RTC to your PC time.
    if (Serial.available()) {
      time_t t = processSyncMessage();
      if (t != 0) {
        Teensy3Clock.set(t); // set the RTC
        setTime(t);
        redLEDstate = true; 
        digitalWrite(redLEDpin, redLEDstate); // show RED LED to show clock was set. 
      }
    }
  
  if(CANbus.read(rxmsg)){
    rxCount++;
    CANRXTimer = 0; //reset the timer since the last CAN message was received.
    
    //add these to toggle the LEDs when a message arrives.
    greenLEDstate = !greenLEDstate;
    digitalWrite(greenLEDpin, greenLEDstate); 
    
    uint32_t ID = rxmsg.id;
    uint8_t len = rxmsg.len;
    
    char timeCountIDandDLCdigits[50]; 
    sprintf(timeCountIDandDLCdigits,"%10i %10i %04i-%02i-%02iT%02i:%02i:%02i.%06i %6i %08X %1i",rxCount,micros(),year(),month(),day(),hour(),minute(),second(),int(microsecondsPerSecond),int(microsBetweenMessages),ID,len);
    Serial.print(timeCountIDandDLCdigits); 
      
    for (uint8_t i = 0; i<len;i++){ 
      char byteDigits[4]; 
      sprintf(byteDigits," %02X",rxmsg.buf[i]);
      Serial.print(byteDigits); 
    }
    Serial.println();
   
    microsBetweenMessages = 0; //reset the timer between each message
   
  }
  
  if (LEDtoggleTimer >=500){
    LEDtoggleTimer = 0; //reset the timer
    ledState = !ledState; // Toggle values
    digitalWrite(LED_BUILTIN,ledState);
  }

  if (CANRXTimer > 200) digitalWrite(greenLEDpin,LOW); //Turn off the LED if no CAN traffic is present.




  if (requestTimer >= millisBetweenRequests) {
    requestTimer = 0;
    uint16_t pgnToRequest = PGNRequestList[pgnIndex];
    pgnIndex++;
    if (pgnIndex > sizeof(PGNRequestList) ) pgnIndex = 0;

  
    txmsg.ext = 1;
    txmsg.id = 0x18EA00F9; //request PGN
    txmsg.len = 3;
    txmsg.buf[0] = (pgnToRequest & 0x0000FF);
    txmsg.buf[1] = (pgnToRequest & 0x00FF00) >> 8 ;
    txmsg.buf[2] = (pgnToRequest & 0xFF0000) >> 16;
    CANbus.write(txmsg);
    txCount++;
   
    microsBetweenMessages=0;
  
  }
  

  
}

time_t getTeensy3Time(){
  microsecondsPerSecond = 0; //If this function gets called every second, then this can keep track of microseconds 
  return Teensy3Clock.get();
}


/*  code to process time sync messages from the serial port   */
#define TIME_HEADER  "T"   // Header tag for serial time sync message
const uint32_t DEFAULT_TIME = 1357041600; // Jan 1 2013 

uint32_t processSyncMessage() {
  uint32_t pctime = 0L;
  
  if(Serial.find(TIME_HEADER)) {
     pctime = Serial.parseInt();
     if( pctime < DEFAULT_TIME) { // check the value is a valid time (greater than Jan 1 2013)
       pctime = 0L; // return 0 to indicate that the time is not valid
     }
  }
  if (displayTimer >=1000){ //Display only if asked.
    displayTimer = 0;
    char timeStamp[35];
    sprintf(timeStamp,"%04d-%02d-%02d %02d:%02d:%02d",year(),month(),day(),hour(),minute(),second());
    Serial.println(timeStamp);
  }  
  return pctime;
}

