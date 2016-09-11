//Reading data from CAN and displaying it on a serial port
//Include the realtime clock functions inspired by the TimeTeensy3.ino example

//Include the CAN libraries for the Teensy microprocessor
#include <FlexCAN.h>
#include <TimeLib.h>

//Declare which pin is connected to the LED
//Use the Teensy Reference Card and the board schematics to determine the pin number
const int redLEDpin = 21;

//initiate the CAN library at 250kbps
FlexCAN CANbus(250000);

//Set up the CAN data structure
static CAN_message_t rxmsg;

//set up a counter for each received message
unsigned long int rxCount = 0;

//set up a timer to toggle the LEDs so the delay function isn't needed.
elapsedMillis LEDtoggleTimer;
elapsedMillis millisecondsPerSecond;


//Keep track of the LED state
boolean ledState = true;

//set up a variable to keep track of the timestamp
time_t previousTime = 0;

void setup() {
  // put your setup code here, to run once:

  // set the Time library to use Teensy 3.0's RTC to keep time
  setSyncProvider(getTeensy3Time);

  //declare the LED Pin to be the output
  pinMode(redLEDpin,OUTPUT);
  digitalWrite(redLEDpin,ledState); //Turn on the LED
  
  //start the CAN access
  CANbus.begin();
  rxmsg.timeout = 0;
  
  //try to wait for the Serial bus to come up for 1 second
  delay(1000);
  Serial.println(F("Teensy 3.2 CAN Receive Test."));
  
  //Set System Time
  if (timeStatus()!= timeSet) {
    Serial.println(F("Unable to sync with the RTC"));
  } 
  else {
    Serial.println(F("RTC has set the system time"));
  }
  
  //print a header
  Serial.print(F("     Count\t    micros\tYYYY-MM-DD HH:MM:SS.ms\t  CAN ID\tDLC"));
  for (uint8_t i = 1; i<9;i++){ //label the byte columns according to J1939
    char byteDigits[4]; //declare a byte display array
    sprintf(byteDigits,"\tB%i",i);
    Serial.print(byteDigits); 
  }

  //before entering the loop, set the previous time
  previousTime = now();
  //synchronize the millisecondPerSecond timer
  while (now() - previousTime < 1){
    millisecondsPerSecond = 0;
  }  
}

void loop() {
  // put your main code here, to run repeatedly:

  //check to see if the number of seconds has changed to reset the millisecond timer for each second
  if (now() - previousTime == 1){
    previousTime = now();
    millisecondsPerSecond = 0;
  }

  // Uncomment this to synchronize the RTC to your PC time.
  /*  if (Serial.available()) {
      time_t t = processSyncMessage();
      if (t != 0) {
        Teensy3Clock.set(t); // set the RTC
        setTime(t);
      }
    }
  */
  
  while(CANbus.read(rxmsg)){
    rxCount++;
    
    uint32_t ID = rxmsg.id;
    uint8_t len = rxmsg.len;
    
    char timeCountIDandDLCdigits[50]; 
    sprintf(timeCountIDandDLCdigits,"%10i\t%10i\t%04i-%02i-%02iT%02i:%02i:%02i.%03i\t%08X\t%1i",rxCount,micros(),year(),month(),day(),hour(),minute(),second(),int(millisecondsPerSecond),ID,len);
    Serial.print(timeCountIDandDLCdigits); 
      
    for (uint8_t i = 0; i<len;i++){ 
      char byteDigits[4]; 
      sprintf(byteDigits,"\t%02X",rxmsg.buf[i]);
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
