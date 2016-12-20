/*
 * Title: Recieve CAN messages and Parse simple J1939
 * 
 * Description: An Arduino sketch to read and display data from a J1939 network.
 * The script is able to decode an extended ID to break it down to a source address
 * priority, parameter group number (PGN), and destination address. 
 * As an example, if the PGN related to the Cruise Control/Vehicle Speed message is 
 * found, it will display the vehicle speed.
 * Other suspect parameter numbers (SPNs) are also included 
 * 
 * Author: Dr. Jeremy S. Daily
 * The University of Tulsa, Mechanical Engineering
 * 
 * Assignment: 
 * 
 * 1. Add at least 3 more J1939 PGNs to be interpreted. (eg. High Resolution Vehicle Distance, Vehicle Hours, Odometer)
 * 
 * 2. (optional) Adapt the code to elimnate all serial output commands
 * except for the value for a parameter (like temperature). This data can be plotted on 
 * the Arduino Serial Plotter. Do this by commenting out Serial.print 
 * statements that are not needed. 
 * 
 */
//Include the CAN libraries for the Teensy microprocessor
#include <FlexCAN.h>
#include <TimeLib.h>

//Declare which pin is connected to the LED
//Use the Teensy Reference Card and the board schematics to determine the pin number
const uint8_t redLEDpin = 5;
const uint8_t greenLEDpin = 14;

//initiate the CAN library at 250kbps
FlexCAN CANbus(250000);

//Set up the CAN data structure
static CAN_message_t rxmsg;
static CAN_message_t txmsg; //Add another data structure

//set up a counter for each received message
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

//Keep track of the LED state
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

  // set the Time library to use Teensy 3.0's RTC to keep time
  setSyncProvider(getTeensy3Time);

  //declare the LED Pin to be the output
  pinMode(redLEDpin,OUTPUT);
  digitalWrite(redLEDpin,ledState); //Turn on the LED
 
 //try to wait for the Serial bus to come up for 1 second
  delay(1000);
  Serial.println(F("Teensy 3.6 CAN Receive with J1939 Parsing."));
 
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
    
  //print a header. The F( ) functions stores the string to be displayed in the larger flash memory
  Serial.print(F("     Count\t    micros\tYYYY-MM-DD HH:MM:SS.ms\t  CAN ID\tDLC\tPriority\thexPGN\tdecPGN\tDA\tSA"));
  for (uint8_t i = 1; i<9;i++){ //label the byte columns according to J1939
    char byteDigits[4]; //declare a byte display array
    sprintf(byteDigits,"\tB%i",i);
    Serial.print(byteDigits); 
  }
  Serial.println(F("\tAcronym\tSignals"));
  
  
}

void loop() {
  // put your main code here, to run repeatedly:

  // Uncomment this to synchronize the RTC to your PC time.
  if (Serial.available()) {
      time_t t = processSyncMessage();
      if (t != 0) {
        Teensy3Clock.set(t); // set the RTC
        setTime(t);
      }
    }
   
  while(CANbus.read(rxmsg)){
    rxCount++;
    CANRXTimer = 0; //reset the timer since the last CAN message was received.
    
    //add these to toggle the LEDs when a message arrives.
    greenLEDstate = !greenLEDstate;
    digitalWrite(greenLEDpin, greenLEDstate); 
    
    uint32_t ID = rxmsg.id;
    uint8_t len = rxmsg.len;

    //Extract J1939 data fields from the extended CAN ID
    uint8_t SA = (ID & 0xFF); //mask the last two hex digits (8 bits) //Source Address
    uint32_t PGN = (ID & 0x03FFFF00) >> 8; //Parameter Group Number
    uint8_t DA;
    if (PGN >= 0xF000) DA = 0xFF; //Broadcast message to a global address
    else {
      DA = (ID & 0x0000FF00) >> 8; //Destination specific address
      PGN = (PGN & 0x03FF00); //set the PGN value to have zeros on the second byte.
    }
    uint8_t priority = (ID & 0x1C000000) >> 26;
    
  
    //Format the output string
    char timeCountIDandDLCdigits[100]; 
    sprintf(timeCountIDandDLCdigits,"%10i\t%10i\t%04i-%02i-%02iT%02i:%02i:%02i.%06i\t%08X\t%3i\t%8i\t%06X\t%6i\t%3i\t%3i",
      rxCount,micros(),year(),month(),day(),hour(),minute(),second(),int(microsecondsPerSecond),ID,len,
      priority,PGN,PGN,DA,SA);
    Serial.print(timeCountIDandDLCdigits); 

    //Display the bytes  
    for (uint8_t i = 0; i<len;i++){ 
      char byteDigits[4]; 
      sprintf(byteDigits,"\t%02X",rxmsg.buf[i]);
      Serial.print(byteDigits); 
    }

    //interpret some messages on the fly
    if (PGN == 65265) //Cruise Control Vehicle Speed
    {
      Serial.print(F("\tCCVS"));
      //
      Serial.print(F("\tSpeed (mph):\t"));
      float SPN84 = word(rxmsg.buf[2],rxmsg.buf[1])/256.0; //Speed in km/h
      float speedMPH = SPN84 * 0.621271;
      if (SPN84 <  251)
        Serial.print(speedMPH);
      else if (SPN84 >= 255) Serial.print(F("Not Available"));
      else Serial.print(F("Out of Range"));
      
      Serial.print(F("\tBrake Switch:\t"));
      uint8_t SPN597 = (rxmsg.buf[3] & 0b00001100) >> 2;
      Serial.print(SPN597,BIN);
      if      (SPN597 == 0) Serial.print(F("\tBrake pedal released"));
      else if (SPN597 == 1) Serial.print(F("\tBrake pedal depressed"));
      else if (SPN597 == 2) Serial.print(F("\tError"));
      else                  Serial.print(F("\tNot Available"));
      
    }
    else if (PGN == 65248) //Vehicle Distance
    {
      Serial.print(F("\tVD"));

      Serial.print(F("\tTotal Vehicle Distance (miles):\t"));
      float SPN244 = (rxmsg.buf[7] << 24 | rxmsg.buf[6] << 16 | rxmsg.buf[5] << 8 | rxmsg.buf[4])*0.125; //Distance in km, least significant bit is 1/8 of a km.
      float SPN244miles = SPN244 * 0.621271;
      Serial.print(SPN244miles);
    }
    else if (PGN == 65217) //High Resolution Vehicle Distance
    {
      Serial.print(F("\tVDHR"));

      Serial.print(F("\tHigh Resolution Total Vehicle Distance (miles):\t"));
      float SPN917 = (rxmsg.buf[3] << 24 | rxmsg.buf[2] << 16 | rxmsg.buf[1] << 8 | rxmsg.buf[0])*0.005; //Distance in km, Least significant bit is 5 meters
      float SPN917miles = SPN917 * 0.621271;
      Serial.print(SPN917miles);
    }
    
    Serial.println(); //Go to the next line
  }
  
   if (LEDtoggleTimer >=500){
    LEDtoggleTimer = 0; //reset the timer
    ledState = !ledState; // Toggle values
    digitalWrite(LED_BUILTIN,ledState);
  }

  if (CANRXTimer > 200) digitalWrite(greenLEDpin,LOW); //Turn off the LED if no CAN traffic is present.
 
}

time_t getTeensy3Time(){
  return Teensy3Clock.get();
}



/*  code to process time sync messages from the serial port   */
unsigned long processSyncMessage() {
  unsigned long pctime = 0L;
  const unsigned long DEFAULT_TIME = 1357041600; // Jan 1 2013 

  if(Serial.find("T")) {
     pctime = Serial.parseInt();
     return pctime;
     if( pctime < DEFAULT_TIME) { // check the value is a valid time (greater than Jan 1 2013)
       pctime = 0L; // return 0 to indicate that the time is not valid
     }
  }
  return pctime;
}
