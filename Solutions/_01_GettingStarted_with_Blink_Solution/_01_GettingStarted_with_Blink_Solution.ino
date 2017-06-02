/* ANSWER
 * Title: A first sketch to blink an LED 
 * Description: This is a basic Ardunino program to show how to upload a program and
 * change its behavior. It is intended to be used with a board with an external LED.
 * 
 * Written by Dr. Jeremy S. Daily
 * The University of Tulsa, Department of Mechanical Engineering
 * 
 * Hardware compatibility: Teensy 3.6 based Teensy Crash EDR
 * 
 * Assignment: 
 * 1. Change the program to blink without using a delay function call.
 * To do this, use the elapsedMillis timer class and test to see if the number of elapsedMillis
 * has exceded a value. If it does, reset the time and change the LED state. You will have to 
 * declare a variable to use to keep track of the LED state.
 * 
 * 2. Add the green LED to blink out of phase with the red LED.
 * 
 * 
 */
 
//Declare which pin is connected to the LED
//Use the Teensy Reference Card and the board schematics to determine the pin number.
const uint8_t redLEDpin = 5;
const uint8_t greenLEDpin = 14;

//declare a millisecont timer object that automatically keeps track of milliseconds.
//Could also use an elapsedMicros object too.
elapsedMillis blinkTimer;

//declare and initialize the state variables for the LEDs.
boolean redLEDstate = false;
boolean greenLEDstate = true;

//declare and initialize a counter variable.
uint32_t toggleCount = 0;

void setup() {
  // put your setup code here, to run once:
  pinMode(redLEDpin, OUTPUT);
  pinMode(greenLEDpin, OUTPUT);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  if (blinkTimer >= 100){  //execute after a set duration.
    blinkTimer = 0; //reset the timer.
    redLEDstate = !redLEDstate;
    greenLEDstate = !greenLEDstate;
    
    digitalWrite(redLEDpin, redLEDstate); 
    digitalWrite(greenLEDpin, greenLEDstate); 
    
    toggleCount++;
    Serial.println(toggleCount);
  }
}
