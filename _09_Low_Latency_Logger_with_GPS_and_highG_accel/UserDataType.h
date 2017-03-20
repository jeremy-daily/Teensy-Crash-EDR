#ifndef UserDataType_h
#define UserDataType_h
struct data_t {
  uint16_t type;
  uint16_t DLC;
  time_t timeStamp;
  uint32_t usec;
  uint32_t ID;
  uint8_t dataField[8];
  
};
#endif  // UserDataType_h
