//Reading data from CAN and displaying it on a serial port
//Include the realtime clock functions inspired by the TimeTeensy3.ino example
//Add capability to send request messages


//Include the CAN libraries for the Teensy microprocessor
#include <FlexCAN.h>
#include <TimeLib.h>

char compID[100] = "TULSA*Teensy-Crash-EDR*Box*1";

const uint16_t PGNRequestList[28] = {
  65261, // Cruise Control/Vehicle Speed Setup
  65214, // Electronic Engine Controller 4
  65259, // Component Identification
  65242, // Software Identification
  65244, // Idle Operation
  65260, // Vehicle Identification
  65255, // Vehicle Hours
  65253, // Engine Hours, Revolutions
  65257, // Fuel Consumption (Liquid)
  65256, // Vehicle Direction/Speed
  65254, // Time/Date
  65211, // Trip Fan Information
  65210, // Trip Distance Information
  65209, // Trip Fuel Information (Liquid)
  65207, // Engine Speed/Load Factor Information
  65206, // Trip Vehicle Speed/Cruise Distance Information
  65205, // Trip Shutdown Information
  65204, // Trip Time Information 1
  65200, // Trip Time Information 2
  65250, // Transmission Configuration
  65253, // Engine Hours, Revolutions
  65203, // Fuel Information (Liquid)
  65201, // ECU History
  65168, // Engine Torque History
  64981, // Electronic Engine Controller 5
  64978, // ECU Performance
  64965, // ECU Identification Information
  65165  // Vehicle Electrical Power #2
};

uint8_t pgnIndex = 0;

//Declare which pin is connected to the LED
//Use the Teensy Reference Card and the board schematics to determine the pin number
const int redLEDpin = 21;

//initiate the CAN library at 250kbps
FlexCAN CANbus(250000);

//Set up the CAN data structure
static CAN_message_t rxmsg;
static CAN_message_t txmsg;

//set up a counter for each received message
unsigned long int rxCount = 0;

//set up a timer to toggle the LEDs so the delay function isn't needed.
elapsedMillis LEDtoggleTimer;
elapsedMillis millisecondsPerSecond;
elapsedMillis requestTimer;
elapsedMillis requestSendTimer;

const int millisBetweenRequests = 1000;

//Keep track of the LED state
boolean ledState = true;


void setup() {
  // put your setup code here, to run once:

  //declare the LED Pin to be the output
  pinMode(redLEDpin,OUTPUT);
  digitalWrite(redLEDpin,ledState); //Turn on the LED
  
  //start the CAN access
  CANbus.begin();
  rxmsg.timeout = 0;
  txmsg.timeout = 0;
  txmsg.len = 8;
  txmsg.id = 0x18EA00F6; //Reqest PGN
  txmsg.ext = 1;
  
  //try to wait for the Serial bus to come up for 1 second
  delay(1000);
  Serial.println(F("Teensy 3.2 CAN Receive Test with Component ID."));
  
  
  //print a header
  Serial.print(F("     Count\t    micros\t  CAN ID\tDLC"));
  for (uint8_t i = 1; i<9;i++){ //label the byte columns according to J1939
    char byteDigits[4]; //declare a byte display array
    sprintf(byteDigits,"\tB%i",i);
    Serial.print(byteDigits); 
  }

}

void loop() {
  // put your main code here, to run repeatedly:

  while(CANbus.read(rxmsg)){
    rxCount++;
    
    uint32_t ID = rxmsg.id;
    uint8_t len = rxmsg.len;
    
    char timeCountIDandDLCdigits[50]; 
    sprintf(timeCountIDandDLCdigits,"%10i\t%10i\t%08X\t%1i",rxCount,micros(),ID,len);
   // Serial.print(timeCountIDandDLCdigits); 
      
    for (uint8_t i = 0; i<len;i++){ 
      char byteDigits[4]; 
      sprintf(byteDigits,"\t%02X",rxmsg.buf[i]);
 //     Serial.print(byteDigits); 
    }
 //Serial.println();

    if ((ID & 0x00FF0000) == 0x00EA0000){
        Serial.print("Request Message Received");

        char timeCountIDandDLCdigits[50]; 
        sprintf(timeCountIDandDLCdigits,"%10i\t%10i\t%08X\t%1i",rxCount,micros(),ID,len);
        Serial.print(timeCountIDandDLCdigits); 
          
        for (uint8_t i = 0; i<len;i++){ 
          char byteDigits[4]; 
          sprintf(byteDigits,"\t%02X",rxmsg.buf[i]);
          Serial.print(byteDigits); 
        }
        Serial.println();
 
        if (rxmsg.buf[0] == 0xEB && rxmsg.buf[1] == 0xFE && requestSendTimer >1000){
          requestSendTimer = 0;
          sendComponentInfo(compID);
        }
        
    }
  }

    
  
  if (LEDtoggleTimer >=100){
    LEDtoggleTimer = 0; //reset the timer
    ledState = !ledState; // Toggle values
    digitalWrite(redLEDpin,ledState);
  }

  if (requestTimer >= millisBetweenRequests) {
    requestTimer = 0;
    uint16_t pgnToRequest = PGNRequestList[pgnIndex];
    pgnIndex++;
    if (pgnIndex > sizeof(PGNRequestList) ) pgnIndex = 0;

    txmsg.ext = 1;
    txmsg.id = 0x18EA00F9; //request PGN
    txmsg.buf[0] = (pgnToRequest & 0x0000FF);
    txmsg.buf[1] = (pgnToRequest & 0x00FF00) >> 8 ;
    txmsg.buf[2] = (pgnToRequest & 0xFF0000) >> 16;
    txmsg.len = 3;
    CANbus.write(txmsg);
  }
  

}


void sendComponentInfo(char id[100])
{
       txmsg.ext = 1;
       txmsg.len = 8;
  
       Serial.print("Received Request for Component ID. Sending  ");
       for (int i = 0; i < 35;i++) Serial.print(id[i]);
       Serial.println();
       byte transport0[8] = {32,35,0,5,0xFF,0xEB,0xFE,0};
       byte transport1[8] = {1,id[0],id[1],id[2],id[3],id[4],id[5],id[6]};
       byte transport2[8] = {2,id[7],id[8],id[9],id[10],id[11],id[12],id[13]};
       byte transport3[8] = {3,id[14],id[15],id[16],id[17],id[18],id[19],id[20]};
       byte transport4[8] = {4,id[21],id[22],id[23],id[24],id[25],id[26],id[27]};
       byte transport5[8] = {5,id[28],id[29],id[30],id[31],id[32],id[33],id[34]};
       txmsg.id = 0x18ECFF18;
       for (int i = 0;i<8;i++) txmsg.buf[i]=transport0[i];
       CANbus.write(txmsg);
       delay(3);
       txmsg.id = 0x18EBFF18;
       for (int i = 0;i<8;i++) txmsg.buf[i]=transport1[i];
       CANbus.write(txmsg);
       delay(3);
       for (int i = 0;i<8;i++) txmsg.buf[i]=transport2[i];
       CANbus.write(txmsg);
       delay(3);
       for (int i = 0;i<8;i++) txmsg.buf[i]=transport3[i];
       CANbus.write(txmsg);
       delay(3);
       for (int i = 0;i<8;i++) txmsg.buf[i]=transport4[i];
       CANbus.write(txmsg); 
       delay(3);
       for (int i = 0;i<8;i++) txmsg.buf[i]=transport5[i];
       if (CANbus.write(txmsg)) Serial.print("Sent Last Message");
       
}
