/*
 * Hands-On Heavy Duty Protocols
 * 
 * Arduino Sketch to emulate the J1939 messages from an electronic brake controller
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
elapsedMillis hundredMillisTimer; //keep track of the time elapese between broadcasting 100ms messages


const int millisBetweenRequests = 100;

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
  
  CANbus.begin();
  rxmsg.timeout = 0;
  txmsg.timeout = 0;

  txmsg.ext = 1;
  txmsg.len = 8;
  memset(txmsg.buf,0,8);
}

void loop() {
  // put your main code here, to run repeatedly:

  if(CANbus.read(rxmsg)){
    rxCount++;
    CANRXTimer = 0; //reset the timer since the last CAN message was received.
    //add these to toggle the LEDs when a message arrives.
    greenLEDstate = !greenLEDstate;
    digitalWrite(greenLEDpin, greenLEDstate);  
  }
  
  if (LEDtoggleTimer >=500){
    LEDtoggleTimer = 0; //reset the timer
    ledState = !ledState; // Toggle values
    digitalWrite(LED_BUILTIN,ledState);
  }

  if (CANRXTimer > 200) digitalWrite(greenLEDpin,LOW); //Turn off the LED if no CAN traffic is present.


  if (hundredMillisTimer >= 100){
    hundredMillisTimer = 0;
    
    txmsg.id = 0x18F0010B; //EBC1 J1939 message
    CANbus.write(txmsg);
    txCount++;
    
    txmsg.id = 0x18FEF117; //EBC1 J1939 message
    CANbus.write(txmsg);
    txCount++;
    
    txmsg.id = 0x18FEBF0B; //EBC2 J1939 message
    CANbus.write(txmsg);
    txCount++;
  }
}
