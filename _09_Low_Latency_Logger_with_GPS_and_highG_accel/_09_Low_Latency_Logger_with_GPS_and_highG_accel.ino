

/**
 * This program logs data to a binary file.  Functions are included
 * to convert the binary file to a csv text file.
 *
 * Samples are logged at regular intervals.  The maximum logging rate
 * depends on the quality of your SD card and the time required to
 * read sensor data.  This example has been tested at 500 Hz with
 * good SD card on an Uno.  4000 HZ is possible on a Due.
 *
 * If your SD card has a long write latency, it may be necessary to use
 * slower sample rates.  Using a Mega Arduino helps overcome latency
 * problems since 13 512 byte buffers will be used.
 *
 * Data is written to the file using a SD multiple block write command.
 */
// log file base name.  Must be five characters or less.
#define FILE_BASE_NAME "DATA"


 
#include <SPI.h>
#include <SdFat.h>
#include <SdFatUtil.h>
#include <FlexCAN.h>
#include <TimeLib.h>
#include <TinyGPS.h>
#include <SparkFun_ADXL345.h>         



#define numBaudRates 4
uint32_t baudRateList[numBaudRates] = {250000,500000,125000,1000000}; 
uint32_t baudrate = 250000; //default (may be overwritten with autobaud detection)

TimeElements tm;
time_t GPStime = 0;   
//------------------------------------------------------------------------------
// User data functions.  Modify these functions for your data items.
#include "UserDataType.h"  // Edit this include file to change data_t.

const int tzoffset = -5;   // Central Time

static CAN_message_t rxmsg,txmsg;

IntervalTimer oneSecondReset;
elapsedMicros microsecondsPerSecond;
elapsedMicros highGsampleTimer;

elapsedMillis buttonPressTimer;
elapsedMillis GPSsampleTimer;
elapsedMillis LEDblinkTimer;
elapsedMillis autobaudTimeout;

TinyGPS gps;

boolean gpsEncoded;

boolean LEDstate;


// accel chip select pin.
const uint8_t ACCEL_CS_PIN = 6;
//
// Digital pin to indicate an error, set to -1 if not used.
// The led blinks for fatal errors. The led goes on solid for SD write
// overrun errors and logging continues.
const uint8_t ERROR_LED_PIN = 21;

const uint8_t BUTTON_PIN = 17;

ADXL345 adxl = ADXL345(ACCEL_CS_PIN);   


void resetMicros() {
  microsecondsPerSecond = 0; //reset the timer
}

// Acquire a data record.
void acquireCANData(data_t* data) {
  data->timeStamp = now();
  data->usec = uint32_t(microsecondsPerSecond);
  data->type = 0;
  data->ID = ( 0x00 << 24 ) | rxmsg.id; // let the first byte in the ID data word to be 0 if this is GPS data.
  data->DLC = rxmsg.len;
  memset(data->dataField,0xFF,8);
  for (uint8_t i = 0; i < rxmsg.len; i++){
    data->dataField[i] = rxmsg.buf[i];  
  }
}



void acquireGPSData(data_t* data) {
  int GPSyear;
  byte GPSmonth, GPSday, GPShour, GPSminute, GPSsecond, GPShundredths;
  unsigned long GPSage;
  do{
    if (Serial1.available()) gps.encode(Serial1.read());
    gps.crack_datetime(&GPSyear, &GPSmonth, &GPSday, &GPShour, &GPSminute, &GPSsecond, &GPShundredths, &GPSage);
//    Serial.print(GPShour);
//    Serial.print(":");
//    Serial.print(GPSminute);
//    Serial.print(":");
//    Serial.print(GPSsecond);
//    Serial.print(" ");
//    Serial.print(GPSday);
//    Serial.print("-");
//    Serial.print(GPSmonth);
//    Serial.print("-");
//    Serial.print(GPSyear); 
//    Serial.println(); 
    tm.Second = GPSsecond;
    tm.Minute = GPSminute;
    tm.Hour = GPShour;
    tm.Day = GPSday;
    tm.Month = GPSmonth;
    tm.Year = GPSyear-1970;
    GPStime = makeTime(tm);
  } while (GPStime < 1471842557); //
  
  int32_t latitude;
  int32_t longitude;
  uint32_t fix_age;
  gps.get_position(&latitude,&longitude,&fix_age);
  data->timeStamp = now();
  data->usec = latitude; //Millionths of a degree
  data->type = 1;
  data->ID = GPStime; 
  data->DLC = longitude;
  data->dataField[0] = (0xFF00 & gps.speed())>>8;
  data->dataField[1] = 0xFF & gps.speed();
  data->dataField[2] = (0xFF00 & gps.course()) >> 8;
  data->dataField[3] = 0xFF & gps.course();
  data->dataField[4] = (0xFF00 & gps.altitude()) >> 8;
  data->dataField[5] = 0xFF & gps.altitude();
  data->dataField[6] = gps.hdop();
  data->dataField[7] = gps.satellites();
}

void acquireHighGData(data_t* data) {
  int x,y,z;   
  adxl.readAccel(&x, &y, &z);
  data->timeStamp = now();
  data->usec = uint32_t(microsecondsPerSecond);
  data->type = 2;
  data->ID = 0; 
  data->DLC = 0;
  data->dataField[0] = (0xFF00 & x)>>8;
  data->dataField[1] = 0xFF & x;
  data->dataField[2] = (0xFF00 & y) >> 8;
  data->dataField[3] = 0xFF & y;
  data->dataField[4] = (0xFF00 & z) >> 8;
  data->dataField[5] = 0xFF & z;
  data->dataField[6] = 0xFF;
  data->dataField[7] = 0xFF;
}


// Print a data record.
void printData(Print* pr, data_t* data) {
  int type = data->type;
  if (type == 0 || type ==1 ||type ==2){
    time_t recordTime = data->timeStamp;
    char timeString[100];
    sprintf(timeString,"%04d-%02d-%02d,%02d:%02d:%02d.%06d,",year(recordTime),month(recordTime),day(recordTime),hour(recordTime),minute(recordTime),second(recordTime),data->usec);
    pr->print(timeString);
    
    sprintf(timeString,"%10d.%06d",data->timeStamp,data->usec);
    pr->print(timeString);
    
    
    char IDString[12];
    sprintf(IDString,",%08X,",data->ID);
    pr->print(IDString);
    pr->print(data->DLC);
    for (int i = 0; i < 8; i++) {
      char entry[5];
      sprintf(entry,",%02X",data->dataField[i]);
      pr->print(entry);
    }
    pr->println();
  }
  
}

// Print data header.
void printHeader(Print* pr) {
  pr->print(F("YYYY-MM-DD HH:MM:SS.usec,"));
  pr->print(F("Unix timeStamp,"));
  pr->print(F("ID,"));
  pr->print(F("DLC"));
  for (uint8_t i = 0; i < 8; i++) {
    pr->print(F(",B"));
    pr->print(i);
  }
  pr->println();
}
//==============================================================================
// Start of configuration constants.
//==============================================================================
//Interval between data records in microseconds.
const uint32_t LOG_INTERVAL_USEC = 250;
//------------------------------------------------------------------------------
// Pin definitions.
//
// SD chip select pin.
const uint8_t SD_CS_PIN = 15;

//------------------------------------------------------------------------------
// File definitions.
//
// Maximum file size in blocks.
// The program creates a contiguous file with FILE_BLOCK_COUNT 512 byte blocks.
// This file is flash erased using special SD commands.  The file will be
// truncated if logging is stopped early.
//const uint32_t FILE_BLOCK_COUNT = 256000;
//const uint32_t FILE_BLOCK_COUNT = 2097152; //1 GB
const uint32_t FILE_BLOCK_COUNT = 4194304; //2 GB
//const uint32_t FILE_BLOCK_COUNT = 8388607; //4 GB - 512



//------------------------------------------------------------------------------
// Buffer definitions.
//
// The logger will use SdFat's buffer plus BUFFER_BLOCK_COUNT additional
// buffers.
//
#ifndef RAMEND
// Assume ARM. Use total of nine 512 byte buffers.
const uint8_t BUFFER_BLOCK_COUNT = 8;
//
#elif RAMEND < 0X8FF
#error Too little SRAM
//
#elif RAMEND < 0X10FF
// Use total of two 512 byte buffers.
const uint8_t BUFFER_BLOCK_COUNT = 1;
//
#elif RAMEND < 0X20FF
// Use total of five 512 byte buffers.
const uint8_t BUFFER_BLOCK_COUNT = 4;
//
#else  // RAMEND
// Use total of 13 512 byte buffers.
const uint8_t BUFFER_BLOCK_COUNT = 12;
#endif  // RAMEND
//==============================================================================
// End of configuration constants.
//==============================================================================
// Temporary log file.  Will be deleted if a reset or power failure occurs.
#define TMP_FILE_NAME "tmp_log.bin"

// Size of file base name.  Must not be larger than six.
const uint8_t BASE_NAME_SIZE = sizeof(FILE_BASE_NAME) - 1;



SdFat sd;
SdBaseFile binFile;

char binName[13] = FILE_BASE_NAME "000.bin";

// Number of data records in a block.
const uint16_t DATA_DIM = (512 - 4)/sizeof(data_t);

//Compute fill so block size is 512 bytes.  FILL_DIM may be zero.
const uint16_t FILL_DIM = 512 - 4 - DATA_DIM*sizeof(data_t);

struct block_t {
  uint16_t count;
  uint16_t overrun;
  data_t data[DATA_DIM];
  uint8_t fill[FILL_DIM];
};

/*
 * ------------------------------------------------------------------------------
 * Function: getBaudRate
 * 
 * returns one of the predefined CAN bauds rates
 * 
 * This function will always run until a CAN message is received. Therefore, the first messages may not be captured if
 * the program starts on a live bus. 
*/
uint32_t getBaudRate() {
  digitalWrite(LED_BUILTIN,HIGH);
  while (autobaudTimeout < 4000){
 
    processSetTimeUtility();
    for(uint8_t i=0;i<numBaudRates;i++){
      uint32_t baudrate = baudRateList[i];
      Serial.print(F("Trying Baudrate of "));
      Serial.println(baudrate);
      //Serial.println(F("Beginning test."));
      Can0.begin(baudrate);
      //The default filters exclude the extended IDs, so we have to set up CAN filters to allow those to pass.
      CAN_filter_t allPassFilter;
      allPassFilter.ext=1;
      for (uint8_t filterNum = 8; filterNum < 16;filterNum++){ //only use half the available filters for the extended IDs
        Can0.setFilter(allPassFilter,filterNum); 
      }
       delay(110);
      if(Can0.available()){
        Serial.print("Baudrate is confirmed to be ");
        Serial.println(baudrate);
        digitalWrite(LED_BUILTIN,LOW);
        return baudrate;
      }
      else{
       Can0.end();
       delay(100);
      }
      Serial.println(F("Trying again."));
     
    }   
  }
  digitalWrite(LED_BUILTIN,LOW);
  Serial.println(F("Setting Default Baudrate of 500000"));
  baudrate =  500000;
  Can0.begin(baudrate);
  return baudrate;
}


//------------------------------------------------------------------------------
/*
 * User provided date time callback function.
 * See SdFile::dateTimeCallback() for usage.
 */
void dateTime(uint16_t* FATdate, uint16_t* FATtime) {
  // User gets date and time from GPS or real-time
  // clock in real callback function

  // return date using FAT_DATE macro to format fields
  *FATdate = FAT_DATE(year(), month(), day());

  // return time using FAT_TIME macro to format fields
  *FATtime = FAT_TIME(hour(), minute(), second());
}


const uint8_t QUEUE_DIM = BUFFER_BLOCK_COUNT + 2;

block_t* emptyQueue[QUEUE_DIM];
uint8_t emptyHead;
uint8_t emptyTail;

block_t* fullQueue[QUEUE_DIM];
uint8_t fullHead;
uint8_t fullTail;

// Advance queue index.
inline uint8_t queueNext(uint8_t ht) {
  return ht < (QUEUE_DIM - 1) ? ht + 1 : 0;
}
//==============================================================================
// Error messages stored in flash.
#define error(msg) errorFlash(F(msg))
//------------------------------------------------------------------------------
void errorFlash(const __FlashStringHelper* msg) {
  sd.errorPrint(msg);
  fatalBlink();
}
//------------------------------------------------------------------------------
//
void fatalBlink() {
  while (true) {
    if (ERROR_LED_PIN >= 0) {
      digitalWrite(ERROR_LED_PIN, HIGH);
      delay(80);
      digitalWrite(ERROR_LED_PIN, LOW);
      delay(80);
      
    }
  }
}
//==============================================================================
// Convert binary file to csv file.
void binaryToCsv() {
  uint8_t lastPct = 0;
  block_t block;
  uint32_t t0 = millis();
  uint32_t syncCluster = 0;
  SdFile csvFile;
  char csvName[13];

  if (!binFile.isOpen()) {
    Serial.println();
    Serial.println(F("No current binary file"));
    return;
  }
  binFile.rewind();
  // Create a new csvFile.
  strcpy(csvName, binName);
  strcpy(&csvName[BASE_NAME_SIZE + 3], ".csv");

  if (!csvFile.open(csvName, O_WRITE | O_CREAT | O_TRUNC)) {
    error("open csvFile failed");
  }
  Serial.println();
  Serial.print(F("Writing: "));
  Serial.print(csvName);
  Serial.println(F(" - type any character to stop"));
  printHeader(&csvFile);
  uint32_t tPct = millis();
  while (!Serial.available() && binFile.read(&block, 512) == 512) {
     if (Serial1.available()) gps.encode(Serial1.read());
  
    uint16_t i;
    if (block.count == 0) {
      break;
    }
    if (block.overrun) {
      csvFile.print(F("OVERRUN,"));
      csvFile.println(block.overrun);
    }
    for (i = 0; i < block.count; i++) {
      printData(&csvFile, &block.data[i]);
    }
    if (csvFile.curCluster() != syncCluster) {
      csvFile.sync();
      syncCluster = csvFile.curCluster();
    }
    if ((millis() - tPct) > 1000) {
      uint8_t pct = binFile.curPosition()/(binFile.fileSize()/100);
      if (pct != lastPct) {
        tPct = millis();
        lastPct = pct;
        Serial.print(pct, DEC);
        Serial.println('%');
      }
    }
    if (Serial.available()) {
      break;
    }
  }
  csvFile.close();
  Serial.print(F("Done: "));
  Serial.print(0.001*(millis() - t0));
  Serial.println(F(" Seconds"));
}
//------------------------------------------------------------------------------
// read data file and check for overruns
void checkOverrun() {
  bool headerPrinted = false;
  block_t block;
  uint32_t bgnBlock, endBlock;
  uint32_t bn = 0;

  if (!binFile.isOpen()) {
    Serial.println();
    Serial.println(F("No current binary file"));
    return;
  }
  if (!binFile.contiguousRange(&bgnBlock, &endBlock)) {
    error("contiguousRange failed");
  }
  binFile.rewind();
  Serial.println();
  Serial.println(F("Checking overrun errors - type any character to stop"));
  while (binFile.read(&block, 512) == 512) {
    if (Serial1.available()) gps.encode(Serial1.read());
  
    if (block.count == 0) {
      break;
    }
    if (block.overrun) {
      if (!headerPrinted) {
        Serial.println();
        Serial.println(F("Overruns:"));
        Serial.println(F("fileBlockNumber,sdBlockNumber,overrunCount"));
        headerPrinted = true;
      }
      Serial.print(bn);
      Serial.print(',');
      Serial.print(bgnBlock + bn);
      Serial.print(',');
      Serial.println(block.overrun);
    }
    bn++;
  }
  if (!headerPrinted) {
    Serial.println(F("No errors found"));
  } else {
    Serial.println(F("Done"));
  }
}
//------------------------------------------------------------------------------
// dump data file to Serial
void dumpData() {
  block_t block;
  if (!binFile.isOpen()) {
    Serial.println();
    Serial.println(F("No current binary file"));
    return;
  }
  binFile.rewind();
  Serial.println();
  Serial.println(F("Type any character to stop"));
  delay(100);
  printHeader(&Serial);
  while (!Serial.available() && binFile.read(&block , 512) == 512) {
    if (Serial1.available()) gps.encode(Serial1.read());
  
    if (block.count == 0) {
      break;
    }
    if (block.overrun) {
      Serial.print(F("OVERRUN,"));
      Serial.println(block.overrun);
    }
    for (uint32_t i = 0; i < block.count; i++) {
      printData(&Serial, &block.data[i]);
    }
  }
  Serial.println(F("Done"));
}
//------------------------------------------------------------------------------
// log data
// max number of blocks to erase per erase call
uint32_t const ERASE_SIZE = 262144L;
void logData() {
  uint32_t bgnBlock, endBlock;
  digitalWrite(ERROR_LED_PIN,HIGH);
  // Allocate extra buffer space.
  block_t block[BUFFER_BLOCK_COUNT];
  block_t* curBlock = 0;
  Serial.println();

  // Find unused file name.
  if (BASE_NAME_SIZE > 5) {
    error("FILE_BASE_NAME too long");
  }
  while (sd.exists(binName)) {
    if (binName[BASE_NAME_SIZE + 2] != '9') {
      binName[BASE_NAME_SIZE + 2]++;
    }
    else {
      binName[BASE_NAME_SIZE + 2] = '0';
      if (binName[BASE_NAME_SIZE + 1] != '9') {
        binName[BASE_NAME_SIZE + 1]++;
      } else {
        binName[BASE_NAME_SIZE + 1] = '0';
        if (binName[BASE_NAME_SIZE] == '9') {
          error("Can't create file name");
        }
        binName[BASE_NAME_SIZE]++;
      }
    }
    if (binName[BASE_NAME_SIZE] == '9' & binName[BASE_NAME_SIZE+1] == '9' & binName[BASE_NAME_SIZE+2] == '9') {
        error("Can't create file name");
    }
  
  }
   
  // Delete old tmp file.
  if (sd.exists(TMP_FILE_NAME)) {
    Serial.println(F("Deleting tmp file"));
    if (!sd.remove(TMP_FILE_NAME)) {
      error("Can't remove tmp file");
    }
  }
  // Create new file.
  Serial.println(F("Creating new file"));
  binFile.close();
  if (!binFile.createContiguous(sd.vwd(),
                                TMP_FILE_NAME, 512 * FILE_BLOCK_COUNT)) {
    error("createContiguous failed");
  }
  // Get the address of the file on the SD.
  if (!binFile.contiguousRange(&bgnBlock, &endBlock)) {
    error("contiguousRange failed");
  }
  // Use SdFat's internal buffer.
  uint8_t* cache = (uint8_t*)sd.vol()->cacheClear();
  if (cache == 0) {
    error("cacheClear failed");
  }

  // Flash erase all data in the file.
  Serial.println(F("Erasing all data"));
  uint32_t bgnErase = bgnBlock;
  uint32_t endErase;
  while (bgnErase < endBlock) {
    endErase = bgnErase + ERASE_SIZE;
    if (endErase > endBlock) {
      endErase = endBlock;
    }
    if (!sd.card()->erase(bgnErase, endErase)) {
      error("erase failed");
    }
    bgnErase = endErase + 1;
  }
  // Start a multiple block write.
  if (!sd.card()->writeStart(bgnBlock, FILE_BLOCK_COUNT)) {
    error("writeBegin failed");
  }
  // Initialize queues.
  emptyHead = emptyTail = 0;
  fullHead = fullTail = 0;

  // Use SdFat buffer for one block.
  emptyQueue[emptyHead] = (block_t*)cache;
  emptyHead = queueNext(emptyHead);

  // Put rest of buffers in the empty queue.
  for (uint8_t i = 0; i < BUFFER_BLOCK_COUNT; i++) {
    emptyQueue[emptyHead] = &block[i];
    emptyHead = queueNext(emptyHead);
  }
  Serial.println(F("Logging - type any character to stop"));
  // Wait for Serial Idle.
  Serial.flush();
  delay(10);
  uint32_t bn = 0;
  uint32_t t0 = millis();
  uint32_t t1 = t0;
  uint32_t overrun = 0;
  uint32_t overrunTotal = 0;
  uint32_t count = 0;
  uint32_t maxLatency = 0;
  int32_t diff;
  // Start at a multiple of interval.
  uint32_t logTime = micros()/LOG_INTERVAL_USEC + 1;
  logTime *= LOG_INTERVAL_USEC;
  bool closeFile = false;
  //digitalWrite(ERROR_LED_PIN,HIGH);
  while (1) {
     if (Serial1.available()) gps.encode(Serial1.read());
  
    // Time for next data record.
    //logTime += LOG_INTERVAL_USEC;
    if (Serial.available() || (!digitalRead(BUTTON_PIN) && buttonPressTimer>100) ) {
      closeFile = true;
      buttonPressTimer = 0;
    }

    if (closeFile) {
      Serial.println(F("Closing Temp Buffer File."));
     // Serial.print("curBlock: ");
     // Serial.println(curBlock);
      Serial.print("curBlock->count: ");
      Serial.println(curBlock->count);
      
      
      if (curBlock != 0 && curBlock->count >= 0) {
        // Put buffer in full queue.
        fullQueue[fullHead] = curBlock;
        fullHead = queueNext(fullHead);
        Serial.print(F("Updated fullHead to "));
        Serial.println(fullHead);
        curBlock = 0;
      }
    } 
    else {
      if (curBlock == 0 && emptyTail != emptyHead) {
        //Serial.println(F("curBloc == 0 && emptyTail != emptyHead"));
        curBlock = emptyQueue[emptyTail];
        emptyTail = queueNext(emptyTail);
        curBlock->count = 0;
        curBlock->overrun = overrun;
        overrun = 0;
      }
//      do {
//        diff = logTime - micros();
//      } while(diff > 0);
//      if (diff < -10) {
//        error("LOG_INTERVAL_USEC too small");
//      }
      if (curBlock == 0) {
        overrun++;
        Serial.print(F("Overrun: "));
        Serial.println(overrun);
      } 
      else {
        if (Can0.read(rxmsg)) acquireCANData(&curBlock->data[curBlock->count++]);
        if (Serial1.available()) {
          char q = Serial1.read();
          //Serial.print(q);
          gpsEncoded = gps.encode(q);
        }
        
        if (GPSsampleTimer >= 200){
          GPSsampleTimer = 0; 
          acquireGPSData(&curBlock->data[curBlock->count++]);
        }

        if (highGsampleTimer >= 312){ //mircoseconds for 3200 Hz
          highGsampleTimer = 0;
          SPI.setDataMode(SPI_MODE3);
          digitalWrite(SD_CS_PIN,HIGH);
          acquireHighGData(&curBlock->data[curBlock->count++]);
          digitalWrite(SD_CS_PIN,LOW);
          SPI.setDataMode(SPI_MODE0);
          
        }
        
        if (LEDblinkTimer >= 500){
          LEDblinkTimer = 0; 
          LEDstate = !LEDstate;
          digitalWrite(ERROR_LED_PIN,LEDstate);
        }

        
         
        if (curBlock->count >= DATA_DIM) {
          //Serial.println(F("curBlock->count >= DATA_DIM"));
          fullQueue[fullHead] = curBlock;
          fullHead = queueNext(fullHead);
          curBlock = 0;
        }
      }
    }

    if (fullHead == fullTail) {
      //Serial.println(F("fullHead == fullTail"));
      // Exit loop if done.
      if (closeFile) {
        break;
      }
    } else if (!sd.card()->isBusy()) {
      //Serial.println(F("!sd.card()->isBusy()"));
      // Get address of block to write.
      block_t* pBlock = fullQueue[fullTail];
      fullTail = queueNext(fullTail);
      // Write block to SD.
      uint32_t usec = micros();
      if (!sd.card()->writeData((uint8_t*)pBlock)) {
        error(F("write data failed"));
      }
      usec = micros() - usec;
      t1 = millis();
      if (usec > maxLatency) {
        maxLatency = usec;
      }
      count += pBlock->count;

      // Add overruns and possibly light LED.
      if (pBlock->overrun) {
        overrunTotal += pBlock->overrun;
        if (ERROR_LED_PIN >= 0) {
          digitalWrite(ERROR_LED_PIN, HIGH);
        }
      }
      // Move block to empty queue.
      emptyQueue[emptyHead] = pBlock;
      emptyHead = queueNext(emptyHead);
      bn++;
      if (bn == FILE_BLOCK_COUNT) {
         Serial.println(F("bn == FILE_BLOCK_COUNT"));
        // File full so stop
        closeFile = true;
        break;
      }
    }
  }
  if (!sd.card()->writeStop()) {
    error("writeStop failed");
  }
  digitalWrite(ERROR_LED_PIN, LOW);
  // Truncate file if recording stopped early.
  if (bn != FILE_BLOCK_COUNT) {
    Serial.println(F("Truncating file"));
    Serial.print(F("uint32_t(512 * bn)"));
    Serial.println(uint32_t(512 * bn));
    if (!binFile.truncate(uint32_t(512 * bn))) {
      error("Can't truncate file");
    }
  }
  if (!binFile.rename(sd.vwd(), binName)) {
    error("Can't rename file");
  }
  Serial.print(F("File renamed: "));
  Serial.println(binName);
  Serial.print(F("Max block write usec: "));
  Serial.println(maxLatency);
  Serial.print(F("Record time sec: "));
  Serial.println(0.001*(t1 - t0), 3);
  Serial.print(F("Sample count: "));
  Serial.println(count);
  Serial.print(F("Samples/sec: "));
  Serial.println((1000.0)*count/(t1-t0));
  Serial.print(F("Overruns: "));
  Serial.println(overrunTotal);
  Serial.println(F("Done"));
}
//------------------------------------------------------------------------------

time_t getTeensy3Time()
{
  return Teensy3Clock.get();
}

void setup(void) {
  Serial.begin(9600);
  digitalWrite(ERROR_LED_PIN,HIGH);
  delay(1000);
  digitalWrite(ERROR_LED_PIN,LOW);
 
  
  pinMode(BUTTON_PIN,INPUT_PULLUP);

  pinMode(SD_CS_PIN,OUTPUT);
  digitalWrite(SD_CS_PIN,HIGH);
  //SPI.setDataMode(SPI_MODE3);
  adxl.powerOn(); 
  adxl.setRate(3200);
  adxl.setSpiBit(0);                              
  delay(100);
  
  adxl.printAllRegister();
  delay(1);
   
  pinMode(ERROR_LED_PIN, OUTPUT);
 
   
  setSyncProvider(getTeensy3Time);
  if (timeStatus()!= timeSet) {
    Serial.println("Unable to sync with the RTC");
  } else {
    Serial.println("RTC has set the system time");
  }

  Serial.print("Starting GPS... ");
  //tft.println("Starting GPS");
  Serial1.begin(9600);
  delay(300);
  Serial1.println("$PMTK251,57600*2C"); //Set Baud Rate to 57600
  delay(100);
  Serial1.flush();
  Serial1.end();
  Serial.println("Setting GPS to 57600 baud... ");
  delay(300);
  Serial1.begin(57600);
  Serial1.println("$PMTK251,57600*2C"); //Set Baud Rate to 57600

  Serial.println("Setting GPS to update at 5 Hz... ");
  Serial1.println("$PMTK220,200*2C"); //update at 5 Hz
  delay(100);
  Serial1.println("$PMTK300,200,0,0,0,0*2F"); //position fix update to 5 Hz
  for (int i = 0; i < 100; i++) {
    if (Serial1.available()) Serial.write(Serial1.read());
  }
  Serial.println("\nDone.");
  
  setSyncProvider(getTeensy3Time);
  if (timeStatus()!= timeSet) {
    Serial.println("Unable to sync with the RTC");
  } else {
    Serial.println("RTC has set the system time");
  }
  setSyncInterval(1);
  char timeString[32];
  sprintf(timeString,"%04d-%02d-%02d %02d:%02d:%02d.%06d",year(),month(),day(),hour(),minute(),second(),uint32_t(microsecondsPerSecond));
  Serial.println(timeString);
  
  baudrate = getBaudRate(); //comment this line out to accept the default
  

  SdFile baudFile;
  baudFile.open("baudRate.txt", O_RDWR | O_CREAT | O_AT_END);
  baudFile.println(timeString);
  baudFile.close();
  
  Serial.println("Wrote Baudrate to a file.");
  
 //  while (now() - previousTime < 1) resetMicros();
//  oneSecondReset.begin(resetMicros,1000000);
//  
  sprintf(timeString,"%04d-%02d-%02d %02d:%02d:%02d.%06d",year(),month(),day(),hour(),minute(),second(),uint32_t(microsecondsPerSecond));
  Serial.println(timeString);
  
  Serial.print(F("FreeRam: "));
  Serial.println(FreeRam());
  Serial.print(F("Records/block: "));
  Serial.println(DATA_DIM);
  if (sizeof(block_t) != 512) {
    error("Invalid block size");
  }
  // initialize file system.
  if (!sd.begin(SD_CS_PIN, SPI_FULL_SPEED)) {
    sd.initErrorPrint();
    fatalBlink();
  }
  // set date time callback function
  SdFile::dateTimeCallback(dateTime);
 
  truncateTempfiles();

  
  
 

//  logData(); //uncomment to automatically start logging. Otherwise use the button
}
//------------------------------------------------------------------------------
void loop(void) {
  if (ERROR_LED_PIN >= 0) {
    digitalWrite(ERROR_LED_PIN, LOW);
  }
  
  // discard any input
  while (Serial.read() >= 0) {}
  
  Serial.println();
  Serial.println(F("type:"));
  Serial.println(F("c - convert file to csv"));
  Serial.println(F("d - dump data to Serial"));
  Serial.println(F("e - overrun error details"));
  Serial.println(F("r - record data"));

  while(!Serial.available() && digitalRead(BUTTON_PIN) )  if (Serial1.available()) gps.encode(Serial1.read());
  
  buttonPressTimer = 0;
  delay(50); //debounce
  char c;
  if (Serial.available()) c = tolower(Serial.read());
  while (Serial.read() >= 0);
  if (!digitalRead(BUTTON_PIN)) c = 'r';
  while (!digitalRead(BUTTON_PIN)){
    if (buttonPressTimer > 2000){
      c='c';
      break;
    }
  }
  
  if (c == 'c') {
    analogWrite(ERROR_LED_PIN,64);
    binaryToCsv();
    analogWrite(ERROR_LED_PIN,0);
  } else if (c == 'd') {
    dumpData();
  } else if (c == 'e') {
    checkOverrun();
  } else if (c == 'r') {
    logData();
  }  else if (!digitalRead(BUTTON_PIN)) {
     delay(500);
     if (!digitalRead(BUTTON_PIN)) logData();
  } else {
    Serial.println(F("Invalid entry"));
  }
  
  digitalWrite(ERROR_LED_PIN, LOW);
  
  while (!digitalRead(BUTTON_PIN)){
     if (Serial1.available()) gps.encode(Serial1.read());
  
    if (ERROR_LED_PIN >= 0) {
      digitalWrite(ERROR_LED_PIN, LOW);
    }
  }//Wait to release the button;
}

void truncateTempfiles(){
  digitalWrite(ERROR_LED_PIN,HIGH);
  if (sd.exists(TMP_FILE_NAME)) {
    Serial.println("Found exsiting temp file."); 
    
    SdBaseFile tempFile;
 
    tempFile.open(TMP_FILE_NAME, O_RDWR);
    
    byte someBytes[4];
    bool stillSearching = true;
    uint32_t highIndex = FILE_BLOCK_COUNT;
    uint32_t lowIndex = 0;
    
    tempFile.seekSet(0);
    for (int j = 0;j<4;j++){
      someBytes[j] = tempFile.read();
    }
    if (someBytes[0]==0xFF & someBytes[1]==0xFF & someBytes[2]==0xFF & someBytes[3]==0xFF){ // End is lower 
      Serial.println("Zero length temp file encountered. Ignoring.");
      if (!sd.remove(TMP_FILE_NAME)) {
        error("Can't remove tmp file");
      }
      return;
    }
    
    uint32_t fileIndex;
    while (stillSearching){ // Use bisection search to find the end of the file.
          fileIndex = (highIndex + lowIndex)/2;
          tempFile.seekSet(fileIndex*512L);
          for (int j = 0;j<4;j++){
            someBytes[j] = tempFile.read();
          }
          
          if (someBytes[0]==0xFF & someBytes[1]==0xFF & someBytes[2]==0xFF & someBytes[3]==0xFF){ // End is lower 
            highIndex = highIndex - (highIndex - lowIndex)/2;
          }
          else{ // end is higher
            lowIndex = lowIndex + (highIndex - lowIndex)/2;
          }
          if (highIndex - lowIndex < 2) stillSearching = false;
    }
    Serial.println("Trunating File.");
    if (!tempFile.truncate(uint32_t(512L * fileIndex))){
      error("Can't truncate file");
    }
    Serial.print("Truncated temp file to ");
    Serial.println( uint32_t(512L * fileIndex));
      
 
  // Find unused file name.
  if (BASE_NAME_SIZE > 5) {
    error("FILE_BASE_NAME too long");
  }
  while (sd.exists(binName)) {
    if (binName[BASE_NAME_SIZE + 2] != '9') {
      binName[BASE_NAME_SIZE + 2]++;
    }
    else {
      binName[BASE_NAME_SIZE + 2] = '0';
      if (binName[BASE_NAME_SIZE + 1] != '9') {
        binName[BASE_NAME_SIZE + 1]++;
      }
      else {
        binName[BASE_NAME_SIZE+1] = '0';
        binName[BASE_NAME_SIZE]++;
      }
    }
    
   if (binName[BASE_NAME_SIZE] == '9' & binName[BASE_NAME_SIZE+1] == '9' & binName[BASE_NAME_SIZE+2] == '9') {
        error("Can't create file name");
    }
  }
  Serial.print("Created new filename of ");
  Serial.println(binName);
  
   
  if (!tempFile.rename(sd.vwd(), binName)) {
    error("Can't rename file");
  }
  
  Serial.print(F("File renamed: "));
  Serial.println(binName);

  tempFile.close();

  }

}


elapsedMillis displayCounter;

void processSetTimeUtility(){
//  if (gps.encode(Serial1.read())) { // process gps messages
//      // when TinyGPS reports new data...
//      unsigned long age;
//      int Year;
//      byte Month, Day, Hour, Minute, Second;
//      gps.crack_datetime(&Year, &Month, &Day, &Hour, &Minute, &Second, NULL, &age);
//      if (age < 500) {
//        // set the Time to the latest GPS reading
//        setTime(Hour, Minute, Second, Day, Month, Year);
//        adjustTime(tzoffset * SECS_PER_HOUR);
//        Teensy3Clock.set(now());
//      }
//    }
    
    if (Serial.available()) {
    time_t t = processSyncMessage();
    if (t != 0) {
      Teensy3Clock.set(t); // set the RTC
      setTime(t);
    }
  }
  
  if (displayCounter >=1000){
    displayCounter = 0;
    char timeStamp[35];
    sprintf(timeStamp,"%04d-%02d-%02d %02d:%02d:%02d",year(),month(),day(),hour(),minute(),second());
   // Serial.println(timeStamp);
  }  
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
  return pctime;
}

