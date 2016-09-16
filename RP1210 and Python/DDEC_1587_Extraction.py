import struct
import sys
from ctypes import *
from ctypes.wintypes import HWND
from array import *
import time 

import math

#-----------------------------------------------------------------------------------------------------
# RP1210B   RP1210_SendCommand Defines (From RP1210B Document)
#-----------------------------------------------------------------------------------------------------

RP1210_Reset_Device                               =                   0
RP1210_Set_All_Filters_States_to_Pass             =                   3
RP1210_Set_Message_Filtering_For_J1939            =                   4
RP1210_Set_Message_Filtering_For_CAN              =                   5
RP1210_Set_Message_Filtering_For_J1708            =                   7
RP1210_Set_Message_Filtering_For_J1850            =                   8
RP1210_Set_Message_Filtering_For_ISO15765         =                   9
RP1210_Generic_Driver_Command                     =                  14
RP1210_Set_J1708_Mode                             =                  15
RP1210_Echo_Transmitted_Messages                  =                  16
RP1210_Set_All_Filters_States_to_Discard          =                  17
RP1210_Set_Message_Receive                        =                  18
RP1210_Protect_J1939_Address                      =                  19
RP1210_Set_Broadcast_For_J1708                    =                  20
RP1210_Set_Broadcast_For_CAN                      =                  21
RP1210_Set_Broadcast_For_J1939                    =                  22
RP1210_Set_Broadcast_For_J1850                    =                  23
RP1210_Set_J1708_Filter_Type                      =                  24
RP1210_Set_J1939_Filter_Type                      =                  25
RP1210_Set_CAN_Filter_Type                        =                  26
RP1210_Set_J1939_Interpacket_Time                 =                  27
RP1210_SetMaxErrorMsgSize                         =                  28
RP1210_Disallow_Further_Connections               =                  29
RP1210_Set_J1850_Filter_Type                      =                  30
RP1210_Release_J1939_Address                      =                  31
RP1210_Set_ISO15765_Filter_Type                   =                  32
RP1210_Set_Broadcast_For_ISO15765                 =                  33
RP1210_Set_ISO15765_Flow_Control                  =                  34
RP1210_Clear_ISO15765_Flow_Control                =                  35
RP1210_Set_ISO15765_Link_Type                     =                  36
RP1210_Set_J1939_Baud                             =                  37
RP1210_Set_ISO15765_Baud                          =                  38
RP1210_Set_BlockTimeout                           =                 215
RP1210_Set_J1708_Baud                             =                 305

#-----------------------------------------------------------------------------------------------------
# RP1210B Constants - Check RP1210B document for any updates.
#-----------------------------------------------------------------------------------------------------

CONNECTED                                         =             1  # Connection state = Connected 
NOT_CONNECTED                                     =            -1  # Connection state = Disconnected

FILTER_PASS_NONE                                  =             0  # Filter state = DISCARD ALL MESSAGES
FILTER_PASS_SOME                                  =             1  # Filter state = PASS SOME (some filters)
FILTER_PASS_ALL                                   =             2  # Filter state = PASS ALL

NULL_WINDOW                                       =             0  # Windows 3.1 is no longer supported.

BLOCKING_IO                                       =             1  # For Blocking calls to send/read.
NON_BLOCKING_IO                                   =             0  # For Non-Blocking calls to send/read.
BLOCK_INFINITE                                    =             0  # For Non-Blocking calls to send/read.

BLOCK_UNTIL_DONE                                  =             0  # J1939 Address claim, wait until done
RETURN_BEFORE_COMPLETION                          =             2  # J1939 Address claim, don't wait

CONVERTED_MODE                                    =             1  # J1708 RP1210Mode="Converted"
RAW_MODE                                          =             0  # J1708 RP1210Mode="Raw"

MAX_J1708_MESSAGE_LENGTH                          =           508  # Maximum size of J1708 message (+1)
MAX_J1939_MESSAGE_LENGTH                          =          1796  # Maximum size of J1939 message (+1)
MAX_ISO15765_MESSAGE_LENGTH                       =          4108  # Maximum size of ISO15765 message (+1)

ECHO_OFF                                          =          0x00  # EchoMode
ECHO_ON                                           =          0x01  # EchoMode

RECEIVE_ON                                        =          0x01  # Set Message Receive
RECEIVE_OFF                                       =          0x00  # Set Message Receive

ADD_LIST                                          =          0x01  # Add a message to the list.
VIEW_B_LIST                                       =          0x02  # View an entry in the list.
DESTROY_LIST                                      =          0x03  # Remove all entries in the list.
REMOVE_ENTRY                                      =          0x04  # Remove a specific entry from the list.
LIST_LENGTH                                       =          0x05  # Returns number of items in list.

FILTER_PGN                                        =          0x01  # Setting of J1939 filters
FILTER_PRIORITY                                   =          0x02  # Setting of J1939 filters
FILTER_SOURCE                                     =          0x04  # Setting of J1939 filters
FILTER_DESTINATION                                =          0x08  # Setting of J1939 filters
FILTER_INCLUSIVE                                  =          0x00  # FilterMode
FILTER_EXCLUSIVE                                  =          0x01  # FilterMode

SILENT_J1939_CLAIM                                =          0x00  # Claim J1939 Address
PASS_J1939_CLAIM_MESSAGES                         =          0x01  # Claim J1939 Address

CHANGE_BAUD_NOW                                   =          0x00  # Change Baud
MSG_FIRST_CHANGE_BAUD                             =          0x01  # Change Baud
RP1210_BAUD_9600                                  =          0x00  # Change Baud
RP1210_BAUD_19200                                 =          0x01  # Change Baud
RP1210_BAUD_38400                                 =          0x02  # Change Baud
RP1210_BAUD_57600                                 =          0x03  # Change Baud
RP1210_BAUD_125k                                  =          0x04  # Change Baud
RP1210_BAUD_250k                                  =          0x05  # Change Baud
RP1210_BAUD_500k                                  =          0x06  # Change Baud
RP1210_BAUD_1000k                                 =          0x07  # Change Baud

STANDARD_CAN                                      =          0x00  # Filters
EXTENDED_CAN                                      =          0x01  # Filters

STANDARD_CAN_ISO15765_EXTENDED                    =          0x02  # 11-bit with ISO15765 extended address
EXTENDED_CAN_ISO15765_EXTENDED                    =          0x03  # 29-bit with ISO15765 extended address
STANDARD_MIXED_CAN_ISO15765                       =          0x04  # 11-bit identifier with mixed addressing
ISO15765_ACTUAL_MESSAGE                           =          0x00  # ISO15765 ReadMessage - type of data
ISO15765_CONFIRM                                  =          0x01  # ISO15765 ReadMessage - type of data
ISO15765_FF_INDICATION                            =          0x02  # ISO15765 ReadMessage - type of data

LINKTYPE_GENERIC_CAN                              =          0x00  # Set_ISO15765_Link_Type argument
LINKTYPE_J1939_ISO15765_2_ANNEX_A                 =          0x01  # Set_ISO15765_Link_Type argument
LINKTYPE_J1939_ISO15765_3                         =          0x02  # Set_ISO15765_Link_Type argument

#-----------------------------------------------------------------------------------------------------
# Local #define Definitions
#-----------------------------------------------------------------------------------------------------

J1939_GLOBAL_ADDRESS                              =           255
J1939_OFFBOARD_DIAGNOSTICS_TOOL_1                 =           249
J1587_OFFBOARD_DIAGNOSTICS_TOOL_1                 =           172

# ----------------------------------------------------------------------------------------------------
# PrintRP1210Error Dictionary data Structure
# 
RP1210Errors = {
    0  : "NO_ERRORS"                                        ,
    128: "ERR_DLL_NOT_INITIALIZED"                          ,
    129: "ERR_INVALID_CLIENT_ID"                            ,
    130: "ERR_CLIENT_ALREADY_CONNECTED"                     ,
    131: "ERR_CLIENT_AREA_FULL"                             ,
    132: "ERR_FREE_MEMORY"                                  ,
    133: "ERR_NOT_ENOUGH_MEMORY"                            ,
    134: "ERR_INVALID_DEVICE"                               ,
    135: "ERR_DEVICE_IN_USE"                                ,
    136: "ERR_INVALID_PROTOCOL"                             ,
    137: "ERR_TX_QUEUE_FULL"                                ,
    138: "ERR_TX_QUEUE_CORRUPT"                             ,
    139: "ERR_RX_QUEUE_FULL"                                ,
    140: "ERR_RX_QUEUE_CORRUPT"                             ,
    141: "ERR_MESSAGE_TOO_LONG"                             ,
    142: "ERR_HARDWARE_NOT_RESPONDING"                      ,
    143: "ERR_COMMAND_NOT_SUPPORTED"                        ,
    144: "ERR_INVALID_COMMAND"                              ,
    145: "ERR_TXMESSAGE_STATUS"                             ,
    146: "ERR_ADDRESS_CLAIM_FAILED"                         ,
    147: "ERR_CANNOT_SET_PRIORITY"                          ,
    148: "ERR_CLIENT_DISCONNECTED"                          ,
    149: "ERR_CONNECT_NOT_ALLOWED"                          ,
    150: "ERR_CHANGE_MODE_FAILED"                           ,
    151: "ERR_BUS_OFF"                                      ,
    152: "ERR_COULD_NOT_TX_ADDRESS_CLAIMED"                 ,
    153: "ERR_ADDRESS_LOST"                                 ,
    154: "ERR_CODE_NOT_FOUND"                               ,
    155: "ERR_BLOCK_NOT_ALLOWED"                            ,
    156: "ERR_MULTIPLE_CLIENTS_CONNECTED"                   ,
    157: "ERR_ADDRESS_NEVER_CLAIMED"                        ,
    158: "ERR_WINDOW_HANDLE_REQUIRED"                       ,
    159: "ERR_MESSAGE_NOT_SENT"                             ,
    160: "ERR_MAX_NOTIFY_EXCEEDED"                          ,
    161: "ERR_MAX_FILTERS_EXCEEDED"                         ,
    162: "ERR_HARDWARE_STATUS_CHANGE"                       ,
    202: "ERR_INI_FILE_NOT_IN_WIN_DIR"                      ,
    204: "ERR_INI_SECTION_NOT_FOUND"                        ,
    205: "ERR_INI_KEY_NOT_FOUND"                            ,
    206: "ERR_INVALID_KEY_STRING"                           ,
    207: "ERR_DEVICE_NOT_SUPPORTED"                         ,
    208: "ERR_INVALID_PORT_PARAM"                           ,
    213: "ERR_COMMAND_TIMED_OUT"                            ,
    220: "ERR_OS_NOT_SUPPORTED"                             ,
    222: "ERR_COMMAND_QUEUE_IS_FULL"                        ,
    224: "ERR_CANNOT_SET_CAN_BAUDRATE"                      ,
    225: "ERR_CANNOT_CLAIM_BROADCAST_ADDRESS"               ,
    226: "ERR_OUT_OF_ADDRESS_RESOURCES"                     ,
    227: "ERR_ADDRESS_RELEASE_FAILED"                       ,
    230: "ERR_COMM_DEVICE_IN_USE"                           ,
    441: "ERR_DATA_LINK_CONFLICT"                           ,
    453: "ERR_ADAPTER_NOT_RESPONDING"                       ,
    454: "ERR_CAN_BAUD_SET_NONSTANDARD"                     ,
    455: "ERR_MULTIPLE_CONNECTIONS_NOT_ALLOWED_NOW"         ,
    456: "ERR_J1708_BAUD_SET_NONSTANDARD"                   ,
    457: "ERR_J1939_BAUD_SET_NONSTANDARD"                   }

#
#
#********************************************************************************
# Global Variables
#********************************************************************************
#
#

#
# RP1210_ReadVersion
#
fpchDLLMajorVersion = c_char()
fpchDLLMinorVersion = c_char()
fpchAPIMajorVersion = c_char()
fpchAPIMinorVersion = c_char()

#
# RP1210_ReadDetailedVersion
#
chAPIVersionInfo    = (c_char*17)()
chDLLVersionInfo    = (c_char*17)()
chFWVersionInfo     = (c_char*17)()
szAPI               = (c_char)(100)
szDLL               = (c_char)(100)
szFW                = (c_char)(100)

#
# Connection Related Variables
#

iAdapterID          = c_short() 
szDLLName           = (c_char*100)()

iProtocolID         = c_short()
szProtocolName      = (c_char*100)()

iDeviceID           = c_short()

nClientID           = c_short()
nRetVal             = c_short()

ucTxRxBuffer        = (c_char*2000)()

    
#-----------------------------------------------------------------------------------------------------
# Print a sent J1708/J1587 message.
#-----------------------------------------------------------------------------------------------------
    
def PrintTxJ1708Message( nLength, ucTxRxBuffer ) :
    '''This function prints a transmitted J1708/J1587 message to the screen.'''
        
    ucPRI      = c_char(0)
    ucMID      = c_char(0)
    ucPID      = c_char(0)
    nDataBytes = c_short(0)

    ucPRI      = struct.unpack( 'B', ucTxRxBuffer[0]   )[0]
    ucMID      = struct.unpack( 'B', ucTxRxBuffer[1]   )[0]
    ucPID      = struct.unpack( 'B', ucTxRxBuffer[2]   )[0]

    nDataBytes = nLength - 3

    print( "Tx J1708 PRI=[%d]" % ucPRI         , end=" " )
    print(          "MID=[%d]" % ucMID         , end=" " )
    print(          "PID=[%d]" % ucPID         , end=" " )
    print(          "LEN=[%d]" % nDataBytes              )
    print( ""                                  , end="\t")
    print( "DATA-HEX"                          , end=""  )

    for ucByte in ucTxRxBuffer[3:nLength] :
         print("[%02X]" % ucByte, end="" )
    #for

    print("")



#-----------------------------------------------------------------------------------------------------
# Print a received J1939 message.
#-----------------------------------------------------------------------------------------------------

def PrintRxJ1939Message( nRetVal, ucTxRxBuffer, display='no' ) :
    '''This function prints a received J1939 message to the screen.'''

    iTS        = c_int  (0)

    ucPGN      = (c_char*4)()
    iPGN       = c_int  (0)

    ucHowPri   = c_char (0)
    iHowPri    = c_int  (0)

    ucSRC      = c_char (0)
    ucDST      = c_char (0)
    iSRC       = c_int  (0)
    iDST       = c_int  (0)

    nDataBytes = c_short(0)

    iTS        = int(struct.unpack('>L',(ucTxRxBuffer[0]+ucTxRxBuffer[1]+ucTxRxBuffer[2]+ucTxRxBuffer[3]))[0])

    ucPGN[0]   = ucTxRxBuffer[4]
    ucPGN[1]   = ucTxRxBuffer[5]
    ucPGN[2]   = ucTxRxBuffer[6]
    ucPGN[3]   = 0

    iPGN       = c_int( struct.unpack( '<L',(ucPGN[0]+ucPGN[1]+ucPGN[2]+ucPGN[3]))[0])

    ucHowPri   = c_char( struct.unpack( 'B', ucTxRxBuffer[7] )[0])
    iHowPri    = bytes( ucHowPri )[0]

    maskedHow  = ( iHowPri & 0x80 ) >> 7
    maskedPri  = ( iHowPri & 0x07 )

    ucSRC      = c_char( struct.unpack( 'B', ucTxRxBuffer[8]   )[0])
    ucDST      = c_char( struct.unpack( 'B', ucTxRxBuffer[9]   )[0])

    iSRC       = bytes( ucSRC )[0]
    iDST       = bytes( ucDST )[0]

    nDataBytes = nRetVal - 10

    if nDataBytes <= 8 :
        szHow = "N/A"
    else :
        if 1 == maskedHow :
            szHow = "BAM"
        else :
            szHow = "RTS"
        #if
    #if
    if display=='yes':
        print( "Rx,J1939,TS=,%d"   % iTS         , end="," )
        print(         "PGN=,%d"   % iPGN.value  , end="," )
        print(          "CM=,%s"   % szHow       , end="," )
        print(         "PRI=,%d"   % maskedPri   , end="," )
        print(         "SRC=,%02X" % iSRC        , end="," )
        print(         "DST=,%02X" % iDST        , end="," )
        print(         "LEN=,%d"   % nDataBytes  , end="," )     
        print( "DATA-HEX="                       , end="," )
        
        
        for ucByte in ucTxRxBuffer[10:nRetVal] :
             print("%02X" % ucByte, end="," )
        print("")    
         
    listOfDataStrings=[]
    for ucByte in ucTxRxBuffer[10:nRetVal] :
        listOfDataStrings.append("%02X" % ucByte)
    #for

  
    return {'TS':iTS, 'PGN':iPGN.value, 'CM':szHow, 'PRI':maskedPri, 'SRC':iSRC, 'DST':iDST, 'LEN':nDataBytes, 'hexData':listOfDataStrings, 'rawData':ucTxRxBuffer[10:nRetVal]}
#def PrintRxJ1939Message

#-----------------------------------------------------------------------------------------------------
# Print a transmitted J1939 message.
#-----------------------------------------------------------------------------------------------------

def PrintTxJ1939Message( nRetVal, ucTxRxBuffer, display='no' ) :
    '''This function prints a transmitted J1939 message to the screen.'''

    ucPGN      = (c_char*4)()
    iPGN       = c_int  (0)

    ucHowPri   = c_char (0)
    iHowPri    = c_int  (0)

    ucSRC      = c_char (0)
    ucDST      = c_char (0)
    iSRC       = c_int  (0)
    iDST       = c_int  (0)

    nDataBytes = c_short(0)

    ucPGN[0]   = ucTxRxBuffer[0]
    ucPGN[1]   = ucTxRxBuffer[1]
    ucPGN[2]   = ucTxRxBuffer[2]
    ucPGN[3]   = 0

    iPGN       = c_int( struct.unpack( '<L',(ucPGN[0]+ucPGN[1]+ucPGN[2]+ucPGN[3]))[0])

    ucHowPri   = c_char( struct.unpack( 'B', ucTxRxBuffer[3] )[0])
    iHowPri    = bytes( ucHowPri )[0]

    maskedHow  = ( iHowPri & 0x80 ) >> 7
    maskedPri  = ( iHowPri & 0x07 )

    ucSRC      = c_char( struct.unpack( 'B', ucTxRxBuffer[4]   )[0])
    ucDST      = c_char( struct.unpack( 'B', ucTxRxBuffer[5]   )[0])

    iSRC       = bytes( ucSRC )[0]
    iDST       = bytes( ucDST )[0]

    nDataBytes = nRetVal - 6

    if nDataBytes <= 8 :
        szHow = "N/A"
    else :
        if 1 == maskedHow :
            szHow = "BAM"
        else :
            szHow = "RTS"
        #if
    #if
    if display=='yes':
        print( "Tx,J1939,PGN=,%d"   % iPGN.value  , end="," )
        print(           "CM=,%s"   % szHow       , end="," )
        print(          "PRI=,%d"   % maskedPri   , end="," )
        print(          "SRC=,%02X" % iSRC        , end="," )
        print(          "DST=,%02X" % iDST        , end="," )
        print(          "LEN=,%d"   % nDataBytes  , end="," )
        print( "DATA-HEX=,"                          , end=""  )
    
        for ucByte in ucTxRxBuffer[6:nRetVal] :
             print("%02X" % ucByte, end="," )
        #for
    
        print("")

#def PrintTxJ1939Message

#-----------------------------------------------------------------------------------------------------
#  Send a request for J1939 VIN (PID=0, VIN=65260).
#-----------------------------------------------------------------------------------------------------

def SendJ1939RequestMessage( nClientID ) :
    '''This sends a J1939 request message (PGN 59904) asking for PGN 65260 - VIN.'''

    nDataBytes = c_short(0)

    ucTxRxBuffer[0] = 0x00        # LSB First of PGN59904 0x00EA00
    ucTxRxBuffer[1] = 0xEA        # Middle
    ucTxRxBuffer[2] = 0x00        # High Byte
    ucTxRxBuffer[3] = 6           # High bit=0 (RTS/CTS) with priority of 6
    ucTxRxBuffer[4] = 249         # OBPC1
    ucTxRxBuffer[5] = 0xFF        # All nodes 0xFF
    ucTxRxBuffer[6] = 0xEC        # LSB First of PGN65260 0x00FEEC
    ucTxRxBuffer[7] = 0xFE        # Middle
    ucTxRxBuffer[8] = 0x00        # High Byte
    
    nDataBytes = 9;
  
    nRetVal = RP1210_SendMessage( c_short( nClientID ), byref( ucTxRxBuffer ), c_short( nDataBytes ), c_short( 0 ), c_short( NON_BLOCKING_IO ) )
  
    if  nRetVal != 0 :
        print("RP1210_SendMessage( J1939 ) returns %i" % nRetVal )
    else :
        PrintTxJ1939Message( nDataBytes, ucTxRxBuffer )
    #if


#-----------------------------------------------------------------------------------------------------
# Print a received CAN message.
#-----------------------------------------------------------------------------------------------------

def PrintRxCANMessage( nRetVal, ucTxRxBuffer ) :
    '''This function prints a received CAN message to the screen.'''

    iTS        = c_int  (0)
    ucCANType  = c_char (0)
    iCANType   = c_int  (0)

    iCANID     = c_int  (0)

    #nDataBytes = c_short(0)

    iTS        = int(struct.unpack('>L',(ucTxRxBuffer[0]+ucTxRxBuffer[1]+ucTxRxBuffer[2]+ucTxRxBuffer[3]))[0])

    ucCANType  = c_char( struct.unpack( 'B', ucTxRxBuffer[4] )[0])
    iCANType   = bytes( ucCANType )[0]

    if iCANType == 0 :
        szCANType = "STD"
        iCANID    = int(struct.unpack('>H',(ucTxRxBuffer[5]+ucTxRxBuffer[6]))[0])
        iDataIdx  = 7
    else :
        szCANType = "EXT"
        iCANID    = int(struct.unpack('>L',(ucTxRxBuffer[5]+ucTxRxBuffer[6]+ucTxRxBuffer[7]+ucTxRxBuffer[8]))[0])
        iDataIdx  = 9
    #if

    #nDataBytes = nRetVal - iDataIdx

    print( "Rx CAN TS=[%d]"   % iTS         , end=" " )
    print(      "TYPE=[%s]"   % szCANType   , end=" " )
    print(    "CANID=[%0X]"   % iCANID                )
    print( ""                               , end="\t")
    print( "DATA-HEX"                       , end=""  )

    for ucByte in ucTxRxBuffer[iDataIdx:nRetVal] :
         print("[%02X]" % ucByte, end="" )
    #for

    print("")

#def PrintCANMessage

#-----------------------------------------------------------------------------------------------------
# Print a received CAN message.
#-----------------------------------------------------------------------------------------------------

def PrintTxCANMessage( nRetVal, ucTxRxBuffer ) :
    '''This function prints a transmitted CAN message to the screen.'''

    ucCANType  = c_char (0)
    iCANType   = c_int  (0)

    iCANID     = c_int  (0)

    #nDataBytes = c_short(0)

    ucCANType  = c_char( struct.unpack( 'B', ucTxRxBuffer[0] )[0])
    iCANType   = bytes( ucCANType )[0]

    if iCANType == 0 :
        szCANType = "STD"
        iCANID    = int(struct.unpack('>H',(ucTxRxBuffer[1]+ucTxRxBuffer[2]))[0])
        iDataIdx  = 3
    else :
        szCANType = "EXT"
        iCANID    = int(struct.unpack('>L',(ucTxRxBuffer[1]+ucTxRxBuffer[2]+ucTxRxBuffer[3]+ucTxRxBuffer[4]))[0])
        iDataIdx  = 5
    #if

    #nDataBytes = nRetVal - iDataIdx

    print( "Tx CAN TYPE=[%s]"   % szCANType   , end=" " )
    print(      "CANID=[%0X]"   % iCANID                )
    print( ""                                 , end="\t")
    print( "DATA-HEX"                         , end=""  )

    for ucByte in ucTxRxBuffer[iDataIdx:nRetVal] :
         print("[%02X]" % ucByte, end="" )
    #for

    print("")

#def PrintTxCANMessage

#-----------------------------------------------------------------------------------------------------
#  Send an extended CAN message request for J1939 VIN (PID=0, VIN=65260).
#-----------------------------------------------------------------------------------------------------

def SendCANRequestMessage( nClientID ) :
    '''This function sends an extended CAN message (J1939 PGN 59904) requesting PGN 65260 (VIN).'''

    nDataBytes = c_short(0)

    ucTxRxBuffer[0] = 0x01        # Extended CAN
    ucTxRxBuffer[1] = 0x18        # CANID 0x18EAFFF9 - Pri ExtDP/DP
    ucTxRxBuffer[2] = 0xEA        # PF=1
    ucTxRxBuffer[3] = 0xFF        # PS=Global Address
    ucTxRxBuffer[4] = 0xF9        # OBD PC 1
    ucTxRxBuffer[5] = 0xEC        # LSB First of PGN65260 0x00FEEC
    ucTxRxBuffer[6] = 0xFE        # Middle
    ucTxRxBuffer[7] = 0x00        # High Byte
    
    nDataBytes = 8;
  
    nRetVal = RP1210_SendMessage( c_short( nClientID ), byref( ucTxRxBuffer ), c_short( nDataBytes ), c_short( 0 ), c_short( NON_BLOCKING_IO ) )
  
    if  nRetVal != 0 :
        print("RP1210_SendMessage( CAN ) returns %i" % nRetVal )
    else :
        PrintTxCANMessage( nDataBytes, ucTxRxBuffer )
    #if


iAdapterID = 1
szDLLName =   "DGDPA5MA.DLL" 
szDLLName =   "DPA4PMA.DLL" 

iProtocolID = 1
szProtocolName = bytes( "J1708" , 'ascii' )

iDeviceID=1

try :
    hRP1210DLL = windll.LoadLibrary( szDLLName )
except :
    print("Error loading the DLL.")
    sys.exit(1)
        
#-----------------------------------------------------------------------------------------------------
# RP1210_ClientConnect
#-----------------------------------------------------------------------------------------------------
# typedef short (WINAPI *fxRP1210_ClientConnect)       ( HWND, short, char *, long, long, short );
    
prototype                   = WINFUNCTYPE( c_short, HWND, c_short, c_char_p, c_long, c_long, c_short)
RP1210_ClientConnect        = prototype( ( "RP1210_ClientConnect", hRP1210DLL ) )
    
#-----------------------------------------------------------------------------------------------------
# RP1210_ClientDisconnect
#-----------------------------------------------------------------------------------------------------
# typedef short (WINAPI *fxRP1210_ClientDisconnect)    ( short                                  );

prototype                   = WINFUNCTYPE( c_short, c_short )
RP1210_ClientDisconnect     = prototype( ( "RP1210_ClientDisconnect", hRP1210DLL ) )

#-----------------------------------------------------------------------------------------------------
# RP1210_SendMessage
#-----------------------------------------------------------------------------------------------------
# typedef short (WINAPI *fxRP1210_SendMessage)         ( short, char*, short, short, short      );

prototype                   = WINFUNCTYPE( c_short, c_short,  POINTER( c_char*2000 ), c_short, c_short, c_short      )
RP1210_SendMessage          = prototype( ("RP1210_SendMessage", hRP1210DLL ) )

#-----------------------------------------------------------------------------------------------------
# RP1210_ReadMessage
#-----------------------------------------------------------------------------------------------------
# typedef short (WINAPI *fxRP1210_ReadMessage)         ( short, char*, short, short             );

prototype                   = WINFUNCTYPE( c_short, c_short, POINTER( c_char*2000 ), c_short, c_short             )
RP1210_ReadMessage          = prototype( ("RP1210_ReadMessage", hRP1210DLL ) )

#-----------------------------------------------------------------------------------------------------
# RP1210_SendCommand
#-----------------------------------------------------------------------------------------------------
# typedef short (WINAPI *fxRP1210_SendCommand)         ( short, short, char*, short             );

prototype                   = WINFUNCTYPE( c_short, c_short, c_short, POINTER( c_char*2000 ), c_short             )
RP1210_SendCommand          = prototype( ("RP1210_SendCommand", hRP1210DLL ) )

#-----------------------------------------------------------------------------------------------------
# RP1210_ReadVersion
#-----------------------------------------------------------------------------------------------------
# typedef short (WINAPI *fxRP1210_ReadVersion)         ( char*, char*, char*, char*             );

prototype                   = WINFUNCTYPE( c_short, c_char_p, c_char_p, c_char_p, c_char_p             )
RP1210_ReadVersion          = prototype( ("RP1210_ReadVersion", hRP1210DLL ) )

#-----------------------------------------------------------------------------------------------------
# RP1210_ReadDetailedVersion
#-----------------------------------------------------------------------------------------------------
# typedef short (WINAPI *fxRP1210_ReadDetailedVersion) ( short, char*, char*, char*             );

prototype                   = WINFUNCTYPE( c_short, c_short, POINTER(c_char*17), POINTER(c_char*17), POINTER(c_char*17) )
RP1210_ReadDetailedVersion  = prototype( ("RP1210_ReadDetailedVersion", hRP1210DLL ) )

#-----------------------------------------------------------------------------------------------------
# RP1210_GetHardwareStatus
#-----------------------------------------------------------------------------------------------------
# typedef short (WINAPI *fxRP1210_GetHardwareStatus)   ( short, char*, short, short             );

prototype                   = WINFUNCTYPE( c_short, c_short, c_char_p, c_short, c_short             )
RP1210_GetHardwareStatus    = prototype( ("RP1210_GetHardwareStatus", hRP1210DLL ) )

#-----------------------------------------------------------------------------------------------------
# RP1210_GetErrorMsg
#-----------------------------------------------------------------------------------------------------
# typedef short (WINAPI *fxRP1210_GetErrorMsg)         ( short, char*                           );

prototype                   = WINFUNCTYPE( c_short, c_short, c_char_p                           )
RP1210_GetErrorMsg          = prototype( ("RP1210_GetErrorMsg", hRP1210DLL ) )

#-----------------------------------------------------------------------------------------------------
# RP1210_GetLastErrorMsg
#-----------------------------------------------------------------------------------------------------
# typedef short (WINAPI *fxRP1210_GetLastErrorMsg)     ( short, int *, char*, short             );

prototype                   = WINFUNCTYPE( c_short, c_void_p, c_char_p, c_short             )
RP1210_GetLastErrorMsg      = prototype( ("RP1210_GetLastErrorMsg", hRP1210DLL ) )

#-----------------------------------------------------------------------------------------------------
# Connect to Device
#-----------------------------------------------------------------------------------------------------

print( "Attempting connect to DLL [%s], DeviceID [%d], Protocol [%s]" %( szDLLName, iDeviceID, str( szProtocolName, 'ascii' ) ) )

nClientID = RP1210_ClientConnect( HWND(None), c_short( iDeviceID ), szProtocolName, 0, 0, 0  )

print('The Client ID is: %i' %nClientID )

if nClientID > 127:
   print('There was an error calling RP1210_ClientConnect(): %s' % RP1210Errors[nClientID] )
   sys.exit( int( nClientID ) )
#if

##-----------------------------------------------------------------------------------------------------
## Call RP1210_ReadVersion to get DLL Major/Minor and API Major/Minor values.
##-----------------------------------------------------------------------------------------------------
#
#nRetVal = RP1210_ReadVersion( byref( fpchDLLMajorVersion ), byref( fpchDLLMinorVersion ),byref( fpchAPIMajorVersion ),byref( fpchAPIMinorVersion ))
#
#if nRetVal == 0 :
#   print('DLL MAJ/MIN = %s.%s'  %( str( fpchDLLMajorVersion, 'ascii' ), str( fpchDLLMinorVersion, 'ascii' ) ) )
#   print('API MAJ/MIN = %s.%s'  %( str( fpchAPIMajorVersion, 'ascii' ), str( fpchAPIMinorVersion, 'ascii' ) ) )
#else :
#   print("ReadVersion fails with a return value of  %i" %(nRetVal) )
##if
#
##-----------------------------------------------------------------------------------------------------
## Call RP1210_ReadDetailedVersion to get DLL, API, FW versions.
##-----------------------------------------------------------------------------------------------------
#
nRetVal = RP1210_ReadDetailedVersion( c_short( nClientID ), byref( chAPIVersionInfo ), byref( chDLLVersionInfo ), byref( chFWVersionInfo ) )

if nRetVal == 0 :
   szAPI = str( chAPIVersionInfo, 'ascii' )
   szDLL = str( chDLLVersionInfo, 'ascii' )
   szFW  = str( chFWVersionInfo , 'ascii' )

   print('DLL = %s' % szDLL  )
   print('API = %s' % szAPI  )
   print('FW  = %s' % szFW   )
else :   
   print("ReadDetailedVersion fails with a return value of  %i" %(nRetVal) )
#if

#-----------------------------------------------------------------------------------------------------
# Set all filters to pass.  This allows messages to be read.
#-----------------------------------------------------------------------------------------------------

nRetVal = RP1210_SendCommand( c_short( RP1210_Set_All_Filters_States_to_Pass ), c_short( nClientID ), None, 0 )

if nRetVal == 0 :
   print("RP1210_Set_All_Filters_States_to_Pass - SUCCESS" )
else :
   print('RP1210_Set_All_Filters_States_to_Pass returns %i: %s' %(nRetVal,RP1210Errors[nRetVal]) )
#if

#-----------------------------------------------------------------------------------------------------
# If we are on J1939, claim address F9/249.
#-----------------------------------------------------------------------------------------------------

ProtocolName = str( szProtocolName, 'ascii' )

if ProtocolName.find( "J1939" ) != -1 :

   # J1939 "NAME" for this sample source code application ( see J1939/81 )
   #    Self Configurable       =   0 = NO
   #    Industry Group          =   0 = GLOBAL
   #    Vehicle System          =   0 = Non-Specific
   #    Vehicle System Instance =   0 = First Diagnostic PC
   #    Reserved                =   0 = Must be zero
   #    Function                = 129 = Offboard Service Tool
   #    Function Instance       =   0 = First Offboard Service Tool
   #    Manufacturer Code       =  11 = Dearborn Group, Inc. 
   #    Manufacturer Identity   =   0 = Dearborn Group, Inc. Sample Source Code
   
   #Note: I'm copying the "name" Cummins gives; check standard to see what this means
   print( "Claiming J1939 address 250" )
   
   ucTxRxBuffer[0] = c_char(    250 )
   ucTxRxBuffer[1] = c_char(   0x86 )
   ucTxRxBuffer[2] = c_char(   0x68 )
   ucTxRxBuffer[3] = c_char(   0x54 )
   ucTxRxBuffer[4] = c_char(   0x01 )
   ucTxRxBuffer[5] = c_char(      0 )
   ucTxRxBuffer[6] = c_char(   0x80 )
   ucTxRxBuffer[7] = c_char(      0 )
   ucTxRxBuffer[8] = c_char(      0 )
   ucTxRxBuffer[9] = c_char( BLOCK_UNTIL_DONE )

   nRetVal = RP1210_SendCommand( c_short( RP1210_Protect_J1939_Address ), c_short( nClientID ), byref( ucTxRxBuffer ), 10 )

   if nRetVal == 0 :
      print("RP1210_Protect_J1939_Address - SUCCESS" )
   else :
      print("RP1210_Protect_J1939_Address returns %i: %s" %(nRetVal,RP1210Errors[nRetVal]) )
   #if



def PrintRxJ1708Message( nRetVal, ucTxRxBuffer, display=False ) :
    '''This function prints a received J1708/J1587 message to the screen.'''
    
    
    timeStamp = int(struct.unpack('>L',(ucTxRxBuffer[0]+ucTxRxBuffer[1]+ucTxRxBuffer[2]+ucTxRxBuffer[3]))[0])
    MID      = int(struct.unpack( 'B', ucTxRxBuffer[4]   )[0])
   
    dataLength = int(nRetVal - 6)
    PIDs=[]
    dataList=[]
    
    i=5
    while i < nRetVal:    
        PID = int(struct.unpack('B', ucTxRxBuffer[i])[0])
        if PID >= 0 and PID < 128:
            a = ucTxRxBuffer[i+1]
            i+=2
        elif PID >= 128 and PID < 192:
            a = ucTxRxBuffer[i+1]+ucTxRxBuffer[i+2]
            i+=3
        elif PID >= 192 and PID < 255:
            n = int(struct.unpack('B', ucTxRxBuffer[i+1])[0])           
            a = b''
            for j in range(i+2,i+2+n):
                a+=ucTxRxBuffer[j]
            i+=2
            i+=n
        
        elif PID == 255: #extended PID
            if display:
                print('Extended ID')            
            PID = 256 + int(struct.unpack('B', ucTxRxBuffer[i+1])[0])
            if PID >= 256 and PID < 384:
                a = ucTxRxBuffer[i+1]
                i+=2
            elif PID >= 384 and PID < 448:
                #a = int(struct.unpack('<H', ucTxRxBuffer[i+1]+ucTxRxBuffer[i+2])[0])
                a = ucTxRxBuffer[i+1]+ucTxRxBuffer[i+2]
                i+=3
            elif PID >= 448 and PID < 512:
                n = int(struct.unpack('B', ucTxRxBuffer[i+1])[0])           
                a = b''
                for j in range(i+2,i+2+n):
                    a+=ucTxRxBuffer[j]
                i+=2
                i+=n
        else:
           print('This should not be printing. There is something wrong.')
           
        PIDs.append(PID)
        dataList.append(a)
        if display:
            print( "Rx J1708 TS= %d, " % timeStamp           , end=" " )
            print(         "MID=[%d]" % MID         , end=" " )
            print(         "PID=[%d]" % PID         , end=" " )
           # print(         "LEN=[%d]" % DataBytes              )
            print( ""                                 , end="\t")
            print( "DATA: "                         , end=""  )
            print(a)
    
    return timeStamp,MID,PIDs,dataLength,dataList 
    


def getJ1587(desiredPID,PIDName='',display=False):
    if desiredPID > 0 and desiredPID < 255:
        ucTxRxBuffer[0] = 0x08 #Priority for J1708
        ucTxRxBuffer[1] = 0xAC #MID for Off-board Diagnosics #1 (decimal 172)
        ucTxRxBuffer[2] = 0x00 # Request PID
        ucTxRxBuffer[3] = desiredPID #PID 

        nDataBytes = 4
    elif desiredPID >= 255 and desiredPID < 512:
        ucTxRxBuffer[0] = 0x08 #Priority for J1708
        ucTxRxBuffer[1] = 0xAC #MID for Off-board Diagnosics #1 (decimal 172)
        ucTxRxBuffer[2] = 0xFF # Request PID
        ucTxRxBuffer[3] = 0x00 # Request PID
        ucTxRxBuffer[4] = desiredPID - 256 #PID 

        nDataBytes = 5
        
    nRetVal = RP1210_SendMessage( c_short( nClientID ), byref( ucTxRxBuffer ), c_short( nDataBytes ), c_short( 0 ), c_short( NON_BLOCKING_IO ) )
    if nRetVal != 0 :
        print("Request RP1210_SendMessage returns %i" % nRetVal )
    
    PID=0
    start = time.time()
    allNetworkData={'timeStamps':[], 'MIDs':[], 'PIDs':[], 'dataList':[]} 
    
    while PID != desiredPID and time.time()-start < 11:    
        nRetVal = RP1210_ReadMessage( c_short( nClientID ), byref( ucTxRxBuffer ), c_short( 2000 ), c_short( BLOCKING_IO ) )
        timeStamp,MID,PIDs,dataLength,dataList = PrintRxJ1708Message( nRetVal, ucTxRxBuffer)
        for PID,data in zip(PIDs,dataList):
            allNetworkData['timeStamps'].append(timeStamp)
            allNetworkData['MIDs'].append(MID)
            allNetworkData['PIDs'].append(PID)
            allNetworkData['dataList'].append(data)
            
            if PID == desiredPID: 
                return data,allNetworkData 
        
    if display:
        print('PID %d, %s is not available on J1708/J1587 bus.' %(desiredPID,PIDName))
    return 'NotAvailable',allNetworkData



def decodeJ1587Bytes(PID,byteData,display=True):
    
    if PID == 74:
        maxRoadSpeedLimit= 0.5 * int(struct.unpack('B',byteData)[0])
        if display:
            print('maxRoadSpeedLimit = %0.1f mph' %maxRoadSpeedLimit) 
        return maxRoadSpeedLimit,"mph"
    
    elif PID == 87:
       cruiseControlHighSetLimitSpeed = 0.5 * int(struct.unpack('B',byteData)[0])
       if display:
           print('cruiseControlHighSetLimitSpeed = %0.1f mph' %cruiseControlHighSetLimitSpeed)
       return cruiseControlHighSetLimitSpeed,"mph"

    elif PID == 88:
       cruiseControlLowSetLimitSpeed = 0.5 * int(struct.unpack('B',byteData)[0])
       if display:
           print('cruiseControlLowSetLimitSpeed = %0.1f mph' %cruiseControlLowSetLimitSpeed)
       return cruiseControlLowSetLimitSpeed,"mph"


def transportSendRequest(byteStringToSend):
    
    # Abort
    ucTxRxBuffer[0] = 0x08 # Priority for J1708
    ucTxRxBuffer[1] = 0xb6 # MID for Off-board Programming Station
    ucTxRxBuffer[2] = 0xC5 # Communication Management PID
    ucTxRxBuffer[3] = 0x02 # Length of Message
    ucTxRxBuffer[4] = 0x80 # MID of target 
    ucTxRxBuffer[5] = 0xFF # Abort command
    
    nDataBytes = 6

    nRetVal = RP1210_SendMessage( c_short( nClientID ), byref( ucTxRxBuffer ), c_short( nDataBytes ), c_short( 0 ), c_short( NON_BLOCKING_IO ) )
    if nRetVal != 0 :
        print("Request RP1210_SendMessage returns %i" % nRetVal )
    #done sending abort
    n=len(byteStringToSend)
    nBytes=n.to_bytes(2,'little')
    print(nBytes)
    
    
    #request to send
    ucTxRxBuffer[0] = 0x08 # Priority for J1708
    ucTxRxBuffer[1] = 0xb6 # MID for Off-board Programming Station
    ucTxRxBuffer[2] = 0xC5 # Communication Management PID
    ucTxRxBuffer[3] = 0x05 # Length of Message
    ucTxRxBuffer[4] = 0x80 # MID of target 
    ucTxRxBuffer[5] = 0x01 # Request to send
    ucTxRxBuffer[6] = 0x01 # Segments
    ucTxRxBuffer[7:9] = nBytes # lo bytes
    
    nDataBytes = 9
    
    byteCount = int(struct.unpack('<H',ucTxRxBuffer[7]+ucTxRxBuffer[8])[0])
    print('Request to send %d bytes.' %byteCount)  
    
    nRetVal = RP1210_SendMessage( c_short( nClientID ), byref( ucTxRxBuffer ), c_short( nDataBytes ), c_short( 0 ), c_short( NON_BLOCKING_IO ) )
    if nRetVal != 0 :
        print("Request RP1210_SendMessage returns %i" % nRetVal )
  
     #wait for clear to send
    
    i=0
    CTS = False
    while i <1000 and CTS == False  :    
        nRetVal = RP1210_ReadMessage( c_short( nClientID ), byref( ucTxRxBuffer ), c_short( 2000 ), c_short( BLOCKING_IO ) )
        timeStamp,MID,PIDs,dataLength,dataList = PrintRxJ1708Message( nRetVal, ucTxRxBuffer)
        i+=1
        for PID,data in zip(PIDs,dataList):
            #print(PID)
            if PID == 197 and int(data[1])==2:
                    CTS = True
                    segmentsClearedFor = data[2]
                    startSegment = data[3]
                    print('Cleared to send %d segments.' %segmentsClearedFor)
                    break
    if CTS: 
         # Send data 
        ucTxRxBuffer[0] = 0x08 # Priority for J1708
        ucTxRxBuffer[1] = 0xb6 # MID for Off-board Programming Station
        ucTxRxBuffer[2] = 0xc6 # Connection mode data transfer PID
        ucTxRxBuffer[3] = (2+n).to_bytes(1,'little') # Length of Message
        ucTxRxBuffer[4] = 0x80 # MID of target 
        ucTxRxBuffer[5] = startSegment # Segment Number
        
        ucTxRxBuffer[6:6+n] = byteStringToSend
        
        nDataBytes = 6+n
        
        print('Sending bytes:', end=' ')
        print(ucTxRxBuffer[6:6+n])
        
        nRetVal = RP1210_SendMessage( c_short( nClientID ), byref( ucTxRxBuffer ), c_short( nDataBytes ), c_short( 0 ), c_short( NON_BLOCKING_IO ) )
        if nRetVal != 0 :
            print("Request RP1210_SendMessage returns %i" % nRetVal )
  
        #wait for acknowledgement
        PID=0
        i=0
        ACK = False
        while i <1000 and ACK == False  :    
            nRetVal = RP1210_ReadMessage( c_short( nClientID ), byref( ucTxRxBuffer ), c_short( 2000 ), c_short( BLOCKING_IO ) )
            timeStamp,MID,PIDs,dataLength,dataList = PrintRxJ1708Message( nRetVal, ucTxRxBuffer)
            i+=1
            for PID,data in zip(PIDs,dataList):
                if PID == 197 and int(data[1])==3:
                    ACK = True
                    print('Message Recieved.')
                    break


def transportGetMessage(filename):
    
    #Wait for a request to send
    PID=0
    i=0
    RTS = False
    while  i <1000 and RTS == False  :    
        nRetVal = RP1210_ReadMessage( c_short( nClientID ), byref( ucTxRxBuffer ), c_short( 2000 ), c_short( BLOCKING_IO ) )
        timeStamp,MID,PIDs,dataLength,dataList = PrintRxJ1708Message( nRetVal, ucTxRxBuffer)
        i+=1
        for PID,data in zip(PIDs,dataList):
            #print(PID)
            #print(data)
            if PID == 197 and int(data[1])==1:
                RTS = True
                segments = data[2]
                byteCount = int.from_bytes(data[3:4],byteorder='little')
                print('Requested to Recieved %d Segments totaling %d bytes' %(segments,byteCount))
                break
    if RTS:
       #Send a clear to send (CTS) response
        # Send data 
        ucTxRxBuffer[0] = 0x08 # Priority for J1708
        ucTxRxBuffer[1] = 0xb6 # MID for Off-board Programming Station
        ucTxRxBuffer[2] = 0xc5 # Connection mode data transfer PID
        ucTxRxBuffer[3] = 0x04 # Length of Message
        ucTxRxBuffer[4] = 0x80 # MID of target 
        ucTxRxBuffer[5] = 0x02 # Clear to Send command
        ucTxRxBuffer[6] = segments # Segments
        ucTxRxBuffer[7] = 0x01
        
        nDataBytes = 8
        
        print('Sending Clear to Send (CTS) %d segments starting with 1' %segments)
        
        nRetVal = RP1210_SendMessage( c_short( nClientID ), byref( ucTxRxBuffer ), c_short( nDataBytes ), c_short( 0 ), c_short( NON_BLOCKING_IO ) )
        if nRetVal != 0 :
            print("Request RP1210_SendMessage returns %i" % nRetVal )
   
        #assemble message that comes in
        RXSegments = {}
        while len(RXSegments) < segments:
            nRetVal = RP1210_ReadMessage( c_short( nClientID ), byref( ucTxRxBuffer ), c_short( 2000 ), c_short( BLOCKING_IO ) )
            timeStamp,MID,PIDs,dataLength,dataList = PrintRxJ1708Message( nRetVal, ucTxRxBuffer)
            for PID,data in zip(PIDs,dataList):
                if PID == 198:
                    #print(data)
                    segmentRXd = int(data[1])
                    dataRXd=data[2:]
                    RXSegments[segmentRXd]=dataRXd
                    print('Recived Segment %d of %d bytes' %(segmentRXd,len(dataRXd)))
        
          
        print('Done with Segments')
         # Send Acknowledgment three times
        ucTxRxBuffer[0] = 0x08 # Priority for J1708
        ucTxRxBuffer[1] = 0xb6 # MID for Off-board Programming Station
        ucTxRxBuffer[2] = 0xc5 # Connection mode data transfer PID
        ucTxRxBuffer[3] = 0x02 # Length of Message
        ucTxRxBuffer[4] = 0x80 # MID of target 
        ucTxRxBuffer[5] = 0x03 # Segment Number
         
        nDataBytes = 6
        
        print('Sending Acknowledgements')
        
        for i in range(3):
            nRetVal = RP1210_SendMessage( c_short( nClientID ), byref( ucTxRxBuffer ), c_short( nDataBytes ), c_short( 0 ), c_short( NON_BLOCKING_IO ) )
            if nRetVal != 0 :
                print("Request RP1210_SendMessage returns %i" % nRetVal )
       
        assembledBytes = b''
        keyList=RXSegments.keys()
        #print(keyList)
        for key in keyList:
           #print(key)
           #print(RXSegments[key])
           assembledBytes += RXSegments[key]
        
        binFile=open(filename,'wb')
        binFile.write(assembledBytes)
        binFile.close()
        
        return assembledBytes
        
def sendDataLinkEscape():
    ucTxRxBuffer[0] = 0x08 # Priority for J1708
    ucTxRxBuffer[1] = 0xb6 # MID for Off-board Programming Station
    ucTxRxBuffer[2] = 0xfe # Data Link Escape PID
    ucTxRxBuffer[3] = 0x80 # 
    ucTxRxBuffer[4] = 0x00 #
    ucTxRxBuffer[5] = 0xdb # 
     
    nDataBytes = 6
    
    print('Sending Data Link Escape')
    
    nRetVal = RP1210_SendMessage( c_short( nClientID ), byref( ucTxRxBuffer ), c_short( nDataBytes ), c_short( 0 ), c_short( NON_BLOCKING_IO ) )
    if nRetVal != 0 :
          print("Request RP1210_SendMessage returns %i" % nRetVal )
 


def processSecondsForTime(TSbytes):
    tZero=time.mktime((1985,1,1,0,0,0,0,1,0)) - 6*3600 #Set the epoc for J1587
    #tZero should be 473407200.0 seconds  
    TS = struct.unpack('<L',TSbytes)[0] + tZero
    timeString = time.strftime("%A, %d %b %Y at %H:%M:%S (UTC)", time.gmtime(TS))
    return timeString
    
    
def getDDEC4HardBrakeData(assembledBytes):
    dataBytes={}
    dataValue={}
    dataUnits={}
    #Bytes 5729-5732 in XTR file
    #Last Stop Record of DDEC Reportd
    
    dataBytes['Incident Odometer'] = assembledBytes[61:65] 
    dataValue['Incident Odometer'] = '%0.1f' %(struct.unpack('<L', dataBytes['Incident Odometer'])[0] * 0.1)
    dataUnits['Incident Odometer'] = 'Miles'
    #5004 = 9:65
    dataBytes['Road Speed']=[]
    dataValue['Road Speed']=[]
    dataUnits['Road Speed']='MPH'
    
    dataBytes['Engine Speed']=[]
    dataValue['Engine Speed']=[]
    dataUnits['Engine Speed']='RPM'
    
    dataBytes['Engine Load']=[]
    dataValue['Engine Load']=[]
    dataUnits['Engine Load']='Percent'
    
    dataBytes['Throttle']=[]
    dataValue['Throttle']=[]
    dataUnits['Throttle']='Percent'
    
    dataValue['Brake Switch']=[]
    dataValue['Clutch Switch']=[]
    dataValue['Cruise Switch']=[]
    dataValue['Diagnostic Code']=[]
       
    dataValue['Time']=[]
    j=-59
    for k in range(70,519,6):
        dataValue['Time'].append(j)
        j+=1
        
        dataBytes['Road Speed'].append(assembledBytes[k+0])
        dataValue['Road Speed'].append('%0.1f' %(assembledBytes[k+0] * 0.5))
        
        dataBytes['Engine Speed'].append(assembledBytes[k+1:k+1+2])
        dataValue['Engine Speed'].append('%0.1f' %(struct.unpack('<H',assembledBytes[k+1:k+1+2])[0] * 0.5))
        
        dataBytes['Engine Load'].append(assembledBytes[k+3])
        dataValue['Engine Load'].append('%0.1f' %(assembledBytes[k+3]  * 0.5))
        
        dataBytes['Throttle'].append(assembledBytes[k+4])
        dataValue['Throttle'].append('%0.1f' %(assembledBytes[k+4]  * 0.4))
       
        bitField = assembledBytes[k+5]
       
        if bitField & 32 == 32:
           dataValue['Brake Switch'].append('Yes')
        else:
           dataValue['Brake Switch'].append('No')
              
        if bitField & 64 == 64:
          dataValue['Clutch Switch'].append('Yes')
        else:
          dataValue['Clutch Switch'].append('No')
       
        if bitField & 128 == 128: 
           dataValue['Cruise Switch'].append('Yes')
        else:
           dataValue['Cruise Switch'].append('No')
       
        if bitField & 1 == 1:
           dataValue['Diagnostic Code'].append('Yes')
        else:
           dataValue['Diagnostic Code'].append('No')
   
    dataBytes['Incident Time'] = assembledBytes[520:524] 
    dataValue['Incident Time'] = processSecondsForTime(dataBytes['Incident Time'])
    dataUnits['Incident Time'] = 'Time Stamp'
       
    return dataBytes,dataValue,dataUnits
   
   
   
def getDDEC4LastStopData(assembledBytes):
    dataBytes={}
    dataValue={}
    dataUnits={}
    #Bytes 5729-5732 in XTR file
    #Last Stop Record of DDEC Reportd
    
    dataBytes['Incident Odometer'] = assembledBytes[61:65] 
    dataValue['Incident Odometer'] = '%0.1f' %(struct.unpack('<L', dataBytes['Incident Odometer'])[0] * 0.1)
    dataUnits['Incident Odometer'] = 'Miles'
    #5004 = 9:65
    dataBytes['Road Speed']=[]
    dataValue['Road Speed']=[]
    dataUnits['Road Speed']='MPH'
    
    dataBytes['Engine Speed']=[]
    dataValue['Engine Speed']=[]
    dataUnits['Engine Speed']='RPM'
    
    dataBytes['Engine Load']=[]
    dataValue['Engine Load']=[]
    dataUnits['Engine Load']='Percent'
    
    dataBytes['Throttle']=[]
    dataValue['Throttle']=[]
    dataUnits['Throttle']='Percent'
    
    dataValue['Brake Switch']=[]
    dataValue['Clutch Switch']=[]
    dataValue['Cruise Switch']=[]
    dataValue['Diagnostic Code']=[]
       
    dataValue['Time']=[]
    j=-104
    for k in range(65,784,6):
        dataValue['Time'].append(j)
        j+=1
        
        dataBytes['Road Speed'].append(assembledBytes[k+0])
        dataValue['Road Speed'].append('%0.1f' %(assembledBytes[k+0] * 0.5))
        
        dataBytes['Engine Speed'].append(assembledBytes[k+1:k+1+2])
        dataValue['Engine Speed'].append('%0.1f' %(struct.unpack('<H',assembledBytes[k+1:k+1+2])[0] * 0.5))
        
        dataBytes['Engine Load'].append(assembledBytes[k+3])
        dataValue['Engine Load'].append('%0.1f' %(assembledBytes[k+3]  * 0.5))
        
        dataBytes['Throttle'].append(assembledBytes[k+4])
        dataValue['Throttle'].append('%0.1f' %(assembledBytes[k+4]  * 0.4))
       
        bitField = assembledBytes[k+5]
       
        if bitField & 32 == 32:
           dataValue['Brake Switch'].append('Yes')
        else:
           dataValue['Brake Switch'].append('No')
              
        if bitField & 64 == 64:
          dataValue['Clutch Switch'].append('Yes')
        else:
          dataValue['Clutch Switch'].append('No')
       
        if bitField & 128 == 128: 
           dataValue['Cruise Switch'].append('Yes')
        else:
           dataValue['Cruise Switch'].append('No')
       
        if bitField & 1 == 1:
           dataValue['Diagnostic Code'].append('Yes')
        else:
           dataValue['Diagnostic Code'].append('No')
   
    dataBytes['Incident Time'] = assembledBytes[790:794] 
    dataValue['Incident Time'] = processSecondsForTime(dataBytes['Incident Time'])
    dataUnits['Incident Time'] = 'Time Stamp'
       
    return dataBytes,dataValue,dataUnits

def getDDEC4ActivityData(assembledBytes):
    #Activity Data for DDEC4
    activityDataBytes={}
    activityDataValue={}
    dataUnits={}
  
    #Bytes 92-95 in XTR        
    activityDataBytes['Distance'] = assembledBytes[61:65] 
    activityDataValue['Distance'] = '%0.1f' %(struct.unpack('<L', activityDataBytes['Distance'])[0] * 0.1)
    dataUnits['Distance'] = 'Miles'
           
    #Bytes 96-99 in XTR file
    #Trip Activity of DDEC Reports
    activityDataBytes['Fuel Used'] = assembledBytes[65:69] 
    activityDataValue['Fuel Used'] = '%0.3f' %(struct.unpack('<L', activityDataBytes['Fuel Used'])[0] * 0.125)
    dataUnits['Fuel Used'] = 'Gallons'
    
    #Bytes 100-103 in XTR file
    #Trip Activity of DDEC Reportd
    activityDataBytes['Time'] = assembledBytes[69:73] 
    secs = struct.unpack('<L', activityDataBytes['Time'])[0]
    activityDataValue['Time'] = '%02d:%02d:%02d' %(secs/3600,secs%3600/60,secs%3600%60)
    dataUnits['Time'] = 'HH:MM:SS'
  
    #Bytes 104-107 in XTR file
    # Not in DDEC Reports
    activityDataBytes['Drive Distance'] = assembledBytes[73:77] 
    activityDataValue['Drive Distance'] = '%0.1f' %(struct.unpack('<L', activityDataBytes['Drive Distance'])[0] * 0.1)
    dataUnits['Drive Distance'] = 'Miles'
  
    #Bytes 108-115 Make no change (8 bytes)
    
    #Bytes 116-119 in XTR file
    #Trip Activity 
    activityDataBytes['Cruise Distance'] = assembledBytes[85:89] 
    activityDataValue['Cruise Distance'] = '%0.1f' %(struct.unpack('<L', activityDataBytes['Cruise Distance'])[0] * 0.1)
    dataUnits['Cruise Distance'] = 'Miles'
    
    #Bytes 120-123 in XTR file
    #Trip Activity 
    activityDataBytes['Cruise Fuel'] = assembledBytes[89:93] 
    activityDataValue['Cruise Fuel'] = '%0.3f' %(struct.unpack('<L', activityDataBytes['Cruise Fuel'])[0] * 0.125)
    dataUnits['Cruise Fuel'] = 'Gallons'
    
    #Bytes 124-127 in XTR file
    #Trip Activity 
    activityDataBytes['Cruise Time'] = assembledBytes[93:97] 
    secs = struct.unpack('<L', activityDataBytes['Cruise Time'])[0]
    activityDataValue['Cruise Time'] = '%02d:%02d:%02d' %(secs/3600,secs%3600/60,secs%3600%60)
    dataUnits['Cruise Time'] = 'HH:MM:SS'
    
    #Bytes 128-131 in XTR file
    #Trip Activity 
    activityDataBytes['Top Gear Distance'] = assembledBytes[97:101] 
    activityDataValue['Top Gear Distance'] = '%0.1f' %(struct.unpack('<L', activityDataBytes['Top Gear Distance'])[0] * 0.1)
    dataUnits['Top Gear Distance'] = 'Miles'
    
    #Bytes 132-135 in XTR file
    #Trip Activity 
    activityDataBytes['Top Gear Fuel'] = assembledBytes[101:105] 
    activityDataValue['Top Gear Fuel'] = '%0.3f' %(struct.unpack('<L', activityDataBytes['Top Gear Fuel'])[0] * 0.125)
    dataUnits['Top Gear Fuel'] = 'Gallons'
   
    #Bytes 136-139 in XTR file
    #Trip Activity 
    activityDataBytes['Top Gear Time'] = assembledBytes[105:109] 
    secs = struct.unpack('<L', activityDataBytes['Top Gear Time'])[0]
    activityDataValue['Top Gear Time'] = '%02d:%02d:%02d' %(secs/3600,secs%3600/60,secs%3600%60)
    dataUnits['Top Gear Time'] = 'HH:MM:SS'
    
    #Bytes 140-143 in XTR file
    #Trip Activity 
    activityDataBytes['Idle Fuel'] = assembledBytes[109:113] 
    activityDataValue['Idle Fuel'] = '%0.3f' %(struct.unpack('<L', activityDataBytes['Idle Fuel'])[0] * 0.125)
    dataUnits['Idle Fuel'] = 'Gallons'
   
    #Bytes 144-147 in XTR file
    #Trip Activity 
    activityDataBytes['Idle Time'] = assembledBytes[113:117] 
    secs = struct.unpack('<L', activityDataBytes['Idle Time'])[0]
    activityDataValue['Idle Time'] = '%02d:%02d:%02d' %(secs/3600,secs%3600/60,secs%3600%60)
    dataUnits['Idle Time'] = 'HH:MM:SS'
    
    #Bytes 148-151 in XTR file
    #Trip Activity 
    activityDataBytes['Power Take Off Fuel'] = assembledBytes[117:121] 
    activityDataValue['Power Take Off Fuel'] = '%0.3f' %(struct.unpack('<L', activityDataBytes['Power Take Off Fuel'])[0] * 0.125)
    dataUnits['Power Take Off Fuel'] = 'Gallons'
    
    #Bytes 152-155 in XTR file
    #Trip Activity 
    activityDataBytes['Power Take Off Time'] = assembledBytes[121:125] 
    secs = struct.unpack('<L', activityDataBytes['Power Take Off Time'])[0]
    activityDataValue['Power Take Off Time'] = '%02d:%02d:%02d' %(secs/3600,secs%3600/60,secs%3600%60)
    dataUnits['Power Take Off Time'] = 'HH:MM:SS'
    
    #Bytes 156-159 in XTR file
    #Trip Activity 
    activityDataBytes['Over Speed A Time'] = assembledBytes[125:129] 
    secs = struct.unpack('<L', activityDataBytes['Over Speed A Time'])[0]
    activityDataValue['Over Speed A Time'] = '%02d:%02d:%02d' %(secs/3600,secs%3600/60,secs%3600%60)
    dataUnits['Over Speed A Time'] = 'HH:MM:SS'
    
    #Bytes 160-163 in XTR file
    #Trip Activity 
    activityDataBytes['Over Speed B Time'] = assembledBytes[129:133] 
    secs = struct.unpack('<L', activityDataBytes['Over Speed B Time'])[0]
    activityDataValue['Over Speed B Time'] = '%02d:%02d:%02d' %(secs/3600,secs%3600/60,secs%3600%60)
    dataUnits['Over Speed B Time'] = 'HH:MM:SS'
    
    #Bytes 164-167 in XTR file
    #Trip Activity 
    activityDataBytes['Over Rev Time'] = assembledBytes[133:137] 
    secs = struct.unpack('<L', activityDataBytes['Over Rev Time'])[0]
    activityDataValue['Over Rev Time'] = '%02d:%02d:%02d' %(secs/3600,secs%3600/60,secs%3600%60)
    dataUnits['Over Rev Time'] = 'HH:MM:SS'
    
    #Bytes 168-171 in XTR file
    #Trip Activity 
    activityDataBytes['Coast Time'] = assembledBytes[137:141] 
    secs = struct.unpack('<L', activityDataBytes['Coast Time'])[0]
    activityDataValue['Coast Time'] = '%02d:%02d:%02d' %(secs/3600,secs%3600/60,secs%3600%60)
    dataUnits['Coast Time'] = 'HH:MM:SS'
    
    #Byte 172 in XTR file
    #Trip Activity
    activityDataBytes['Peak Road Speed'] = assembledBytes[141] 
    activityDataValue['Peak Road Speed'] = '%0.1f' %(activityDataBytes['Peak Road Speed'] * 0.5)
    dataUnits['Peak Road Speed'] = 'MPH'
    
    #Bytes 173-174 in XTR file
    #Trip Activity 
    activityDataBytes['Peak Engine Speed'] = assembledBytes[142:144]
    activityDataValue['Peak Engine Speed'] = '%d' %(struct.unpack('<H',activityDataBytes['Peak Engine Speed'])[0] * 0.25)
    dataUnits['Peak Engine Speed'] = 'RPM'    
    
    #Bytes 175 in XTR file
    #Configuration
    activityDataBytes['Top Gear Ratio'] = assembledBytes[144] 
    activityDataValue['Top Gear Ratio'] = activityDataBytes['Top Gear Ratio']
    dataUnits['Top Gear Ratio'] = 'RPM/MPH'
   
    #Bytes 176-179 in XTR file
    #Trip Activity 
    activityDataBytes['Top Gear - 1 Distance'] = assembledBytes[145:149] 
    activityDataValue['Top Gear - 1 Distance'] = '%0.1f' %(struct.unpack('<L', activityDataBytes['Top Gear - 1 Distance'])[0] * 0.1)
    dataUnits['Top Gear - 1 Distance'] = 'Miles'
    
    #Bytes 180-183 in XTR file
    #Trip Activity 
    activityDataBytes['Top Gear - 1 Fuel'] = assembledBytes[149:153] 
    activityDataValue['Top Gear - 1 Fuel'] = '%0.3f' %(struct.unpack('<L', activityDataBytes['Top Gear - 1 Fuel'])[0] * 0.125)
    dataUnits['Top Gear - 1 Fuel'] = 'Gallons'
  
    #Bytes 184-187 in XTR file
    #Trip Activity 
    activityDataBytes['Top Gear - 1 Time'] = assembledBytes[153:157] 
    secs = struct.unpack('<L', activityDataBytes['Top Gear - 1 Time'])[0]
    activityDataValue['Top Gear - 1 Time'] = '%02d:%02d:%02d' %(secs/3600,secs%3600/60,secs%3600%60)
    dataUnits['Top Gear - 1 Time'] = 'HH:MM:SS'
   
    #Bytes 188 in XTR file
    #Configuration
    activityDataBytes['Top Gear - 1 Ratio'] = assembledBytes[157] 
    activityDataValue['Top Gear - 1 Ratio'] = activityDataBytes['Top Gear - 1 Ratio']
    dataUnits['Top Gear - 1 Ratio'] = 'RPM/MPH'
    
    #Bytes 189-192 in DDEC4 XTR file 
    #Not in DDEC Reports
    activityDataBytes['Top Gear - 1 Time Stamp'] = assembledBytes[158:162]
    activityDataValue['Top Gear - 1 Time Stamp'] = processSecondsForTime(activityDataBytes['Top Gear - 1 Time Stamp'])
    dataUnits['Top Gear - 1 Time Stamp'] = 'Time Stamp'
    
    #Bytes 193-196 in XTR file
    #Trip Activity 
    activityDataBytes['Top Gear Cruise Distance'] = assembledBytes[162:166] 
    activityDataValue['Top Gear Cruise Distance'] = '%0.1f' %(struct.unpack('<L', activityDataBytes['Top Gear Cruise Distance'])[0] * 0.1)
    dataUnits['Top Gear Cruise Distance'] = 'Miles'
    
    #Bytes 197-200 in XTR file
    #Trip Activity 
    activityDataBytes['Top Gear Cruise Fuel'] = assembledBytes[166:170] 
    activityDataValue['Top Gear Cruise Fuel'] = '%0.3f' %(struct.unpack('<L', activityDataBytes['Top Gear Cruise Fuel'])[0] * 0.125)
    dataUnits['Top Gear Cruise Fuel'] = 'Gallons'
   
    #Bytes 201-204 in XTR file
    #Trip Activity 
    activityDataBytes['Top Gear Cruise Time'] = assembledBytes[170:174] 
    secs = struct.unpack('<L', activityDataBytes['Top Gear Cruise Time'])[0]
    activityDataValue['Top Gear Cruise Time'] = '%02d:%02d:%02d' %(secs/3600,secs%3600/60,secs%3600%60)
    dataUnits['Top Gear Cruise Time'] = 'HH:MM:SS'
    
    
    #Bytes 205-208 in XTR file
    #Not in DDEC Reports
    activityDataBytes['RSG Distance'] = assembledBytes[174:178] 
    activityDataValue['RSG Distance'] = '%0.1f' %(struct.unpack('<L', activityDataBytes['RSG Distance'])[0] * 0.1)
    dataUnits['RSG Distance'] = 'Miles'
    
    #Bytes 209-212 in XTR file
    #Not in DDEC Reports
    activityDataBytes['RSG Fuel'] = assembledBytes[178:182] 
    activityDataValue['RSG Fuel'] = '%0.3f' %(struct.unpack('<L', activityDataBytes['RSG Fuel'])[0] * 0.125)
    dataUnits['RSG Fuel'] = 'Gallons'
   
    #Bytes 213-216 in XTR file
    #Not in DDEC Reports
    activityDataBytes['RSG Time'] = assembledBytes[182:186] 
    secs = struct.unpack('<L', activityDataBytes['RSG Time'])[0]
    activityDataValue['RSG Time'] = '%02d:%02d:%02d' %(secs/3600,secs%3600/60,secs%3600%60)
    dataUnits['RSG Time'] = 'HH:MM:SS'
    
    #Bytes 217-220 in XTR file
    #Trip Activity
    activityDataBytes['Stop Idle Fuel'] = assembledBytes[186:190] 
    activityDataValue['Stop Idle Fuel'] = '%0.3f' %(struct.unpack('<L', activityDataBytes['Stop Idle Fuel'])[0] * 0.125)
    dataUnits['Stop Idle Fuel'] = 'Gallons'
   
    #Bytes 221-224 in XTR file
    #Trip Activity
    activityDataBytes['Stop Idle Time'] = assembledBytes[190:194] 
    secs = struct.unpack('<L', activityDataBytes['Stop Idle Time'])[0]
    activityDataValue['Stop Idle Time'] = '%02d:%02d:%02d' %(secs/3600,secs%3600/60,secs%3600%60)
    dataUnits['Stop Idle Time'] = 'HH:MM:SS'
    
    #Bytes 225-228 in XTR file
    #Not in DDEC Reports
    activityDataBytes['Pump Distance'] = assembledBytes[194:198] 
    activityDataValue['Pump Distance'] = '%0.1f' %(struct.unpack('<L', activityDataBytes['Pump Distance'])[0] * 0.1)
    dataUnits['Pump Distance'] = 'Miles'
    
    #Bytes 229-232 in XTR file
    #Not in DDEC Reports
    activityDataBytes['Pump Fuel'] = assembledBytes[198:202] 
    activityDataValue['Pump Fuel'] = '%0.3f' %(struct.unpack('<L', activityDataBytes['Pump Fuel'])[0] * 0.125)
    dataUnits['Pump Fuel'] = 'Gallons'
   
    #Bytes 233-236 in XTR file
    #Not in DDEC Reports
    activityDataBytes['Pump Time'] = assembledBytes[202:206] 
    secs = struct.unpack('<L', activityDataBytes['Pump Time'])[0]
    activityDataValue['Pump Time'] = '%02d:%02d:%02d' %(secs/3600,secs%3600/60,secs%3600%60)
    dataUnits['Pump Time'] = 'HH:MM:SS'
   
    #Bytes 237-240 in XTR file
    #Not in DDEC Reports
    activityDataBytes['Engine Brake Time'] = assembledBytes[206:210] 
    secs = struct.unpack('<L', activityDataBytes['Engine Brake Time'])[0]
    activityDataValue['Engine Brake Time'] = '%02d:%02d:%02d' %(secs/3600,secs%3600/60,secs%3600%60)
    dataUnits['Engine Brake Time'] = 'HH:MM:SS'
   
    #Bytes 241-244 in XTR file
    #Trip Activity
    activityDataBytes['Engine Fan Time'] = assembledBytes[210:214] 
    secs = struct.unpack('<L', activityDataBytes['Engine Fan Time'])[0]
    activityDataValue['Engine Fan Time'] = '%02d:%02d:%02d' %(secs/3600,secs%3600/60,secs%3600%60)
    dataUnits['Engine Fan Time'] = 'HH:MM:SS'
   
    #Bytes 245-248 in XTR file
    #Trip Activity
    activityDataBytes['Manual Fan Time'] = assembledBytes[214:218] 
    secs = struct.unpack('<L', activityDataBytes['Manual Fan Time'])[0]
    activityDataValue['Manual Fan Time'] = '%02d:%02d:%02d' %(secs/3600,secs%3600/60,secs%3600%60)
    dataUnits['Manual Fan Time'] = 'HH:MM:SS'
  
    #Bytes 249-252 in XTR file
    #Trip Activity
    activityDataBytes['A/C Fan Time'] = assembledBytes[218:222] 
    secs = struct.unpack('<L', activityDataBytes['A/C Fan Time'])[0]
    activityDataValue['A/C Fan Time'] = '%02d:%02d:%02d' %(secs/3600,secs%3600/60,secs%3600%60)
    dataUnits['A/C Fan Time'] = 'HH:MM:SS'
   
     #TODO Need DPF time if DDEC 5 or above      
   
    #Bytes 253-256 in XTR file
    #Optimized Idle
    activityDataBytes['Opt. Idle Armed Time'] = assembledBytes[222:226] 
    secs = struct.unpack('<L', activityDataBytes['Opt. Idle Armed Time'])[0]
    activityDataValue['Opt. Idle Armed Time'] = '%02d:%02d:%02d' %(secs/3600,secs%3600/60,secs%3600%60)
    dataUnits['Opt. Idle Armed Time'] = 'HH:MM:SS'
   
    #Bytes 257-260 in XTR file
    activityDataBytes['Opt. Idle Run Time'] = assembledBytes[226:230] 
    secs = struct.unpack('<L', activityDataBytes['Opt. Idle Run Time'])[0]
    activityDataValue['Opt. Idle Run Time'] = '%02d:%02d:%02d' %(secs/3600,secs%3600/60,secs%3600%60)
    dataUnits['Opt. Idle Run Time'] = 'HH:MM:SS'
   
    #Bytes 261-264 in XTR file
    activityDataBytes['Opt. Idle Battery Time'] = assembledBytes[230:234] 
    secs = struct.unpack('<L', activityDataBytes['Opt. Idle Battery Time'])[0]
    activityDataValue['Opt. Idle Battery Time'] = '%02d:%02d:%02d' %(secs/3600,secs%3600/60,secs%3600%60)
    dataUnits['Opt. Idle Battery Time'] = 'HH:MM:SS'
   
    #Bytes 265-268 in XTR file
    activityDataBytes['Opt. Idle Engine Temp Time'] = assembledBytes[234:238] 
    secs = struct.unpack('<L', activityDataBytes['Opt. Idle Engine Temp Time'])[0]
    activityDataValue['Opt. Idle Engine Temp Time'] = '%02d:%02d:%02d' %(secs/3600,secs%3600/60,secs%3600%60)
    dataUnits['Opt. Idle Engine Temp Time'] = 'HH:MM:SS'
   
    #Bytes 269-272 in XTR file
    activityDataBytes['Opt. Idle Thermostat Time'] = assembledBytes[238:242] 
    secs = struct.unpack('<L', activityDataBytes['Opt. Idle Thermostat Time'])[0]
    activityDataValue['Opt. Idle Thermostat Time'] = '%02d:%02d:%02d' %(secs/3600,secs%3600/60,secs%3600%60)
    dataUnits['Opt. Idle Thermostat Time'] = 'HH:MM:SS'

    #Bytes 273-276 in XTR file
    activityDataBytes['Opt. Idle Extended Time'] = assembledBytes[242:246] 
    secs = struct.unpack('<L', activityDataBytes['Opt. Idle Extended Time'])[0]
    activityDataValue['Opt. Idle Extended Time'] = '%02d:%02d:%02d' %(secs/3600,secs%3600/60,secs%3600%60)
    dataUnits['Opt. Idle Extended Time'] = 'HH:MM:SS'
   
    #Bytes 277-280 in XTR file
    activityDataBytes['Opt. Idle Continuous Time'] = assembledBytes[246:250] 
    secs = struct.unpack('<L', activityDataBytes['Opt. Idle Continuous Time'])[0]
    activityDataValue['Opt. Idle Continuous Time'] = '%02d:%02d:%02d' %(secs/3600,secs%3600/60,secs%3600%60)
    dataUnits['Opt. Idle Continuous Time'] = 'HH:MM:SS'
   
    #Bytes 281-284 in XTR file
    activityDataBytes['Peak Road Speed Time Stamp'] = assembledBytes[250:254]
    activityDataValue['Peak Road Speed Time Stamp'] = processSecondsForTime(activityDataBytes['Peak Road Speed Time Stamp'])
    dataUnits['Peak Road Speed Time Stamp'] = 'Time Stamp'
    
    #Bytes 285-288 in XTR file
    activityDataBytes['Peak Engine Speed Time Stamp'] = assembledBytes[254:258]
    activityDataValue['Peak Engine Speed Time Stamp'] = processSecondsForTime(activityDataBytes['Peak Road Speed Time Stamp'])
    dataUnits['Peak Engine Speed Time Stamp'] = 'Time Stamp'
   
     #Bytes 289-292 in XTR file
    activityDataBytes['Start Time Stamp'] = assembledBytes[258:262]
    activityDataValue['Start Time Stamp'] = processSecondsForTime(activityDataBytes['Start Time Stamp'])
    dataUnits['Start Time Stamp'] = 'Time Stamp'
    
    #Bytes 293-296 in XTR file
    #Not in DDEC Reports
    activityDataBytes['Start Odometer'] = assembledBytes[262:266] 
    activityDataValue['Start Odometer'] = '%0.1f' %(struct.unpack('<L', activityDataBytes['Start Odometer'])[0] * 0.1)
    dataUnits['Start Odometer'] = 'Miles'
    
    #Bytes 297-298
    activityDataBytes['Over Speed A Count'] = assembledBytes[266:268]
    activityDataValue['Over Speed A Count'] = struct.unpack('<H',activityDataBytes['Over Speed A Count'])[0] 
    dataUnits['Over Speed A Count'] = 'Count (max 65535)'    
   
    #Bytes 299-300
    activityDataBytes['Over Speed B Count'] = assembledBytes[268:270]
    activityDataValue['Over Speed B Count'] = struct.unpack('<H',activityDataBytes['Over Speed B Count'])[0] 
    dataUnits['Over Speed B Count'] = 'Count (max 65535)'    
    
    #Bytes 301-302
    activityDataBytes['Over Rev Count'] = assembledBytes[270:272]
    activityDataValue['Over Rev Count'] = struct.unpack('<H',activityDataBytes['Over Rev Count'])[0] 
    dataUnits['Over Rev Count'] = 'Count (max 65535)'    
    
    #Bytes 303-306 in XTR file
    activityDataBytes['Brake Count'] = assembledBytes[272:276] 
    activityDataValue['Brake Count'] = struct.unpack('<L', activityDataBytes['Brake Count'])[0] 
    dataUnits['Brake Count'] = 'Count (max 2^32)'
    
    #Bytes 307-308 in XTR file
    activityDataBytes['Hard Brake Count'] = assembledBytes[276:278] 
    activityDataValue['Hard Brake Count'] = struct.unpack('<H', activityDataBytes['Hard Brake Count'])[0] 
    dataUnits['Hard Brake Count'] = 'Count (max 65535)'
    
    #Bytes 309-312 in XTR file
    activityDataBytes['Braking Velocity Energy'] = assembledBytes[278:282] 
    activityDataValue['Braking Velocity Energy'] = struct.unpack('<L', activityDataBytes['Braking Velocity Energy'])[0] 
    dataUnits['Braking Velocity Energy'] = 'Sum energy'
    
    #Bytes 313-316 in XTR file
    #Bug in csv exporter with data representation
    activityDataBytes['Crank Shaft Revolutions'] = assembledBytes[282:286] 
    activityDataValue['Crank Shaft Revolutions'] = struct.unpack('<L', activityDataBytes['Crank Shaft Revolutions'])[0] 
    dataUnits['Crank Shaft Revolutions'] = 'Count (max 2^32)'
    
    #Bytes 317-318 in XTR file
    activityDataBytes['Diagnostic Alerts'] = assembledBytes[286:288] 
    activityDataValue['Diagnostic Alerts'] = struct.unpack('<H', activityDataBytes['Diagnostic Alerts'])[0] 
    dataUnits['Diagnostic Alerts'] = 'Count (max 65535)'
    
    #Byte 319 in XTR file
    activityDataBytes['Average Drive Load'] = assembledBytes[288] 
    activityDataValue['Average Drive Load'] = activityDataBytes['Average Drive Load']
    dataUnits['Average Drive Load'] = '% max load'
    
    return activityDataBytes,activityDataValue,dataUnits

def prettyPrintEventData(eventDataValue,caption):
    htmlString =  '<table width="100%" border="1" cellspacing="1" cellpadding="2">\n'
    htmlString += ' <caption> %s </caption>\n' %caption
    htmlString += '  <tr>\n     '
    htmlString += '    <th colspan="4">Event Time: %s</th> <th colspan="5" aligh="right">Event Odometer: %s Miles</th> \n' %(eventDataValue['Incident Time'],eventDataValue['Incident Odometer'])
    htmlString += '  </tr>\n     '
    htmlString += '  <tr>\n'
    htmlString += '    <td>Time (sec)</td> <td>Vehicle Speed (MPH)</td> <td>Engine Speed (RPM)</td> <td>Brake</td> <td>Clutch</td> <td>Engine Load (%)</td> <td>Throttle (%)</td>  <td>Cruise</td>  <td>Diag. Code</td>\n'
    htmlString += '  </tr>\n'
    
    for t,sp,rpm,br,cl,el,th,cr,dc in zip(eventDataValue['Time'],
                                          eventDataValue['Road Speed'],
                                          eventDataValue['Engine Speed'],
                                          eventDataValue['Brake Switch'],
                                          eventDataValue['Clutch Switch'],
                                          eventDataValue['Engine Load'],
                                          eventDataValue['Throttle'],
                                          eventDataValue['Cruise Switch'],
                                          eventDataValue['Diagnostic Code']):
        htmlString += '  <tr>\n'
        htmlString += '    <td>%d</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td>\n' %(t,sp,rpm,br,cl,el,th,cr,dc)
        htmlString += '  </tr>\n'                                   
    
    
    htmlString += '</table>\n<p>\n'

    return htmlString
    
    
    
    
def prettyPrintBandedTable(table,caption,leftband=['1','2','3','4','5','6','7','8','9','10','Total'],topband=['Engine RPM','A','B','C','D','E','F','G','H','I','J','Total']):
    
    htmlString =  '<table width="100%" border="1" cellspacing="1" cellpadding="2">\n'
    htmlString += ' <caption> %s </caption>\n' %caption
    htmlString += '  <tr>\n     '
    for entry in topband:    
        htmlString += '<th>%s</th> '%entry
    htmlString += '\n  </tr>\n'
    for j in range(len(table)):
        htmlString += '  <tr>\n     '
        htmlString += '<td>%s</td> ' %leftband[j]
        total=0
        for k in range(len(table[0])):
            entry=table[j][k]            
            total+=float(entry)            
            htmlString += '<td>%s</td> ' %table[j][k]  
        htmlString += '<td>%0.2f</td>\n' %total
        htmlString += '  </tr>\n'
    
    htmlString += '</table>\n<p>\n'

    return htmlString
    
    
    
def prettyPrintDailyUse(dailyUseBytes,dailyUseValue,dailyUseUnits):
    htmlString =  '<table width="100%" border="1" cellspacing="1" cellpadding="2">\n'
    htmlString += ' <caption> Daily Engine Usage Log </caption>\n'
    htmlString += '  <tr>\n'
    htmlString += '    <th rowspan="2">Start Day and Time (UTC)</th> <th>Odometer</th>   <th>Distance</th>   <th>Fuel</th>      <th colspan="2">Total Minutes</th>  <th colspan="2">00:00-02:00</th> <th colspan="2">02:00-04:00</th>  <th colspan="2">04:00-06:00</th>  <th colspan="2">06:00-08:00</th>  <th colspan="2">08:00-10:00</th>  <th colspan="2">10:00-12:00</th>  <th colspan="2">12:00-14:00</th>  <th colspan="2">14:00-16:00</th>  <th colspan="2">16:00-18:00</th>  <th colspan="2">18:00-20:00</th>  <th colspan="2">20:00-22:00</th>  <th colspan="2">22:00-24:00</th> \n'
    htmlString += '  </tr>\n'
    htmlString += '  <tr>\n'
    htmlString += '                                                  <td>Miles</td>      <td>Miles</td>       <td>(Gallons)</td> <th>Idle</th>     <th>Drive</th> <th>Idle</th>     <th>Drive</th>  <th>Idle</th>     <th>Drive</th>  <th>Idle</th>     <th>Drive</th>  <th>Idle</th>     <th>Drive</th>  <th>Idle</th>     <th>Drive</th>  <th>Idle</th>     <th>Drive</th>  <th>Idle</th>     <th>Drive</th>  <th>Idle</th>     <th>Drive</th>  <th>Idle</th>     <th>Drive</th>  <th>Idle</th>     <th>Drive</th>  <th>Idle</th>     <th>Drive</th>  <th>Idle</th>     <th>Drive</th>  \n'
    htmlString += '  </tr>\n'
     
    for day,odometer,distance,fuel,i1,i2,i3,i4,i5,i6,i7,i8,i9,i10,i11,i12,d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11,d12 in zip(dailyUseValue['Start Time'],
                                                                                                                        dailyUseValue['Odometer'],
                                                                                                                        dailyUseValue['Distance'],
                                                                                                                        dailyUseValue['Fuel'],
                                                                                                                        dailyUseValue['Idle Time 00:00-02:00'],
                                                                                                                        dailyUseValue['Idle Time 02:00-04:00'],
                                                                                                                        dailyUseValue['Idle Time 04:00-06:00'],
                                                                                                                        dailyUseValue['Idle Time 06:00-08:00'],
                                                                                                                        dailyUseValue['Idle Time 08:00-10:00'],
                                                                                                                        dailyUseValue['Idle Time 10:00-12:00'],
                                                                                                                        dailyUseValue['Idle Time 12:00-14:00'],
                                                                                                                        dailyUseValue['Idle Time 14:00-16:00'],
                                                                                                                        dailyUseValue['Idle Time 16:00-18:00'],
                                                                                                                        dailyUseValue['Idle Time 18:00-20:00'],
                                                                                                                        dailyUseValue['Idle Time 20:00-22:00'],
                                                                                                                        dailyUseValue['Idle Time 22:00-24:00'],
                                                                                                                        dailyUseValue['Drive Time 00:00-02:00'],
                                                                                                                        dailyUseValue['Drive Time 02:00-04:00'],
                                                                                                                        dailyUseValue['Drive Time 04:00-06:00'],
                                                                                                                        dailyUseValue['Drive Time 06:00-08:00'],
                                                                                                                        dailyUseValue['Drive Time 08:00-10:00'],
                                                                                                                        dailyUseValue['Drive Time 10:00-12:00'],
                                                                                                                        dailyUseValue['Drive Time 12:00-14:00'],
                                                                                                                        dailyUseValue['Drive Time 14:00-16:00'],
                                                                                                                        dailyUseValue['Drive Time 16:00-18:00'],
                                                                                                                        dailyUseValue['Drive Time 18:00-20:00'],
                                                                                                                        dailyUseValue['Drive Time 20:00-22:00'],
                                                                                                                        dailyUseValue['Drive Time 22:00-24:00']):
        totalIdle  = int(i1)+int(i2)+int(i3)+int(i4)+int(i5)+int(i6)+int(i7)+int(i8)+int(i9)+int(i10)+int(i11)+int(i12)                                                                                                                        
        totalDrive = int(d1)+int(d2)+int(d3)+int(d4)+int(d5)+int(d6)+int(d7)+int(d8)+int(d9)+int(d10)+int(d11)+int(d12)                                                                                                                        
        htmlString += '  <tr>\n'
        htmlString += '    <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%d</td> <td>%d</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> \n' %(day[:-5],odometer,distance,fuel,totalIdle,totalDrive,i1,d1,i2,d2,i3,d3,i4,d4,i5,d5,i6,d6,i7,d7,i8,d8,i9,d9,i10,d10,i11,d11,i12,d12)
        htmlString += '  </tr>\n'
        
    htmlString += '</table>\n<p>\n'

    return htmlString

def prettyPrintDict(DataValue,DataUnits,DataBytes,caption='Example Caption',DataPID=False):
    htmlString =  '<table width="100%" border="1" cellspacing="1" cellpadding="2">\n'
    htmlString += '<caption>&nbsp;\n'
    htmlString += caption
    htmlString += '\n</caption>\n\n'    
    htmlString += '  <tr>\n'
    htmlString += '    <th>Parameter</th>   <th>Value</th> <th>Units</th> <th>Data Source</th> <th>Raw Hex Bytes</th>\n' 
    htmlString += '  </tr>\n'
    htmlString += '  <tr>\n'
    for key in sorted(DataValue):
        htmlString +='  <tr>\n'
        #print(key, end='\t')
        
        htmlString +='    <th scope="row", align="left">&nbsp;'
        htmlString +=key
        htmlString +='</th>\n'
        
       # print(dataValue[key], end = ' ' )
        htmlString +='    <td>&nbsp;'
        htmlString +=str(DataValue[key])
        htmlString +='</td>\n'
            
        htmlString +='    <td>&nbsp;'
        try:
             htmlString +=DataUnits[key]
        except KeyError:
            pass
        htmlString +='</td>\n'
         
       
        htmlString +='    <td>&nbsp;'
        try:
            htmlString +='PID = %d' %DataPID[key]
        except:
            htmlString +='ECM Memory'
        htmlString +='</td>\n'
       
        htmlString +='    <td>&nbsp;'
        try:
            if isinstance(DataBytes[key],int):
                htmlString +='%02X ' %DataBytes[key]
               
            else:
                for d in DataBytes[key]:
                    htmlString +='%02X ' %d
        except KeyError:
            pass
        htmlString +='</td>\n'
    
        htmlString +='  </tr>\n\n'
    htmlString += '</table>\n<p>\n'
    return htmlString

def prettyPrintDiagnostics(diagnosticValue,diagnosticUnits,caption='Diagnostic Data'):
    htmlString =  '<table width="100%" border="1" cellspacing="1" cellpadding="2">\n'
    htmlString += '<caption>&nbsp;\n'
    htmlString += caption
    htmlString += '\n</caption>\n\n'    
    htmlString += '  <tr>\n'
    htmlString += '    <th colspan="4">Diagnostic Code: %s</th>   <th colspan="9"> Diagnostic Time: %s</th><td>Units</td>\n' %(diagnosticValue['Diagnostic Code'],diagnosticValue['Diagnostic Time'])
    htmlString += '  </tr>\n'
    htmlString += '  <tr>\n'
    htmlString += '    <td>Time Before Fault</th>   <td>0</td> <td>5</td> <td>10</td> <td>15</td> <td>20</td> <td>25</td> <td>30</td> <td>35</td> <td>40</td> <td>45</td> <td>50</td> <td>55</td> <td>Seconds</td>\n' 
    htmlString += '  </tr>\n'
    for key in sorted(diagnosticValue):
      if key not in ['Diagnostic Time', 'Diagnostic Code','EngineBrake']:
        htmlString +='  <tr>\n'
        #print(key, end='\t')
        
        htmlString +='    <th scope="row", align="left">&nbsp;'
        htmlString +=key
        htmlString +='</th>\n'
        
        #print(dataValue[key], end = ' ' )
        
        for dv in diagnosticValue[key]:
            htmlString +='    <td>&nbsp;'
            htmlString +=str(dv)
            htmlString +='</td>\n'
            
        try:
            print(diagnosticUnits[key])
        except KeyError:
            diagnosticUnits[key]=''
        htmlString +='    <td>&nbsp;'
        htmlString +=diagnosticUnits[key]
        htmlString +='</td>\n'
        
        htmlString +='  </tr>\n\n'
        
        
    htmlString += '</table>\n<p>\n'
    return htmlString
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#Standards based data

htmlString=''


dataPID={}
dataBytes={}
dataValue={}
dataUnits={}
dataComment={}

name = 'Maximum Road Speed Limit'
dataPID[name]=74
ecmData,allNetworkData = getJ1587(dataPID[name],name,False)
dataBytes[name] = ecmData 
dataValue[name] = '%0.1f' %(struct.unpack('B', ecmData)[0] * 0.5)
dataUnits[name] = 'MPH'

name = 'Cruise Control High-Set Limit Speed'
dataPID[name]=87
ecmData,allNetworkData = getJ1587(dataPID[name],name,False)
dataBytes[name] = ecmData 
dataValue[name] = '%0.1f' %(struct.unpack('B', ecmData)[0] * 0.5)
dataUnits[name] = 'MPH'

name = 'Cruise Control Low-Set Limit Speed'
dataPID[name]=88
ecmData,allNetworkData = getJ1587(dataPID[name],name,False)
dataBytes[name] = ecmData 
dataValue[name] = '%0.1f' %(struct.unpack('B', ecmData)[0] * 0.5)
dataUnits[name] = 'MPH'

name = 'Governor Droop'
dataPID[name]=113
ecmData,allNetworkData = getJ1587(dataPID[name],name,False)
dataBytes[name] = ecmData 
dataValue['Governor Droop'] = '%0.1f' %(struct.unpack('B', ecmData)[0] * 2.0)
dataUnits['Governor Droop'] = 'RPM'

name = 'Rated Engine Power'
dataPID[name]=166
ecmData,allNetworkData = getJ1587(dataPID[name],name,False)
dataBytes[name] = ecmData 
dataValue[name] = '%d' %(struct.unpack('<H', ecmData)[0] )
dataUnits[name] = 'Horsepower'

name = 'Battery Voltage'
dataPID[name]=168
ecmData,allNetworkData = getJ1587(dataPID[name],name,False)
if ecmData:
    dataBytes[name] = ecmData 
    dataValue[name] = '%0.2f' %(struct.unpack('<H', ecmData)[0] * 0.05 )
    dataUnits[name] = 'Volts'

name = 'Trip Fuel'
dataPID[name]=182
ecmData,allNetworkData = getJ1587(dataPID[name],name,False)
dataBytes[name] = ecmData 
dataValue[name] = '%0.3f' %(struct.unpack('<H', ecmData)[0] * 0.125)
dataUnits[name] = 'Gallons'


name = 'Idle Engine Speed'
dataPID[name]=188
ecmData,allNetworkData = getJ1587(dataPID[name],name,False)
dataBytes[name] = ecmData 
dataValue[name] = '%d' %(struct.unpack('<H', ecmData)[0] * 0.25)
dataUnits[name] = 'RPM'

name = 'Rated Engine Speed'
dataPID[name]=189
ecmData,allNetworkData = getJ1587(dataPID[name],name,False)
dataBytes[name] = ecmData 
dataValue[name] = '%d' %(struct.unpack('<H', ecmData)[0] * 0.25)
dataUnits[name] = 'RPM'

name = 'Speed Sensor Calibration'
dataPID[name]=228
ecmData,allNetworkData = getJ1587(dataPID[name],name,False)
dataBytes[name] = ecmData 
dataValue[name] = '%d' %(struct.unpack('<L', ecmData)[0] )
dataUnits[name] = 'pulses per mile'

name = 'Unit Number'
dataPID[name]=233
ecmData,allNetworkData = getJ1587(dataPID[name],name,False)
dataBytes[name] = ecmData 
dataValue[name] = str(ecmData,'ascii')
dataUnits[name] = 'Alphanumeric'

name = 'Software Identification'
dataPID[name]=234
ecmData,allNetworkData = getJ1587(dataPID[name],name,False)
dataBytes[name] = ecmData 
dataValue[name] = str(ecmData,'ascii')
dataUnits[name] = 'Alphanumeric'

name = 'Total Idle Hours'
dataPID[name]=235
ecmData,allNetworkData = getJ1587(dataPID[name],name,False)
dataBytes[name] = ecmData 
secs = struct.unpack('<L', ecmData)[0] * 0.05 * 3600
dataValue[name] = '%02d:%02d:%02d' %(secs/3600,secs%3600/60,secs%3600%60) 
dataUnits[name] = 'HH:MM:SS'

name = 'Total Idle Fuel Used'
dataPID[name]=236
ecmData,allNetworkData = getJ1587(dataPID[name],name,False)
dataBytes[name] = ecmData 
dataValue[name] = '%0.3f' %(struct.unpack('<L', ecmData)[0] * 0.125)
dataUnits[name] = 'Gallons'

name = 'Vehicle Identification Number'
dataPID[name]=237
ecmData,allNetworkData = getJ1587(dataPID[name],name,False)
dataBytes[name] = ecmData 
dataValue[name] = str(ecmData,'ascii')
dataUnits[name] = 'Alphanumeric'

name = 'Time Since Last ECM Reprogram' #Reference ch6_mbe_ec_c13.pdf
dataPID[name]=240
ecmData,allNetworkData = getJ1587(dataPID[name],name,False)
dataBytes[name] = ecmData 
secs = struct.unpack('<L', ecmData)[0] * 0.05 * 3600
dataValue[name] = '%02d:%02d:%02d' %(secs/3600,secs%3600/60,secs%3600%60)
dataUnits[name] = 'HH:MM:SS'

name = 'Component Information - MID'
dataPID[name]=243
ecmData,allNetworkData = getJ1587(dataPID[name],name,True)
dataBytes[name] = ecmData
dataValue[name] = '%d' %ecmData[0]
dataUnits[name] = 'Number'

name = 'Component Information - Make'
dataPID[name]=243
#dataBytes[name] = ecmData
text=str(ecmData[1:],'ascii').split('*')
dataValue[name] = text[0]
dataUnits[name] = 'Alphanumeric'

name = 'Component Information - Model'
dataPID[name]=243
dataValue[name] = text[1]
dataUnits[name] = 'Alphanumeric'

name = 'Component Information - Serial No.'
dataPID[name]=243
dataValue[name] = text[2]
dataUnits[name] = 'Alphanumeric'

name = 'Trip Miles'
dataPID[name]=244
ecmData,allNetworkData = getJ1587(dataPID[name],name,False)
dataBytes[name] = ecmData 
dataValue[name] = '%0.1f' %(struct.unpack('<L', ecmData)[0] * 0.1 )
dataUnits[name] = 'Miles'

name = 'Total Miles'
dataPID[name]=245
ecmData,allNetworkData = getJ1587(dataPID[name],name,False)
dataBytes[name] = ecmData 
dataValue[name] = '%0.1f' %(struct.unpack('<L', ecmData)[0] * 0.1 )
dataUnits[name] = 'Miles'

name = 'Total Engine Hours' #
dataPID[name]=247
ecmData,allNetworkData = getJ1587(dataPID[name],name,False)
dataBytes[name] = ecmData 
secs = struct.unpack('<L', ecmData)[0] * 0.05 * 3600
dataValue[name] = '%02d:%02d:%02d' %(secs/3600,secs%3600/60,secs%3600%60)
dataUnits[name] = 'HH:MM:SS'
dataComment[name] = 'Time is accumulated while the engine speed is above 60 rpm.'

name = 'Total PTO Hours' 
dataPID[name]=248
ecmData,allNetworkData = getJ1587(dataPID[name],name,False)
dataBytes[name] = ecmData 
secs = struct.unpack('<L', ecmData)[0] * 0.05 * 3600
dataValue[name] = '%02d:%02d:%02d' %(secs/3600,secs%3600/60,secs%3600%60)
dataUnits[name] = 'HH:MM:SS'
dataComment[name] = 'Hand throttle or high idle.'

#name = 'Total Engine Revolutions' 
#dataPID[name]=249
#ecmData,allNetworkData = getJ1587(dataPID[name],name,False)
#dataBytes[name] = ecmData 
#try:
#    dataValue[name] = '%d' %(struct.unpack('<L', ecmData)[0] * 1000)
#except TypeError:
#    dataValue[name] = ecmData
#dataUnits[name] = 'Revolutions'

name = 'Total Fuel Used'
dataPID[name]=250
ecmData,allNetworkData = getJ1587(dataPID[name],name,False)
dataBytes[name] = ecmData 
try:
    dataValue[name] = '%0.3f' %(struct.unpack('<L', ecmData)[0] * 0.125)
except TypeError:
    dataValue[name] = ecmData
dataUnits[name] = 'Gallons'

name = 'ECM Clock' 
dataPID[name]=251
ecmData,allNetworkData = getJ1587(dataPID[name],name,False)
dataBytes[name] = ecmData 
secs =  ecmData[0] * 0.25
mins =  ecmData[1]
hrs  =  ecmData[2]
dataValue[name] = '%02d:%02d:%02d' %(hrs,mins,secs)
dataUnits[name] = 'HH:MM:SS (UTC)'

name = 'ECM Date' 
dataPID[name]=252
ecmData,allNetworkData = getJ1587(dataPID[name],name,False)
dataBytes[name] = ecmData 
day   =  1 + ecmData[0] * 0.25 
month =  ecmData[1]
year  =  ecmData[2] + 1985
dataValue[name] = '%02d/%02d/%04d' %(month,day,year)
dataUnits[name] = 'Month/Day/Year'


requests = [b'\x00\xc8\x07\x04\x06\x00\x46\x41\x41\x5a\x05\x48',
            b'\x00\xc8\x07\x04\x01\x00\x46\x41\x41\x5a\xcd\x09',
            b'\x00\xc8\x07\x04\x0e\x00\x46\x41\x41\x5a\x08\x0a',
            b'\x00\xc8\x07\x04\x06\x00\x46\x41\x41\x5a\x05\x48',
            b'\x00\xc8\x07\x04\x0f\x00\x46\x41\x41\x5a\x4d\xaa',
            b'\x00\xc8\x07\x04\x10\x00\x46\x41\x41\x5a\x92\x2d',
            b'\x00\xc8\x07\x04\x0c\x00\x46\x41\x41\x5a\x83\x4a',
            b'\x00\xc8\x07\x04\x14\x00\x46\x41\x41\x5a\x94\x8c',
            b'\x00\xc8\x07\x04\x02\x00\x46\x41\x41\x5a\x03\xe9',
            b'\x00\xc8\x07\x04\x04\x00\x46\x41\x41\x5a\x8e\x08']

    
           
sendDataLinkEscape()
i=0

newXTRfile = open('DDEC4Download.XTR','wb')
newXTRfile.write(b'\x44\x44\x45\x43\x31\x00\x01\x00\x5B\x16\x00\x00\x08\x80\x44\x44\x45\x43\x20\x49\x56\x05\x32\x36\x2E\x30\x30\xB9\xE8\xDA\x35\x00\x0A\x04\x0A\x00\x2C\x00\x01\x5F\x82\xE8\x0B\x00\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x54\x49\x42\x20\x44\x44\x45\x43\x34\x00\x89\x3D\xC8\x00\x15\xF9\x35\x1C\x30\x36\x52\x30\x34\x39\x39\x35\x33\x34')

for request in requests:       
    assembledBytes=b''
    transportSendRequest(request)
    filename='DDECReturnBytes-1-%d.bin' %i
    assembledBytes = transportGetMessage(filename)
    print(assembledBytes)
    if i>0:
        newXTRfile.write(assembledBytes[51:-2])
    
    if i==0: #request == b'\x00\xc8\x07\x04\x06\x00\x46\x41\x41\x5a\x05\x48': #Request 0 and 3
        #Bytes 0-4  in DDEC4 XTR file are file identifier 'DDEC1'
        #Byte 5 is null 0x00
        #Bytes 6 and 7 are a record number indicator in little endian 0x01 0x00 = 1
        #bytes 8-11 is the file size in bytes after this word: 0x5B 0x16 0x00 0x00 = 5723 + 12 = 5735 (total bytes)
        #Byte 12 is a control byte (8 = length of the next data field)
        #Byte 13 is the MID of the Engine (0x80)
        #Bytes 14-20 is the Controller identifier ('DDEC IV') 
        #Byte 21 is a  control byte (5 = length of the next data field)
        #Bytes 22-26 in DDEC4 XTR file
        dataBytes['ECM Software Version'] = assembledBytes[93:98]
        dataValue['ECM Software Version'] = str(dataBytes['ECM Software Version'],'ascii')
        dataUnits['ECM Software Version'] = 'Alphanumeric'  
       
        #Bytes 27-32 did not change the csv output file
        
        #Byte 33 is reset status
        #Bytes 34-38 re control bytes and do not change the DDEC Reports generated CSV file
        
        #Byte 39 changes the utilization sections which makes me think it has something to do with the calendar time of extraction.
        
        #Bytes 40-43 in DDEC4 XTR file      
        dataBytes['Current Engine Hours'] = assembledBytes[9:13]
        dataValue['Current Engine Hours'] = struct.unpack('<L', dataBytes['Current Engine Hours'])[0] * 0.05
        dataUnits['Current Engine Hours'] = 'Hours'        
        
        #Bytes 44-52 in DDEC4 XTR file
        dataBytes['Driver Identifier'] = assembledBytes[13:23]
        dataValue['Driver Identifier'] = str(dataBytes['Driver Identifier'],'ascii')
        dataUnits['Driver Identifier'] = 'Alphanumeric'
        
        #Bytes 54-62 in DDEC4 XTR file
        dataBytes['Vehicle Identifier'] = assembledBytes[23:33]
        dataValue['Vehicle Identifier'] = str(dataBytes['Vehicle Identifier'],'ascii')
        dataUnits['Vehicle Identifier'] = 'Alphanumeric'
        
        
        #Bytes 68-71 in DDEC4 XTR file  
        dataBytes['ECM Time Stamp at Extraction'] = assembledBytes[37:41]
        dataValue['ECM Time Stamp at Extraction'] = processSecondsForTime(dataBytes['ECM Time Stamp at Extraction'])
        dataUnits['ECM Time Stamp at Extraction'] = 'Time Stamp'
        
        #Bytes 72-81 in DDEC4 XTR File
        dataBytes['Engine Serial Number'] = assembledBytes[41:51]
        dataValue['Engine Serial Number'] = str(dataBytes['Engine Serial Number'],'ascii')
        dataUnits['Engine Serial Number'] = 'Alphanumeric'        
        
        #Bytes 82-86 are control bytes     
       
    elif i==1: #request == b'\x00\xc8\x07\x04\x01\x00\x46\x41\x41\x5a\xcd\x09':   #Request #1 
       tripDataValue={}
       
       tripDataBytes,tripDataValue,tripDataUnits = getDDEC4ActivityData(assembledBytes)   
        
       #The last 2 bytes in this data stream do not show up in the XTR file
         
    elif i==2: #request == b'\x00\xc8\x07\x04\x0e\x00\x46\x41\x41\x5a\x08\x0a': #request # 2
        #Monthly Activity - 1
        #Block 51-60 in the J1708 data corresponds to block 320 - 329 in the XTR file. It's not clear what those bytes mean.
        
        Month1DataBytes,Month1DataValue,Month1DataUnits = getDDEC4ActivityData(assembledBytes) 
        
        Month2DataBytes,Month2DataValue,Month2DataUnits = getDDEC4ActivityData(assembledBytes[228:]) 
      
        Month3DataBytes,Month3DataValue,Month3DataUnits = getDDEC4ActivityData(assembledBytes[456:]) 
        
    elif i == 3: #request ==  b'\x00\xc8\x07\x04\x06\x00\x46\x41\x41\x5a\x05\x48': #request 3     
        
        #Byte 1019 in XTR file
         
        #byte 1020 -> unreadable file
        #byte 1021 -> time stamp changes
        #byte 1022 -> time stamp changes
        #byte 1023 -> unreadable file 4 bytes (perhaps date of some sort)
        
        #byte 1024-1025 in XTR file
        dataBytes['Over Rev Limit A'] = assembledBytes[61:63]
        dataValue['Over Rev Limit A'] = '%0.2f' %(struct.unpack('<H',dataBytes['Over Rev Limit A'])[0] * 0.25)
        dataUnits['Over Rev Limit A'] = 'RPM'       
        
        #byte 1026 in XTR file
        dataBytes['Over Speed Limit A'] = assembledBytes[63]
        dataValue['Over Speed Limit A'] = '%d' %(dataBytes['Over Speed Limit A'] )
        dataUnits['Over Speed Limit A'] = 'MPH'       
        
        #byte 1027 in XTR file
        dataBytes['Over Speed Limit B'] = assembledBytes[64]
        dataValue['Over Speed Limit B'] = '%d' %(dataBytes['Over Speed Limit B'] )
        dataUnits['Over Speed Limit B'] = 'MPH'       
             
        #bytes 1028-1047 are duplicate of other data: unit number driver number
             
        #byte 1048-1051 in XTR file
        dataBytes['Current Odometer'] = assembledBytes[85:89]
        dataValue['Current Odometer'] = '%0.1f' %(struct.unpack('<L',dataBytes['Current Odometer'])[0] * 0.1)
        dataUnits['Current Odometer'] = 'Miles'       
        
        #byte 1052 in XTR file
        dataBytes['Hard Brake Deceleration Limit'] = assembledBytes[89]
        dataValue['Hard Brake Deceleration Limit'] = '%d' %(dataBytes['Hard Brake Deceleration Limit'] )
        dataUnits['Hard Brake Deceleration Limit'] = 'MPH/sec'       
        
        #byte 1053 in XTR file
        dataBytes['Idle Time Limit (Stop)'] = assembledBytes[90]
        dataValue['Idle Time Limit (Stop)'] = '%d' %(dataBytes['Idle Time Limit (Stop)'] )
        dataUnits['Idle Time Limit (Stop)'] = 'Minutes'       
        
        #byte 1054 in XTR
        dataBytes['Top Gear Ratio'] = assembledBytes[91]
        dataValue['Top Gear Ratio'] = '%d' %(dataBytes['Top Gear Ratio'])
        dataUnits['Top Gear Ratio'] = 'rpm/mph'       
        
        #byte 1055 in XTR file
        dataBytes['Data Hub Device MID'] = assembledBytes[92]
        dataValue['Data Hub Device MID'] = '%d' %(dataBytes['Data Hub Device MID'] )
        dataUnits['Data Hub Device MID'] = 'Numeric'       
        
        #1056-1060 Software ID (duplicate)
        
        #byte 1061
        dataBytes['ECM Type'] = assembledBytes[98]
        dataValue['ECM Type'] = int(dataBytes['ECM Type'])
        if dataValue['ECM Type'] == 4:
            dataValue['ECM Type Name'] = 'DDEC IV'
        elif dataValue['ECM Type'] == 1:
            dataValue['ECM Type Name'] = 'TBD'
        elif dataValue['ECM Type'] == 2:
            dataValue['ECM Type Name'] = 'DDEC II'
        elif dataValue['ECM Type'] == 3:
            dataValue['ECM Type Name'] = 'DDEC III'
        elif dataValue['ECM Type'] == 5:
            dataValue['ECM Type Name'] = 'DDEC V'
        elif dataValue['ECM Type'] == 10:
            dataValue['ECM Type Name'] = 'CPC2 (DDEC VI)'
        elif dataValue['ECM Type'] == 11:
            dataValue['ECM Type Name'] = 'CPC2+ (DDEC 10)'
        elif dataValue['ECM Type'] == 13:
            dataValue['ECM Type Name'] = 'DDEC CPC4'
        elif dataValue['ECM Type'] == 50:
            dataValue['ECM Type Name'] = 'VCU/PLD'
        else:
            dataValue['ECM Type Name'] = 'Unknown'
            
        dataUnits['ECM Type']='Numeric'
        dataUnits['ECM Type Name']='Alphanumeric'
        
        #byte 1062 in XTR file
        dataBytes['Speed Band 1 Limit'] = assembledBytes[99]
        dataValue['Speed Band 1 Limit'] = '%d' %(dataBytes['Speed Band 1 Limit'] )
        dataUnits['Speed Band 1 Limit'] = 'MPH' 
        
        #byte 1063 in XTR file
        dataBytes['Speed Band 2 Limit'] = assembledBytes[100]
        dataValue['Speed Band 2 Limit'] = '%d' %(dataBytes['Speed Band 2 Limit'] )
        dataUnits['Speed Band 2 Limit'] = 'MPH' 
        
        #byte 1064 in XTR file
        dataBytes['Speed Band 3 Limit'] = assembledBytes[101]
        dataValue['Speed Band 3 Limit'] = '%d' %(dataBytes['Speed Band 3 Limit'] )
        dataUnits['Speed Band 3 Limit'] = 'MPH' 
        
        #byte 1065 in XTR file
        dataBytes['Speed Band 4 Limit'] = assembledBytes[102]
        dataValue['Speed Band 4 Limit'] = '%d' %(dataBytes['Speed Band 4 Limit'] )
        dataUnits['Speed Band 4 Limit'] = 'MPH' 
        
        #byte 1066 in XTR file
        dataBytes['Speed Band 5 Limit'] = assembledBytes[103]
        dataValue['Speed Band 5 Limit'] = '%d' %(dataBytes['Speed Band 5 Limit'] )
        dataUnits['Speed Band 5 Limit'] = 'MPH' 
        
        #byte 1067 in XTR file
        dataBytes['Speed Band 6 Limit'] = assembledBytes[104]
        dataValue['Speed Band 6 Limit'] = '%d' %(dataBytes['Speed Band 6 Limit'] )
        dataUnits['Speed Band 6 Limit'] = 'MPH' 
       
        #byte 1068 in XTR file
        dataBytes['Speed Band 7 Limit'] = assembledBytes[105]
        dataValue['Speed Band 7 Limit'] = '%d' %(dataBytes['Speed Band 7 Limit'] )
        dataUnits['Speed Band 7 Limit'] = 'MPH' 
        
        #byte 1069 in XTR file
        dataBytes['Speed Band A Limit'] = assembledBytes[106]
        dataValue['Speed Band A Limit'] = '%d' %(dataBytes['Speed Band A Limit'] )
        dataUnits['Speed Band A Limit'] = 'MPH' 
        
        #byte 1070 in XTR file
        dataBytes['Speed Band B Limit'] = assembledBytes[107]
        dataValue['Speed Band B Limit'] = '%d' %(dataBytes['Speed Band B Limit'] )
        dataUnits['Speed Band B Limit'] = 'MPH' 
       
        #byte 1071 in XTR file
        dataBytes['RPM Band 1 Limit'] = assembledBytes[108]
        dataValue['RPM Band 1 Limit'] = '%d' %(dataBytes['RPM Band 1 Limit'] * 100)
        dataUnits['RPM Band 1 Limit'] = 'RPM' 

        #byte 1072 in XTR file
        dataBytes['RPM Band 2 Limit'] = assembledBytes[109]
        dataValue['RPM Band 2 Limit'] = '%d' %(dataBytes['RPM Band 2 Limit'] * 100)
        dataUnits['RPM Band 2 Limit'] = 'RPM' 
       
        #byte 1073 in XTR file
        dataBytes['RPM Band 3 Limit'] = assembledBytes[110]
        dataValue['RPM Band 3 Limit'] = '%d' %(dataBytes['RPM Band 3 Limit'] * 100)
        dataUnits['RPM Band 3 Limit'] = 'RPM' 
        
        #byte 1074 in XTR file
        dataBytes['RPM Band 4 Limit'] = assembledBytes[111]
        dataValue['RPM Band 4 Limit'] = '%d' %(dataBytes['RPM Band 4 Limit'] * 100)
        dataUnits['RPM Band 4 Limit'] = 'RPM' 
        
        #byte 1075 in XTR file
        dataBytes['RPM Band 5 Limit'] = assembledBytes[112]
        dataValue['RPM Band 5 Limit'] = '%d' %(dataBytes['RPM Band 5 Limit'] * 100)
        dataUnits['RPM Band 5 Limit'] = 'RPM' 
        
        #byte 1076 in XTR file
        dataBytes['RPM Band 6 Limit'] = assembledBytes[113]
        dataValue['RPM Band 6 Limit'] = '%d' %(dataBytes['RPM Band 6 Limit'] * 100)
        dataUnits['RPM Band 6 Limit'] = 'RPM' 
        
        #byte 1077 in XTR file
        dataBytes['RPM Band 7 Limit'] = assembledBytes[114]
        dataValue['RPM Band 7 Limit'] = '%d' %(dataBytes['RPM Band 7 Limit'] * 100)
        dataUnits['RPM Band 7 Limit'] = 'RPM' 
       
        #byte 1078 in XTR file
        dataBytes['RPM Band 8 Limit'] = assembledBytes[115]
        dataValue['RPM Band 8 Limit'] = '%d' %(dataBytes['RPM Band 8 Limit'] * 100)
        dataUnits['RPM Band 8 Limit'] = 'RPM' 
        
        #byte 1079 in XTR file
        dataBytes['Over Rev Limit'] = assembledBytes[116]
        dataValue['Over Rev Limit'] = '%d' %(dataBytes['Over Rev Limit'] * 100)
        dataUnits['Over Rev Limit'] = 'RPM' 
        
        #byte 1080 in XTR file
        dataBytes['Load Band 1 Limit'] = assembledBytes[117]
        dataValue['Load Band 1 Limit'] = '%0.1f' %(dataBytes['Load Band 1 Limit'] * 0.5)
        dataUnits['Load Band 1 Limit'] = '% load' 
        
        #byte 1081 in XTR file
        dataBytes['Load Band 2 Limit'] = assembledBytes[118]
        dataValue['Load Band 2 Limit'] = '%0.1f' %(dataBytes['Load Band 2 Limit'] * 0.5)
        dataUnits['Load Band 2 Limit'] = '% load' 
        
        #byte 1082 in XTR file
        dataBytes['Load Band 3 Limit'] = assembledBytes[119]
        dataValue['Load Band 3 Limit'] = '%0.1f' %(dataBytes['Load Band 3 Limit'] * 0.5)
        dataUnits['Load Band 3 Limit'] = '% load' 
        
        #byte 1083 in XTR file
        dataBytes['Load Band 4 Limit'] = assembledBytes[120]
        dataValue['Load Band 4 Limit'] = '%0.1f' %(dataBytes['Load Band 4 Limit'] * 0.5)
        dataUnits['Load Band 4 Limit'] = '% load' 
        
         
        #byte 1084 in XTR file
        dataBytes['Load Band 5 Limit'] = assembledBytes[121]
        dataValue['Load Band 5 Limit'] = '%0.1f' %(dataBytes['Load Band 5 Limit'] * 0.5)
        dataUnits['Load Band 5 Limit'] = '% load' 
        
        #byte 1085 in XTR file
        dataBytes['Load Band 6 Limit'] = assembledBytes[122]
        dataValue['Load Band 6 Limit'] = '%0.1f' %(dataBytes['Load Band 6 Limit'] * 0.5)
        dataUnits['Load Band 6 Limit'] = '% load' 
        
        #byte 1086 in XTR file
        dataBytes['Load Band 7 Limit'] = assembledBytes[123]
        dataValue['Load Band 7 Limit'] = '%0.1f' %(dataBytes['Load Band 7 Limit'] * 0.5)
        dataUnits['Load Band 7 Limit'] = '% load' 
        
        #byte 1087 in XTR file
        dataBytes['Load Band 8 Limit'] = assembledBytes[124]
        dataValue['Load Band 8 Limit'] = '%0.1f' %(dataBytes['Load Band 8 Limit'] * 0.5)
        dataUnits['Load Band 8 Limit'] = '% load' 
         
        #byte 1088 in XTR file
        dataBytes['Load Band 9 Limit'] = assembledBytes[125]
        dataValue['Load Band 9 Limit'] = '%0.1f' %(dataBytes['Load Band 9 Limit'] * 0.5)
        dataUnits['Load Band 9 Limit'] = '% load' 
        
        #byte 1089 - 1091 in XTR file don't change csv
        
        #byte 1092        
        dataBytes['Service Due Flag'] = assembledBytes[129]
        if dataBytes['Service Due Flag'] == 0:
            dataValue['Service Due Flag'] = 'Off'
        elif dataBytes['Service Due Flag'] == 1:
            dataValue['Service Due Flag'] = 'On'
        else:
            dataValue['Service Due Flag'] = 'Error'
        dataUnits['Service Due Flag'] = 'On/Off/Error'
        
        
        #Bytes 1093-1096 in DDEC4 XTR file  
        dataBytes['Configuration Page Change Time Stamp'] = assembledBytes[130:134]
        dataValue['Configuration Page Change Time Stamp'] = processSecondsForTime(dataBytes['Configuration Page Change Time Stamp'])
        dataUnits['Configuration Page Change Time Stamp'] = 'Time Stamp'
      
        #byte 1097        
        dataBytes['Idle Algorithm'] = assembledBytes[134]
        if dataBytes['Idle Algorithm'] == 0:
            dataValue['Idle Algorithm'] = 'Veh. Speed Sensor'
        elif dataBytes['Idle Algorithm'] == 1:
            dataValue['Idle Algorithm'] = 'Governor'
        elif dataBytes['Idle Algorithm'] == 2:
            dataValue['Idle Algorithm'] = 'RPm and Load'
        else:
            dataValue['Idle Algorithm'] = 'Unknown'
        dataUnits['Idle Algorithm'] = 'Text'
        
        #byte 1098
        dataBytes['Time Zone'] = assembledBytes[135]
        dataValue['Time Zone'] = '%d' %(struct.unpack('b',struct.pack('B',dataBytes['Time Zone']))[0] / 4) #Reference DDEC Reports calculated parameters
        dataUnits['Time Zone'] = 'Hours'       
        
        #byte 1099        
        dataBytes['Trip Reset Lock Out'] = assembledBytes[136]
        if dataBytes['Trip Reset Lock Out'] == 0:
            dataValue['Trip Reset Lock Out'] = 'Off'
        elif dataBytes['Trip Reset Lock Out'] == 1:
            dataValue['Trip Reset Lock Out'] = 'On'
        else:
            dataValue['Trip Reset Lock Out'] = 'Error'
        dataUnits['Trip Reset Lock Out'] = 'On/Off/Error'
        
    elif i == 4: #Diagnosic Records
      diagnosticRecords = []
      recLen=281
      for j in range(3):              
        diagnosticBytes={}
        diagnosticValue={}
        diagnosticUnits={}
        #XTR byte 1105 -> Assembled Byte 55
        
        #byte 1107 in XTR file        
        diagnosticBytes['Diagnostic Code']= assembledBytes[57 + j*recLen]
        diagnosticValue['Diagnostic Code']= '%d' %assembledBytes[57 + j*recLen]
        
        #byte 1108-1111
        diagnosticBytes['Diagnostic Time']= assembledBytes[58 + j*recLen:62 + j*recLen]
        diagnosticValue['Diagnostic Time']= processSecondsForTime(diagnosticBytes['Diagnostic Time'])
        diagnosticUnits['Diagnostic Time']= 'Time Stamp'
        
        diagnosticBytes['VehicleSpeed']=[]
        diagnosticBytes['EngineSpeed'] =[]
        diagnosticBytes['BoostPress']  =[]
        diagnosticBytes['OilPress']    =[]
        diagnosticBytes['FuelPress']   =[]
        diagnosticBytes['CoolantTemp'] =[]
        diagnosticBytes['OilTemp']     =[]
        diagnosticBytes['FuelTemp']     =[]
        diagnosticBytes['EngineLoad']  =[]
        diagnosticBytes['Throttle']    =[]
        diagnosticBytes['EngineBrake'] =[]
        diagnosticBytes['Cruise']      =[]
        diagnosticBytes['AccelSwitch'] =[]
        diagnosticBytes['BrakeSwitch'] =[]
        diagnosticBytes['ClutchSwitch']=[]
        
        diagnosticValue['VehicleSpeed']=[]
        diagnosticValue['EngineSpeed'] =[]
        diagnosticValue['BoostPress']  =[]
        diagnosticValue['OilPress']    =[]
        diagnosticValue['FuelPress']   =[]
        diagnosticValue['CoolantTemp'] =[]
        diagnosticValue['OilTemp']     =[]
        diagnosticValue['FuelTemp']     =[]
        diagnosticValue['EngineLoad']  =[]
        diagnosticValue['Throttle']    =[]
        diagnosticValue['EngineBrake'] =[]
        diagnosticValue['Cruise']      =[]
        diagnosticValue['AccelSwitch'] =[]
        diagnosticValue['BrakeSwitch'] =[]
        diagnosticValue['ClutchSwitch']=[]
        
        diagnosticUnits['VehicleSpeed']='MPH'
        diagnosticUnits['EngineSpeed'] ='RPM'
        diagnosticUnits['BoostPress']  ='PSI'
        diagnosticUnits['OilPress']    ='psi'
        diagnosticUnits['FuelPress']   ='psi'
        diagnosticUnits['CoolantTemp'] ='deg F'
        diagnosticUnits['OilTemp']     ='deg F'
        diagnosticUnits['FuelTemp']     ='deg F'
        diagnosticUnits['EngineLoad']  ='%'
        diagnosticUnits['Throttle']    ='% throttle'
        diagnosticUnits['EngineBrake'] ='cylinders'
        diagnosticUnits['Cruise']      ='on/off'
        diagnosticUnits['AccelSwitch'] ='on/off'
        diagnosticUnits['BrakeSwitch'] ='on/off'
        diagnosticUnits['ClutchSwitch']='on/off'
        
        for k in range(62 + j*recLen,320 + j*recLen,23):
                        
            diagnosticBytes['VehicleSpeed'].append(assembledBytes[k])
            diagnosticValue['VehicleSpeed'].append('%0.1f' %(assembledBytes[k] * 0.5))
            
            diagnosticBytes['EngineSpeed'].append(assembledBytes[k+1:k+3])
            diagnosticValue['EngineSpeed'].append('%0.2f' %(struct.unpack('<H',assembledBytes[k+1:k+3])[0] * 0.25))
           
            diagnosticBytes['BoostPress'].append(assembledBytes[k+3:k+5])
            diagnosticValue['BoostPress'].append('%0.3f' %(struct.unpack('<H',assembledBytes[k+3:k+5])[0] * 0.125))
            
            diagnosticBytes['OilPress'].append(assembledBytes[k+5:k+7])
            diagnosticValue['OilPress'].append('%0.3f' %(struct.unpack('<H',assembledBytes[k+5:k+7])[0] * 0.125))
           
            diagnosticBytes['FuelPress'].append(assembledBytes[k+7:k+9])
            diagnosticValue['FuelPress'].append('%0.3f' %(struct.unpack('<H',assembledBytes[k+7:k+9])[0] * 0.125))
           
            #Add 2 for no change in file
            #bytes 1130 and 1131
           
            
            diagnosticBytes['CoolantTemp'].append(assembledBytes[k+11:k+13])
            diagnosticValue['CoolantTemp'].append('%0.2f' %(struct.unpack('<H',assembledBytes[k+11:k+13])[0] * 0.25 - 40))
            
            diagnosticBytes['OilTemp'].append(assembledBytes[k+13:k+15])
            diagnosticValue['OilTemp'].append('%0.2f' %(struct.unpack('<H',assembledBytes[k+13:k+15])[0] * 0.25 - 40))
            
            diagnosticBytes['FuelTemp'].append(assembledBytes[k+15:k+17])
            diagnosticValue['FuelTemp'].append('%0.2f' %(struct.unpack('<H',assembledBytes[k+15:k+17])[0] * 0.25 - 40))
            
            diagnosticBytes['Throttle'].append(assembledBytes[k+17])
            diagnosticValue['Throttle'].append('%0.2f' %(assembledBytes[k+17] * 0.4 ))
            
            diagnosticBytes['EngineLoad'].append(assembledBytes[k+21])
            diagnosticValue['EngineLoad'].append('%0.2f' %(assembledBytes[k+21] * 0.5 ))
            
        
            bitField = assembledBytes[k+22]
           
            if bitField & 128 == 128: 
               diagnosticValue['Cruise'].append('Yes')
            else:
               diagnosticValue['Cruise'].append('No')
           
            if bitField & 16 == 16:
               diagnosticValue['AccelSwitch'].append('Yes')
            else:
               diagnosticValue['AccelSwitch'].append('No')
            
            if bitField & 32 == 32:
               diagnosticValue['BrakeSwitch'].append('Yes')
            else:
               diagnosticValue['BrakeSwitch'].append('No')
                  
            if bitField & 64 == 64:
              diagnosticValue['ClutchSwitch'].append('Yes')
            else:
              diagnosticValue['ClutchSwitch'].append('No')
           
            
        diagnosticRecords.append(diagnosticValue)  
        print(diagnosticValue)
    
    elif i == 5:    
        #Daily Engine Usage
        #XTR byte 1950 = session 5 byte 51
        
        dailyUseBytes={}
        dailyUseValue={}
        dailyUseUnits={}
        
        dailyUseBytes['Distance']   =[]
        dailyUseBytes['Fuel']       =[]
        dailyUseBytes['Start Time']  =[]
        dailyUseBytes['Odometer']   =[]
        dailyUseBytes['Idle Time 00:00-02:00'] = []
        dailyUseBytes['Idle Time 02:00-04:00'] = []
        dailyUseBytes['Idle Time 04:00-06:00'] = []
        dailyUseBytes['Idle Time 06:00-08:00'] = []
        dailyUseBytes['Idle Time 08:00-10:00'] = []
        dailyUseBytes['Idle Time 10:00-12:00'] = []
        dailyUseBytes['Idle Time 12:00-14:00'] = []
        dailyUseBytes['Idle Time 14:00-16:00'] = []
        dailyUseBytes['Idle Time 16:00-18:00'] = []
        dailyUseBytes['Idle Time 18:00-20:00'] = []
        dailyUseBytes['Idle Time 20:00-22:00'] = []
        dailyUseBytes['Idle Time 22:00-24:00'] = []
        dailyUseBytes['Drive Time 00:00-02:00'] = []
        dailyUseBytes['Drive Time 02:00-04:00'] = []
        dailyUseBytes['Drive Time 04:00-06:00'] = []
        dailyUseBytes['Drive Time 06:00-08:00'] = []
        dailyUseBytes['Drive Time 08:00-10:00'] = []
        dailyUseBytes['Drive Time 10:00-12:00'] = []
        dailyUseBytes['Drive Time 12:00-14:00'] = []
        dailyUseBytes['Drive Time 14:00-16:00'] = []
        dailyUseBytes['Drive Time 16:00-18:00'] = []
        dailyUseBytes['Drive Time 18:00-20:00'] = []
        dailyUseBytes['Drive Time 20:00-22:00'] = []
        dailyUseBytes['Drive Time 22:00-24:00'] = []
        
        dailyUseValue['Distance']   =[]
        dailyUseValue['Fuel']       =[]
        dailyUseValue['Start Time']  =[]
        dailyUseValue['Odometer']   =[]
        dailyUseValue['Idle Time 00:00-02:00'] = []
        dailyUseValue['Idle Time 02:00-04:00'] = []
        dailyUseValue['Idle Time 04:00-06:00'] = []
        dailyUseValue['Idle Time 06:00-08:00'] = []
        dailyUseValue['Idle Time 08:00-10:00'] = []
        dailyUseValue['Idle Time 10:00-12:00'] = []
        dailyUseValue['Idle Time 12:00-14:00'] = []
        dailyUseValue['Idle Time 14:00-16:00'] = []
        dailyUseValue['Idle Time 16:00-18:00'] = []
        dailyUseValue['Idle Time 18:00-20:00'] = []
        dailyUseValue['Idle Time 20:00-22:00'] = []
        dailyUseValue['Idle Time 22:00-24:00'] = []
        dailyUseValue['Drive Time 00:00-02:00'] = []
        dailyUseValue['Drive Time 02:00-04:00'] = []
        dailyUseValue['Drive Time 04:00-06:00'] = []
        dailyUseValue['Drive Time 06:00-08:00'] = []
        dailyUseValue['Drive Time 08:00-10:00'] = []
        dailyUseValue['Drive Time 10:00-12:00'] = []
        dailyUseValue['Drive Time 12:00-14:00'] = []
        dailyUseValue['Drive Time 14:00-16:00'] = []
        dailyUseValue['Drive Time 16:00-18:00'] = []
        dailyUseValue['Drive Time 18:00-20:00'] = []
        dailyUseValue['Drive Time 20:00-22:00'] = []
        dailyUseValue['Drive Time 22:00-24:00'] = []
        
        dailyUseUnits['Distance']   ='Miles'
        dailyUseUnits['Fuel']       ='Gallons'
        dailyUseUnits['Start Time']  ='Time Stamp'
        dailyUseUnits['Odometer']   ='Miles'
        dailyUseUnits['Idle Time 00:00-02:00'] = 'Minutes'
        dailyUseUnits['Idle Time 02:00-04:00'] = 'Minutes'
        dailyUseUnits['Idle Time 04:00-06:00'] = 'Minutes'
        dailyUseUnits['Idle Time 06:00-08:00'] = 'Minutes'
        dailyUseUnits['Idle Time 08:00-10:00'] = 'Minutes'
        dailyUseUnits['Idle Time 10:00-12:00'] = 'Minutes'
        dailyUseUnits['Idle Time 12:00-14:00'] = 'Minutes'
        dailyUseUnits['Idle Time 14:00-16:00'] = 'Minutes'
        dailyUseUnits['Idle Time 16:00-18:00'] = 'Minutes'
        dailyUseUnits['Idle Time 18:00-20:00'] = 'Minutes'
        dailyUseUnits['Idle Time 20:00-22:00'] = 'Minutes'
        dailyUseUnits['Idle Time 22:00-24:00'] = 'Minutes'
        dailyUseUnits['Drive Time 00:00-02:00'] = 'Minutes'
        dailyUseUnits['Drive Time 02:00-04:00'] = 'Minutes'
        dailyUseUnits['Drive Time 04:00-06:00'] = 'Minutes'
        dailyUseUnits['Drive Time 06:00-08:00'] = 'Minutes'
        dailyUseUnits['Drive Time 08:00-10:00'] = 'Minutes'
        dailyUseUnits['Drive Time 10:00-12:00'] = 'Minutes'
        dailyUseUnits['Drive Time 12:00-14:00'] = 'Minutes'
        dailyUseUnits['Drive Time 14:00-16:00'] = 'Minutes'
        dailyUseUnits['Drive Time 16:00-18:00'] = 'Minutes'
        dailyUseUnits['Drive Time 18:00-20:00'] = 'Minutes'
        dailyUseUnits['Drive Time 20:00-22:00'] = 'Minutes'
        dailyUseUnits['Drive Time 22:00-24:00'] = 'Minutes'
       
        for j in range(57,(58+30*36)-1,36):
            dailyUseBytes['Distance'].append(assembledBytes[j:j+2])
            dailyUseValue['Distance'].append('%0.1f' %(struct.unpack('<H', dailyUseBytes['Distance'][-1])[0] * 0.1 ))
            
            dailyUseBytes['Fuel'].append(assembledBytes[j+2:j+4])
            dailyUseValue['Fuel'].append('%0.3f' %(struct.unpack('<H', dailyUseBytes['Fuel'][-1])[0] * 0.125))
           
            dailyUseBytes['Start Time'].append(assembledBytes[j+4:j+8])
            dailyUseValue['Start Time'].append(processSecondsForTime(dailyUseBytes['Start Time'][-1]))
            
            dailyUseBytes['Odometer'].append(assembledBytes[j+8:j+12])
            dailyUseValue['Odometer'].append('%0.1f' %(struct.unpack('<L', dailyUseBytes['Odometer'][-1])[0] * 0.1))
        
            dailyUseBytes['Idle Time 00:00-02:00'].append(assembledBytes[j+12])
            dailyUseBytes['Idle Time 02:00-04:00'].append(assembledBytes[j+13])
            dailyUseBytes['Idle Time 04:00-06:00'].append(assembledBytes[j+14])
            dailyUseBytes['Idle Time 06:00-08:00'].append(assembledBytes[j+15])
            dailyUseBytes['Idle Time 08:00-10:00'].append(assembledBytes[j+16])
            dailyUseBytes['Idle Time 10:00-12:00'].append(assembledBytes[j+17])
            dailyUseBytes['Idle Time 12:00-14:00'].append(assembledBytes[j+18])
            dailyUseBytes['Idle Time 14:00-16:00'].append(assembledBytes[j+19])
            dailyUseBytes['Idle Time 16:00-18:00'].append(assembledBytes[j+20])
            dailyUseBytes['Idle Time 18:00-20:00'].append(assembledBytes[j+21])
            dailyUseBytes['Idle Time 20:00-22:00'].append(assembledBytes[j+22])
            dailyUseBytes['Idle Time 22:00-24:00'].append(assembledBytes[j+23])
                
            dailyUseValue['Idle Time 00:00-02:00'].append('%d' %assembledBytes[j+12])
            dailyUseValue['Idle Time 02:00-04:00'].append('%d' %assembledBytes[j+13])
            dailyUseValue['Idle Time 04:00-06:00'].append('%d' %assembledBytes[j+14])
            dailyUseValue['Idle Time 06:00-08:00'].append('%d' %assembledBytes[j+15])
            dailyUseValue['Idle Time 08:00-10:00'].append('%d' %assembledBytes[j+16])
            dailyUseValue['Idle Time 10:00-12:00'].append('%d' %assembledBytes[j+17])
            dailyUseValue['Idle Time 12:00-14:00'].append('%d' %assembledBytes[j+18])
            dailyUseValue['Idle Time 14:00-16:00'].append('%d' %assembledBytes[j+19])
            dailyUseValue['Idle Time 16:00-18:00'].append('%d' %assembledBytes[j+20])
            dailyUseValue['Idle Time 18:00-20:00'].append('%d' %assembledBytes[j+21])
            dailyUseValue['Idle Time 20:00-22:00'].append('%d' %assembledBytes[j+22])
            dailyUseValue['Idle Time 22:00-24:00'].append('%d' %assembledBytes[j+23])
        
            dailyUseBytes['Drive Time 00:00-02:00'].append(assembledBytes[j+24])
            dailyUseBytes['Drive Time 02:00-04:00'].append(assembledBytes[j+25])
            dailyUseBytes['Drive Time 04:00-06:00'].append(assembledBytes[j+26])
            dailyUseBytes['Drive Time 06:00-08:00'].append(assembledBytes[j+27])
            dailyUseBytes['Drive Time 08:00-10:00'].append(assembledBytes[j+28])
            dailyUseBytes['Drive Time 10:00-12:00'].append(assembledBytes[j+29])
            dailyUseBytes['Drive Time 12:00-14:00'].append(assembledBytes[j+30])
            dailyUseBytes['Drive Time 14:00-16:00'].append(assembledBytes[j+31])
            dailyUseBytes['Drive Time 16:00-18:00'].append(assembledBytes[j+32])
            dailyUseBytes['Drive Time 18:00-20:00'].append(assembledBytes[j+33])
            dailyUseBytes['Drive Time 20:00-22:00'].append(assembledBytes[j+34])
            dailyUseBytes['Drive Time 22:00-24:00'].append(assembledBytes[j+35])

            dailyUseValue['Drive Time 00:00-02:00'].append('%d' %assembledBytes[j+24])
            dailyUseValue['Drive Time 02:00-04:00'].append('%d' %assembledBytes[j+25])
            dailyUseValue['Drive Time 04:00-06:00'].append('%d' %assembledBytes[j+26])
            dailyUseValue['Drive Time 06:00-08:00'].append('%d' %assembledBytes[j+27])
            dailyUseValue['Drive Time 08:00-10:00'].append('%d' %assembledBytes[j+28])
            dailyUseValue['Drive Time 10:00-12:00'].append('%d' %assembledBytes[j+29])
            dailyUseValue['Drive Time 12:00-14:00'].append('%d' %assembledBytes[j+30])
            dailyUseValue['Drive Time 14:00-16:00'].append('%d' %assembledBytes[j+31])
            dailyUseValue['Drive Time 16:00-18:00'].append('%d' %assembledBytes[j+32])
            dailyUseValue['Drive Time 18:00-20:00'].append('%d' %assembledBytes[j+33])
            dailyUseValue['Drive Time 20:00-22:00'].append('%d' %assembledBytes[j+34])
            dailyUseValue['Drive Time 22:00-24:00'].append('%d' %assembledBytes[j+35])
            
    elif i == 6:
        
        percentTripTimeDataBytes={}
        percentTripTimeDataValue={}
       
        bands = 10
        percentTripTimeDataBytes['Brakes']=[]
        percentTripTimeDataValue['Brakes']=[]
        
        for j in range(57,57+bands*4-1,4):
            percentTripTimeDataBytes['Brakes'].append(assembledBytes[j:j+4])
            percentTripTimeDataValue['Brakes'].append('%d' %struct.unpack('<L', percentTripTimeDataBytes['Brakes'][-1])[0])
            
        percentTripTimeDataBytes['Hard Brakes']=[]
        percentTripTimeDataValue['Hard Brakes']=[]
        for j in range(97,97+bands*2-1,2):
            percentTripTimeDataBytes['Hard Brakes'].append(assembledBytes[j:j+2])
            percentTripTimeDataValue['Hard Brakes'].append('%d' %struct.unpack('<H', percentTripTimeDataBytes['Hard Brakes'][-1])[0])
            
        percentTripTimeDataBytes['Speed and RPM Times']=[]
        percentTripTimeDataValue['Speed and RPM Times']=[]
        total=0
        for j in range(0,bands):
            percentTripTimeDataBytes['Speed and RPM Times'].append([])
            percentTripTimeDataValue['Speed and RPM Times'].append([])
            
            for k in range(0,bands):
                percentTripTimeDataBytes['Speed and RPM Times'][j].append(assembledBytes[117 + j*bands*4 + k*4 : 117 + j*bands*4 + k*4 + 4])
                seconds= struct.unpack('<L',  percentTripTimeDataBytes['Speed and RPM Times'][j][k])[0]
                total+=seconds
                percentTripTimeDataValue['Speed and RPM Times'][j].append(seconds)
        
        percentTripTimeDataValue['Speed and RPM Table']=[]
        for j in range(0,bands):
            percentTripTimeDataValue['Speed and RPM Table'].append([])
            for k in range(0,bands):
                percentTripTimeDataValue['Speed and RPM Table'][j].append('%0.2f' %(100 * percentTripTimeDataValue['Speed and RPM Times'][j][k]/float(total)))
         
        percentTripTimeDataValue['SpeedTimeTotal']=total 
         
        
        percentTripTimeDataBytes['Load and RPM Times']=[]
        percentTripTimeDataValue['Load and RPM Times']=[]
        total=0
        for j in range(0,bands):
            percentTripTimeDataBytes['Load and RPM Times'].append([])
            percentTripTimeDataValue['Load and RPM Times'].append([])
            
            for k in range(0,bands):
                percentTripTimeDataBytes['Load and RPM Times'][j].append(assembledBytes[517 + j*bands*4 + k*4 : 517 + j*bands*4 + k*4 + 4])
                seconds= struct.unpack('<L',  percentTripTimeDataBytes['Load and RPM Times'][j][k])[0]
                total+=seconds
                percentTripTimeDataValue['Load and RPM Times'][j].append(seconds)
        
        percentTripTimeDataValue['Load and RPM Table']=[]
        for j in range(0,bands):
            percentTripTimeDataValue['Load and RPM Table'].append([])
            for k in range(0,bands):
                percentTripTimeDataValue['Load and RPM Table'][j].append('%0.2f' %(100 * percentTripTimeDataValue['Load and RPM Times'][j][k]/float(total)))
        
        percentTripTimeDataValue['LoadTimeTotal']=total 
        


        #This section needs testing or further analysis. The DDEC reports over Rev bands to not match the pattern here.
        #The first entry in the table drops to zero as larger numbers are added.
      
        percentTripTimeDataBytes['Over Speed Times']=[]
        percentTripTimeDataValue['Over Speed Times']=[]
        for k in range(0,bands):
                percentTripTimeDataBytes['Over Speed Times'].append(assembledBytes[917 + k*4 : 917 + k*4 + 4])
                seconds= struct.unpack('<L',  percentTripTimeDataBytes['Over Speed Times'][k])[0]
                percentTripTimeDataValue['Over Speed Times'].append(seconds)
        
        percentTripTimeDataValue['Over Speed Table']=[]
        for k in range(0,bands):
                percentTripTimeDataValue['Over Speed Table'].append('%0.3f' %(100 * percentTripTimeDataValue['Over Speed Times'][k]/float(total)))
        
        
        
        percentTripTimeDataBytes['Over Rev Times']=[]
        percentTripTimeDataValue['Over Rev Times']=[]
        for k in range(0,bands):
                percentTripTimeDataBytes['Over Rev Times'].append(assembledBytes[957 + k*4 : 957 + k*4 + 4])
                seconds= struct.unpack('<L',  percentTripTimeDataBytes['Over Rev Times'][k])[0]
                percentTripTimeDataValue['Over Rev Times'].append(seconds)
                
        percentTripTimeDataValue['Over Rev Table']=[]
        percentTripTimeDataValue['Over Rev Table'].append('%0.3f' %(100 * percentTripTimeDataValue['Over Rev Times'][k]/float(total)))
        for k in range(0,bands):
            percentTripTimeDataValue['Over Rev Table'].append('%0.3f' %(100 * percentTripTimeDataValue['Over Rev Times'][k]/float(total)))
        
        
        #print(percentTripTimeDataValue)
        
        
    elif i == 7:
        #Life to date
        #Bytes 3989-3992 in XTR        
        dataBytes['Total Distance'] = assembledBytes[58:62] 
        dataValue['Total Distance'] = '%0.1f' %(struct.unpack('<L', dataBytes['Total Distance'])[0] * 0.1)
        dataUnits['Total Distance'] = 'Miles'
               
        #Bytes 3993-3996 in XTR
        dataBytes['Total Fuel Used'] = assembledBytes[62:66] 
        dataValue['Total Fuel Used'] = '%0.3f' %(struct.unpack('<L', dataBytes['Total Fuel Used'])[0] * 0.125)
        dataUnits['Total Fuel Used'] = 'Gallons'
        
        #Bytes 3997-4000 in XTR file
        #Trip Activity of DDEC Reportd
        dataBytes['Total Time'] = assembledBytes[66:70] 
        secs = struct.unpack('<L', dataBytes['Total Time'])[0]
        dataValue['Total Time'] = '%02d:%02d:%02d' %(secs/3600,secs%3600/60,secs%3600%60)
        dataUnits['Total Time'] = 'HH:MM:SS'
        
        #Bytes 4001-4004 in XTR
        dataBytes['Total Idle Fuel Used'] = assembledBytes[70:74] 
        dataValue['Total Idle Fuel Used'] = '%0.3f' %(struct.unpack('<L', dataBytes['Total Idle Fuel Used'])[0] * 0.125)
        dataUnits['Total Idle Fuel Used'] = 'Gallons'
        
        #Bytes 4005-4008 in XTR file
        dataBytes['Total Idle Time'] = assembledBytes[74:78] 
        secs = struct.unpack('<L', dataBytes['Total Idle Time'])[0]
        dataValue['Total Idle Time'] = '%02d:%02d:%02d' %(secs/3600,secs%3600/60,secs%3600%60)
        dataUnits['Total Idle Time'] = 'HH:MM:SS'
        
        #Bytes 4009-4012 in XTR
        dataBytes['Total PTO Fuel Used'] = assembledBytes[78:82] 
        dataValue['Total PTO Fuel Used'] = '%0.3f' %(struct.unpack('<L', dataBytes['Total PTO Fuel Used'])[0] * 0.125)
        dataUnits['Total PTO Fuel Used'] = 'Gallons'
        
        #Bytes 4013-4016 in XTR file
        dataBytes['Total PTO Time'] = assembledBytes[82:86] 
        secs = struct.unpack('<L', dataBytes['Total PTO Time'])[0]
        dataValue['Total PTO Time'] = '%02d:%02d:%02d' %(secs/3600,secs%3600/60,secs%3600%60)
        dataUnits['Total PTO Time'] = 'HH:MM:SS'
        
        #Bytes 4017-4020 in XTR file
        dataBytes['Total Cruise Time'] = assembledBytes[86:90] 
        secs = struct.unpack('<L', dataBytes['Total Cruise Time'])[0]
        dataValue['Total Cruise Time'] = '%02d:%02d:%02d' %(secs/3600,secs%3600/60,secs%3600%60)
        dataUnits['Total Cruise Time'] = 'HH:MM:SS'
        
        #Bytes 4021-4024 in XTR file
        dataBytes['Total Optimized Idle Active Time'] = assembledBytes[90:94] 
        secs = struct.unpack('<L', dataBytes['Total Optimized Idle Active Time'])[0]
        dataValue['Total Optimized Idle Active Time'] = '%02d:%02d:%02d' %(secs/3600,secs%3600/60,secs%3600%60)
        dataUnits['Total Optimized Idle Active Time'] = 'HH:MM:SS'
        
        #Bytes 4025-4028 in XTR file
        dataBytes['Total Optimized Idle Run Time'] = assembledBytes[94:98] 
        secs = struct.unpack('<L', dataBytes['Total Optimized Idle Run Time'])[0]
        dataValue['Total Optimized Idle Run Time'] = '%02d:%02d:%02d' %(secs/3600,secs%3600/60,secs%3600%60)
        dataUnits['Total Optimized Idle Run Time'] = 'HH:MM:SS'
        
        #Bytes 4029-4032 in XTR file
        dataBytes['Total Engine Brake Time'] = assembledBytes[98:102] 
        secs = struct.unpack('<L', dataBytes['Total Engine Brake Time'])[0]
        dataValue['Total Engine Brake Time'] = '%02d:%02d:%02d' %(secs/3600,secs%3600/60,secs%3600%60)
        dataUnits['Total Engine Brake Time'] = 'HH:MM:SS'
        
        #Byte 4033 in XTR file
        dataBytes['Life Average Drive Load'] = assembledBytes[102] 
        dataValue['Life Average Drive Load'] = dataBytes['Life Average Drive Load']
        dataUnits['Life Average Drive Load'] = '% max load'
        
        #Bytes 4034-4037 in XTR file
        dataBytes['Life Engine Revolutions'] = assembledBytes[103:107] 
        dataValue['Life Engine Revolutions'] = struct.unpack('<L', dataBytes['Life Engine Revolutions'])[0] 
        dataUnits['Life Engine Revolutions'] = 'Count (max 2^32)'
    
        #Bytes 4029-4032 in XTR file
        dataBytes['Total Engine Fan On Time'] = assembledBytes[107:111] 
        secs = struct.unpack('<L', dataBytes['Total Engine Fan On Time'])[0]
        dataValue['Total Engine Fan On Time'] = '%02d:%02d:%02d' %(secs/3600,secs%3600/60,secs%3600%60)
        dataUnits['Total Engine Fan On Time'] = 'HH:MM:SS'
               
        #Bytes 4029-4032 in XTR file
        dataBytes['Total Manual Fan On Time'] = assembledBytes[111:115] 
        secs = struct.unpack('<L', dataBytes['Total Manual Fan On Time'])[0]
        dataValue['Total Manual Fan On Time'] = '%02d:%02d:%02d' %(secs/3600,secs%3600/60,secs%3600%60)
        dataUnits['Total Manual Fan On Time'] = 'HH:MM:SS'
       
        #Bytes 4029-4032 in XTR file
        dataBytes['Total A/C Fan On Time'] = assembledBytes[115:119] 
        secs = struct.unpack('<L', dataBytes['Total A/C Fan On Time'])[0]
        dataValue['Total A/C Fan On Time'] = '%02d:%02d:%02d' %(secs/3600,secs%3600/60,secs%3600%60)
        dataUnits['Total A/C Fan On Time'] = 'HH:MM:SS'
         
    elif i == 8:    
        hardBrake1Bytes,hardBrake1Value,hardBrake1Units=getDDEC4HardBrakeData(assembledBytes)
        hardBrake2Bytes,hardBrake2Value,hardBrake2Units=getDDEC4HardBrakeData(assembledBytes[467:])
    
    elif i == 9:    
        lastStopBytes,lastStopValue,lastStopUnits=getDDEC4LastStopData(assembledBytes)
        
    else:
        htmlString+='<p>Something went wrong! i = %d' %i
   
    i+=1

newXTRfile.write(b'\xff\xff')
newXTRfile.close()

htmlString+=prettyPrintDict(dataValue,dataUnits,dataBytes,'ECM Data',dataPID)

htmlString+=prettyPrintEventData(hardBrake1Value,'Hard Brake #1')
htmlString+=prettyPrintEventData(hardBrake2Value,'Hard Brake #2')
htmlString+=prettyPrintEventData(lastStopValue,'Last Stop Record')

htmlString+=prettyPrintDict(tripDataValue,tripDataUnits,tripDataBytes,'Trip Activity')
      
htmlString+=prettyPrintDailyUse(dailyUseBytes,dailyUseValue,dailyUseUnits)


htmlString+=prettyPrintDiagnostics(diagnosticValue,diagnosticUnits,'Diagnostic Data')

htmlString+=prettyPrintBandedTable(percentTripTimeDataValue['Speed and RPM Table'],'Percent of Trip Time in Speed and RPM Table')

htmlString+=prettyPrintBandedTable(percentTripTimeDataValue['Load and RPM Table'],'Percent of Trip Time in Load and RPM Table')
htmlString+=prettyPrintDict(Month1DataValue,Month1DataUnits,Month1DataBytes,'Monthly Activity 1')
htmlString+=prettyPrintDict(Month2DataValue,Month2DataUnits,Month2DataBytes,'Monthly Activity 2')
htmlString+=prettyPrintDict(Month3DataValue,Month3DataUnits,Month3DataBytes,'Monthly Activity 3')
        
    
outputFile=open('extractedData.html','w')
outputFile.write(htmlString)
outputFile.close()

#print(percentTripTimeDataValue)
#print(hardBrake1Value)
#print(hardBrake2Value)
#print(lastStopValue)



nRetVal = RP1210_ClientDisconnect( c_short( nClientID ) )

if nRetVal == 0 :
   print("RP1210_ClientDisconnect - SUCCESS" )
else :
   print("RP1210_ClientDisconnect returns %i" %nRetVal )
#if
