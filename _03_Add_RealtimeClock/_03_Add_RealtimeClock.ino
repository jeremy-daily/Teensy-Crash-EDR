/*
 * Hands-On Heavy Duty Protocols
 * 
 * Arduino Sketch to include real time stamps to received CAN messages
 * 
 * Written By Dr. Jeremy S. Daily
 * The University of Tulsa
 * Department of Mechanical Engineering
 * 
 * 29 September 2016
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
 * 1. Set the time of the Teensy 3.6 by sending the formatted time string from the PC
 *    using the python time setting script. 
 * 2. Add the decimal value for real time stamp to the serial output console
 * 3. (ADVANCED) Include an interrupt to keep track of the number of microseconds
 *    between each second. 
 * 4. Display the difference in microseconds between each CAN message.   
 */

//Include the CAN libraries for the Teensy 3.6 microprocessor
#include <FlexCAN2.h>
#include <kinetis_flexcan.h>

#include <TimeLib.h>


//Declare which pin is connected to the LED
//Use the Teensy Reference Card and the board schematics to determine the pin number.
const uint8_t redLEDpin = 5;
const uint8_t greenLEDpin = 14;

//initiate the CAN library at 250kbps
FlexCAN CANbus(250000);

//Set up the CAN data structure
static CAN_message_t rxmsg;

//set up a counter for each received message
unsigned long int rxCount = 0;

//set up a timer to toggle the LEDs so the delay function isn't needed.
elapsedMillis LEDtoggleTimer;
elapsedMillis displayTimer;

//Keep track of microseconds
elapsedMicros microsecondsPerSecond;


//Keep track of the LED states
boolean ledState = false;
boolean redLEDstate = false;
boolean greenLEDstate = true;


//set up a variable to keep track of the timestamp
time_t previousTime = 0;

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
  Serial.println(F("Teensy 3.6 CAN Receive Test."));
  
  // set the Time library to use Teensy 3.0's RTC to keep time
  setSyncProvider(getTeensy3Time);
  if (timeStatus()!= timeSet) {
    Serial.println("Unable to sync with the RTC");
  } else {
    Serial.println("RTC has set the system time");
  }
  setSyncInterval(1);

  //Display current time. 
  char timeString[32];
  sprintf(timeString,"%04d-%02d-%02d %02d:%02d:%02d.%06d",year(),month(),day(),hour(),minute(),second(),uint32_t(microsecondsPerSecond));
  Serial.println(timeString);
  
  //start the CAN access
  CANbus.begin();
  rxmsg.timeout = 0;
  
  //print a header
  Serial.print(F("     Count\t    micros\tYYYY-MM-DD HH:MM:SS.ms\t  CAN ID\tDLC"));
  for (uint8_t i = 1; i<9;i++){ //label the byte columns according to J1939
    char byteDigits[4]; //declare a byte display array
    sprintf(byteDigits,"\tB%i",i);
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
      }
    }
  
  
  if(CANbus.read(rxmsg)){
    rxCount++;
    
    uint32_t ID = rxmsg.id;
    uint8_t len = rxmsg.len;
    
    char timeCountIDandDLCdigits[50]; 
    sprintf(timeCountIDandDLCdigits,"%10i\t%10i\t%04i-%02i-%02iT%02i:%02i:%02i.%06i\t%08X\t%1i",rxCount,micros(),year(),month(),day(),hour(),minute(),second(),int(microsecondsPerSecond),ID,len);
    Serial.print(timeCountIDandDLCdigits); 
      
    for (uint8_t i = 0; i<len;i++){ 
      char byteDigits[4]; 
      sprintf(byteDigits,"\t%02X",rxmsg.buf[i]);
      Serial.print(byteDigits); 
    }
    Serial.println();
    redLEDstate = !redLEDstate;
    greenLEDstate = !greenLEDstate;
    digitalWrite(redLEDpin, redLEDstate); 
    digitalWrite(greenLEDpin, greenLEDstate); 
  }
  
  if (LEDtoggleTimer >=500){
    LEDtoggleTimer = 0; //reset the timer
    ledState = !ledState; // Toggle values
    digitalWrite(LED_BUILTIN,ledState);
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

