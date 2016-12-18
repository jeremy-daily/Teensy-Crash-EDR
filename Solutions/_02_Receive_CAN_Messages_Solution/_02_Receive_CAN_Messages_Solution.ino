/* ANSWER
 * Hands-On Heavy Duty Protocols
 * 
 * Arduino Sketch to test the ability to receive CAN messages
 * 
 * Written By Dr. Jeremy S. Daily
 * The University of Tulsa
 * Department of Mechanical Engineering
 * 
 * 17 December 2016
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
 * SOFTWARE.
 * 
 * 
 * Assignment: 
 * 1. Install the FlexCAN2 library by selecting Sketch -> Include Library -> Add Zip Library
 *    Select the FlexCAN2 directory from the libraries folder. This must be done before
 *    this sketch will compile. (Note: the original FlexCAN library will work too).
 * 2. Add the ability to keep track of the number of received messages and display it.
 * 3. Toggle the LEDs each time a message arrives. 
 * 4. Change the output to be in decimal (instead of Hex)
 * 5. Make the data tab separated. 
 * 
 */

//Include the CAN libraries for the Teensy 3.6 microprocessor
#include <FlexCAN2.h>
#include <kinetis_flexcan.h>


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

//Keep track of the LED states
boolean ledState = false;
boolean redLEDstate = false;
boolean greenLEDstate = true;

void setup() {
  // put your setup code here, to run once:
  pinMode(redLEDpin, OUTPUT);
  pinMode(greenLEDpin, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  
  //start the CAN access
  CANbus.begin();
  rxmsg.timeout = 0; 
  
  //try to wait for the Serial bus to come up for 1 second
  delay(1000);
  Serial.println(F("Teensy 3.6 CAN Receive Test.")); //stores static text in the larger flash memory instead of the program stack. 

  //print a header to understand the displayed data.
  Serial.print(F("Count\tuSec\tID\tDLC"));
  for (uint8_t i = 1; i<9;i++){ //label the byte columns according to J1939
    char byteDigits[7]; //declare a byte display array
    sprintf(byteDigits,"\tB%i",i);
    Serial.print(byteDigits); 
  }
  Serial.println();

  //Set the LED display values.
  digitalWrite(LED_BUILTIN,ledState);
  digitalWrite(redLEDpin, redLEDstate); 
  digitalWrite(greenLEDpin, greenLEDstate); 
}

void loop() {
  // put your main code here, to run repeatedly:
  if(CANbus.read(rxmsg)){
    rxCount++;
    
    //add these to toggle the LEDs when a message arrives.
    redLEDstate = !redLEDstate;
    greenLEDstate = !greenLEDstate;
    digitalWrite(redLEDpin, redLEDstate); 
    digitalWrite(greenLEDpin, greenLEDstate); 
    
    uint32_t ID = rxmsg.id;
    uint8_t len = rxmsg.len;
    
    char timeCountIDandDLCdigits[40]; 
    sprintf(timeCountIDandDLCdigits,"%10i\t%10i\t%10i\t%1i",rxCount,micros(),ID,len);
    Serial.print(timeCountIDandDLCdigits); 
      
    for (uint8_t i = 0; i<len;i++){ 
      char byteDigits[12]; 
      sprintf(byteDigits,"\t%3i",rxmsg.buf[i]);
      Serial.print(byteDigits); 
    }
    Serial.println();
  }
  
  if (LEDtoggleTimer >=500){ //Use this LED to provide feedback to the user that the loop is running. 
    LEDtoggleTimer = 0; //reset the timer
    ledState = !ledState; // Toggle values
    digitalWrite(LED_BUILTIN,ledState);
  }
  
}
