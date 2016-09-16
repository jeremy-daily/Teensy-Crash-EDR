# ----------------------------------------------------------------------------------------------------
#  DG Technologies - RP1210 Sample Source for Python - Copyright (c) 2012-2013 - Dearborn Group, Inc.
# ----------------------------------------------------------------------------------------------------
# 
# Name:            SampleSourceCode.py  Version 1.1
# 
# Date:            December 4, 12
# 
# Co-Written By:   Kenneth L. DeGrant II
#                  Field Applications Engineering Manager and TMC RP1210 Task Force Chairman
#                  DG Technologies
#                  33604 West 8 Mile Road
#                  Farmington Hills, MI  48335
#                  kdegrant@dgtech.com
#
#                  Dr. Jeremy Daily
#                  Associate Professor of Mechanical Engineering
#                  University of Tulsa
#                  800 S. Tucker Dr.
#                  Tulsa, OK 74104
# 
# Description:     This code is provided by DG Technologies to assist application developers in 
#                  developing RP1210 applications for the Dearborn Protocol Adapter ( DPA ) family 
#                  of products using the Python programming language.  It allows connecting to a 
#                  DG DPA and the J1708/J1587, CAN@250k, and J1939 protocols ( the most common 
#                  heavy-duty vehicle protocols ).  It also allows connections to CAN and J1939 
#                  with automatic baud rate detection as specified in J1939 and TMC RP1210.
#
#                  This application demonstrates the four basic features of any communications
#                  device (Open, Read, Write, Close).  It displays all message traffic seen/sent 
#                  and also sends out request messages every 5 seconds.
#
# Code Notes:      All necessary code for this project is in one file ( this file ).  Because this
#                  program runs under the Python interpreter window and outputs text as it would
#                  if were running under a DOS command prompt, it can be readily adapted to do any basic 
#                  functionality that a developer unfamiliar with RP1210 might want to do without
#                  having to look at complex "GUI" code.  
#
# J1939 Notes:     The code sends a J1939 request using PGN 59904 (Request PGN) asking for 
#                  PGN 65259 - Component ID.
#
# J1587 Notes:     The code sends a J1587 request using PID 0 (Request PID) asking for 
#                  PID 237 - VIN.
#
# CAN Notes:       The code sends a 29-bit CANID of CANID 0x18EAFFF9 with three bytes
#                  of data [EC][FE][00].  This correlates to the J1939 PGN of 59904 ( the request PGN ) 
#                  requesting the PGN 0x00FEEC ( 65260 - VIN ) from address F9 ( Offboard PC #1 ).  
#                  The receive/print routine for the CAN protocol handles both standard CAN ( 11-bit ) 
#                  as well as extended ( 29-bit ) CAN traffic.  
#
# DPA Notes:       This program requires that you have downloaded and installed the latest DPA
#                  drivers for either the DPA 4 Plus ( DPA4PSA/DPA4PMA ), DPA 4 Plus and prior adapters
#                  ( found in DG121032 ), or the DPA 5 ( DGDPA5SA/DGDPA5MA ).  These drivers are 
#                  readily available from the DG Technologies website as follows:
#
#                               http://www.dgtech.com/download.php
#
# Python Notes:    This program was developed using the Python Interpreter at version 3.2.3.
#
# No Liability:    This code is example code and is NOT warranted to be fit for any particular use 
#                  or purpose.  DG Technologies will not be held liable for any use or 
#                  misuse of this code "under any circumstances whatsoever".  
# 
# Notes:           Be sure to have your DOS command prompt set to a width of at least 150, as the 
#                  program displays about 140 contiguous characters from a J1939 message.
# 
#                  It is possible to develop a completely RP1210 A/B/C compliant application that
#                  will not connect, send or read messages to or from a particular databus.  
#                  To ensure success, please read the documentation for the protocol you want to use 
#                  thoroughly along with reading the "complete" RP1210 document before trying to 
#                  adapt this code to a particular purpose.
#
# Copyright:       This code is copyrighted by Dearborn Group, Inc., and is intended
#                  solely for the use of our DPA customers or potential DPA customers.  No portion,
#                  including "snippets" of this code are to be used, investigated, or copied in any 
#                  shape, form, or fashion, by anyone who is, or may in the future be, in competition 
#                  with DG Technologies in any way.  The code shall also not be modified in
#                  a way that it is capable of being used with any adapter outside of one from Dearborn 
#                  Group Technology.
#
# ----------------------------------------------------------------------------------------------------
#  Revision  Date       Notes
#     1.0    10-08-12   Original Version.
#     1.1    12-04-12   Changed copyright dates.
# ----------------------------------------------------------------------------------------------------
#

PROGRAM_ID = "DG Technologies - RP1210 Python Sample Souce Code - Version 1.1"

#-----------------------------------------------------------------------------------------------------
# Include Files
#-----------------------------------------------------------------------------------------------------

import struct
import sys
import os
import msvcrt
from   ctypes import *
from   ctypes.wintypes import HWND
from   array import *
from   time import *

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

#
#
#********************************************************************************
# Global Functions
#********************************************************************************
#
#

#-----------------------------------------------------------------------------------------------------
# Print a Received J1708/J1587 message.
#-----------------------------------------------------------------------------------------------------

def PrintRxJ1708Message( nRetVal, ucTxRxBuffer ) :
    '''This function prints a received J1708/J1587 message to the screen.'''
    
    iTS        = c_int (0)
    ucMID      = c_char(0)
    ucPID      = c_char(0)
    nDataBytes = c_short(0)
    
    iTS        = int(struct.unpack('>L',(ucTxRxBuffer[0]+ucTxRxBuffer[1]+ucTxRxBuffer[2]+ucTxRxBuffer[3]))[0])
    ucMID      = struct.unpack( 'B', ucTxRxBuffer[4]   )
    ucPID      = struct.unpack( 'B', ucTxRxBuffer[5]   )
    nDataBytes = nRetVal - 6
    
    print( "Rx J1708 TS=[%d]" % iTS           , end=" " )
    print(         "MID=[%d]" % ucMID         , end=" " )
    print(         "PID=[%d]" % ucPID         , end=" " )
    print(         "LEN=[%d]" % nDataBytes              )
    print( ""                                 , end="\t")
    print( "DATA-HEX"                         , end=""  )
    
    for ucByte in ucTxRxBuffer[6:nRetVal] :
        print("[%02X]" % ucByte, end="" )
    #for

    print("")
        
#def PrintRxJ1708Message
    
#-----------------------------------------------------------------------------------------------------
# Print a sent J1708/J1587 message.
#-----------------------------------------------------------------------------------------------------
    
def PrintTxJ1708Message( nLength, ucTxRxBuffer ) :
    '''This function prints a transmitted J1708/J1587 message to the screen.'''
        
    ucPRI      = c_char(0)
    ucMID      = c_char(0)
    ucPID      = c_char(0)
    nDataBytes = c_short(0)

    ucPRI      = struct.unpack( 'B', ucTxRxBuffer[0]   )
    ucMID      = struct.unpack( 'B', ucTxRxBuffer[1]   )
    ucPID      = struct.unpack( 'B', ucTxRxBuffer[2]   )

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

#def PrintTxJ1708Message

#-----------------------------------------------------------------------------------------------------
# Send a request for J1708/J1587 VIN (PID=0, VIN=.
#-----------------------------------------------------------------------------------------------------

def SendJ1708RequestMessage( nClientID ) :
    '''This function sends a J1708 request PID=0 for VIN (PID=237).'''

    ucPRI      = c_char(0)
    ucMID      = c_char(0)
    ucPID      = c_char(0)
    nDataBytes = c_short(0)
    
    ucTxRxBuffer[0] = 8     # Lowest Priority
    ucTxRxBuffer[1] = 172   # Offboard PC 1
    ucTxRxBuffer[2] = 0x00  # Request PID
    ucTxRxBuffer[3] = 237   # VIN
    nDataBytes      = 4;
  
    nRetVal = RP1210_SendMessage( c_short( nClientID ), byref( ucTxRxBuffer ), c_short( nDataBytes ), c_short( 0 ), c_short( NON_BLOCKING_IO ) )
  
    if  nRetVal != 0 :
        print("RP1210_SendMessage( J1708 ) returns %i" % nRetVal )
    else :
        PrintTxJ1708Message( nDataBytes, ucTxRxBuffer )
    #if

#def PrintTxJ1708Message

#-----------------------------------------------------------------------------------------------------
# Print a received J1939 message.
#-----------------------------------------------------------------------------------------------------

def PrintRxJ1939Message( nRetVal, ucTxRxBuffer ) :
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

    print( "Rx J1939 TS=[%d]"   % iTS         , end=" " )
    print(         "PGN=[%d]"   % iPGN.value  , end=" " )
    print(          "CM=[%s]"   % szHow       , end=" " )
    print(         "PRI=[%d]"   % maskedPri   , end=" " )
    print(         "SRC=[%02X]" % iSRC        , end=" " )
    print(         "DST=[%02X]" % iDST        , end=" " )
    print(         "LEN=[%d]"   % nDataBytes            )
    print( ""                                 , end="\t")
    print( "DATA-HEX"                         , end=""  )

    for ucByte in ucTxRxBuffer[10:nRetVal] :
         print("[%02X]" % ucByte, end="" )
    #for

    print("")

#def PrintRxJ1939Message

#-----------------------------------------------------------------------------------------------------
# Print a transmitted J1939 message.
#-----------------------------------------------------------------------------------------------------

def PrintTxJ1939Message( nRetVal, ucTxRxBuffer ) :
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

    print( "Tx J1939 PGN=[%d]"   % iPGN.value  , end=" " )
    print(           "CM=[%s]"   % szHow       , end=" " )
    print(          "PRI=[%d]"   % maskedPri   , end=" " )
    print(          "SRC=[%02X]" % iSRC        , end=" " )
    print(          "DST=[%02X]" % iDST        , end=" " )
    print(          "LEN=[%d]"   % nDataBytes            )
    print( ""                                  , end="\t")
    print( "DATA-HEX"                          , end=""  )

    for ucByte in ucTxRxBuffer[6:nRetVal] :
         print("[%02X]" % ucByte, end="" )
    #for

    print("")

#def PrintTxJ1939Message

#-----------------------------------------------------------------------------------------------------
#  Send a request for J1939 Component ID (PID=0, VIN=65259).
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
    ucTxRxBuffer[6] = 0xEB        # LSB First of PGN65260 0x00FEEC
    ucTxRxBuffer[7] = 0xFE        # Middle
    ucTxRxBuffer[8] = 0x00        # High Byte
    
    nDataBytes = 9;
  
    nRetVal = RP1210_SendMessage( c_short( nClientID ), byref( ucTxRxBuffer ), c_short( nDataBytes ), c_short( 0 ), c_short( NON_BLOCKING_IO ) )
  
    if  nRetVal != 0 :
        print("RP1210_SendMessage( J1939 ) returns %i" % nRetVal )
    else :
        PrintTxJ1939Message( nDataBytes, ucTxRxBuffer )
    #if

#def SendJ1939RequestMessage

#-----------------------------------------------------------------------------------------------------
# Print a received CAN message.
#-----------------------------------------------------------------------------------------------------

def PrintRxCANMessage( nRetVal, ucTxRxBuffer ) :
    '''This function prints a received CAN message to the screen.'''

    iTS        = c_int  (0)
    ucCANType  = c_char (0)
    iCANType   = c_int  (0)

    iCANID     = c_int  (0)

    nDataBytes = c_short(0)

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

    nDataBytes = nRetVal - iDataIdx

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

    nDataBytes = c_short(0)

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

    nDataBytes = nRetVal - iDataIdx

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

#def SendCANRequestMessage

#
#        
#-----------------------------------------------------------------------------------------------------
# main() Code Body
#-----------------------------------------------------------------------------------------------------
#
#
print( "-------------------------------------------------------------------------------------" )
print( "%s" %PROGRAM_ID                                                                        )
print( "-------------------------------------------------------------------------------------" )

#-----------------------------------------------------------------------------------------------------
# Get the DLL name to use.
#-----------------------------------------------------------------------------------------------------

iAdapterID = 0

while iAdapterID > 6 or iAdapterID < 1 :
   print( "                                                                         " )
   print( "------------------------------------------------------------------------ " )
   print( " Select Adapter To Use                                                   " )
   print( "------------------------------------------------------------------------ " )
   print( "                                                                         " )
   print( " 1 = DPA 4 Plus Single-Application           ( DLL Name =  DPA4PSA.DLL ) " )
   print( " 2 = DPA 4 Plus Multi-Application            ( DLL Name =  DPA4PMA.DLL ) " )
   print( " 3 = DPA 5      Single-Application           ( DLL Name = DGDPA5SA.DLL ) " )
   print( " 4 = DPA 5      Multi-Application            ( DLL Name = DGDPA5MA.DLL ) " )
   print( " 5 = DPA 4 Plus And Prior DPAs               ( DLL Name = DG121032.DLL ) " )
   print( " 6 = Allison DR Drivers ( DPA 4 Plus/DPA 5 ) ( DLL Name = DR121032.DLL ) " )
   print( "                                                                         " )
   
   iAdapterID = int( input( "-> " ) )

   if iAdapterID == 1:
      szDLLName = "DPA4PSA.DLL" 
      break
   #if
   if iAdapterID == 2: 
      szDLLName =   "DPA4PMA.DLL" 
      break
   #if
   if iAdapterID == 3: 
      szDLLName =  "DGDPA5SA.DLL" 
      break
   #if
   if iAdapterID == 4: 
      szDLLName =  "DGDPA5MA.DLL" 
      break
   #if
   if iAdapterID == 5: 
      szDLLName =  "DG121032.DLL" 
      break
   #if
   if iAdapterID == 6: 
      szDLLName =  "DR121032.DLL" 
      break
   #if

# while

#-----------------------------------------------------------------------------------------------------
# Get the Protocol name to use.
#-----------------------------------------------------------------------------------------------------

iProtocolID = 0

while iProtocolID < 1 or iProtocolID > 5 :
   print( "                                                                     " )
   print( "---------------------------------------------------------------------" )
   print( " Selection Protocol To Use                                           " )
   print( "---------------------------------------------------------------------" )
   print( "                                                                     " )
   print( " 1 = J1708                                                           " )
   print( " 2 = J1939                                                           " )
   print( " 3 = J1939:Baud=Auto  ( Automatic Baud Detect )                      " )
   print( " 4 = CAN                                                             " )
   print( " 5 = CAN:Baud=Auto    ( Automatic Baud Detect )                      " )
   print( "                                                                     " )
   print(  )
   
   iProtocolID = int( input( "-> " ) )

   if iProtocolID == 1:
      szProtocolName = bytes( "J1708" , 'ascii' )
      break
   #if
   if iProtocolID == 2: 
      szProtocolName = bytes( "J1939" , 'ascii' )
      break
   #if
   if iProtocolID == 3: 
      szProtocolName = bytes( "J1939:Baud=Auto" , 'ascii' )
      break
   #if
   if iProtocolID == 4: 
      szProtocolName = bytes( "CAN" , 'ascii' )
      break
   #if
   if iProtocolID == 5: 
      szProtocolName = bytes( "CAN:Baud=Auto" , 'ascii' )
      break
   #if

# while

#-----------------------------------------------------------------------------------------------------
# Get the DeviceID to use.
#-----------------------------------------------------------------------------------------------------

print( "                                                                      " )
print( "--------------------------------------------------------------------- " )
print( " Select Device To Use                                                 " )
print( "--------------------------------------------------------------------- " )
print( "                                                                      " )

if iAdapterID == 1 or iAdapterID == 2 :
   print( " Common DPA 4 Plus Single-Application/Multi-Application Devices   " )
   print( "     1   =  DPA 4 Plus - USB                                      " )
#if
if iAdapterID == 3 or iAdapterID == 4 :
   print( " Common DPA 5 Single-Application/Multi-Application Devices        " )
   print( "     1   =  DPA 5 - USB                                           " )
#if
if iAdapterID == 5 :
   print( " Common DG121032.ini Devices                                      " )
   print( "     150 =  DPA 4/4 Plus USB                                      " )
   print( "     101 =  DPA II/II+/III+ Serial Using COM1                     " )
   print( "     102 =  DPA II/II+/III+ Serial Using COM2                     " )
#if
if iAdapterID == 6 :
   print( " Common DR121032.ini Devices                                      " )
   print( "     150 =  DPA 4 USB                                             " )
   print( "     151 =  DPA 4 Plus USB and DPA 5 USB                          " )
#if

print( "                                                                      " )
print( " These are the most common DG Technologies devices based on the DLL   " )
print( " that was selected.  Other device numbers may exist in that INI file  " )
print( " such as Bluetooth entries for the DPA 5 ( beginning at 160 ).        " )
print( " Please enter the device number you would like to use.                " )
print( "                                                                      " )

iDeviceID = int( input( "-> " ) )
 
#-----------------------------------------------------------------------------------------------------
#  Load the RP1210 Library, assign function pointers.
#-----------------------------------------------------------------------------------------------------

try :
    hRP1210DLL = windll.LoadLibrary( szDLLName )
except :
    print("Error loading the DLL.")
    sys.exit(1)
#try
        
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

#-----------------------------------------------------------------------------------------------------
# Call RP1210_ReadVersion to get DLL Major/Minor and API Major/Minor values.
#-----------------------------------------------------------------------------------------------------

nRetVal = RP1210_ReadVersion( byref( fpchDLLMajorVersion ), byref( fpchDLLMinorVersion ),byref( fpchAPIMajorVersion ),byref( fpchAPIMinorVersion ))

if nRetVal == 0 :
   print('DLL MAJ/MIN = %s.%s'  %( str( fpchDLLMajorVersion, 'ascii' ), str( fpchDLLMinorVersion, 'ascii' ) ) )
   print('API MAJ/MIN = %s.%s'  %( str( fpchAPIMajorVersion, 'ascii' ), str( fpchAPIMinorVersion, 'ascii' ) ) )
else :
   print("ReadVersion fails with a return value of  %i" %nRetVal )
#if

#-----------------------------------------------------------------------------------------------------
# Call RP1210_ReadDetailedVersion to get DLL, API, FW versions.
#-----------------------------------------------------------------------------------------------------

nRetVal = RP1210_ReadDetailedVersion( c_short( nClientID ), byref( chAPIVersionInfo ), byref( chDLLVersionInfo ), byref( chFWVersionInfo ) )

if nRetVal == 0 :
   szAPI = str( chAPIVersionInfo, 'ascii' )
   szDLL = str( chDLLVersionInfo, 'ascii' )
   szFW  = str( chFWVersionInfo , 'ascii' )

   print('DLL = %s' % szDLL  )
   print('API = %s' % szAPI  )
   print('FW  = %s' % szFW   )
else :   
   print("ReadDetailedVersion fails with a return value of  %i" %nRetVal )
#if

#-----------------------------------------------------------------------------------------------------
# Set all filters to pass.  This allows messages to be read.
#-----------------------------------------------------------------------------------------------------

nRetVal = RP1210_SendCommand( c_short( RP1210_Set_All_Filters_States_to_Pass ), c_short( nClientID ), None, 0 )

if nRetVal == 0 :
   print("RP1210_Set_All_Filters_States_to_Pass - SUCCESS" )
else :
   print('RP1210_Set_All_Filters_States_to_Pass returns %i' %nRetVal )
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
   
   print( "Claiming J1939 address 249" )
   
   ucTxRxBuffer[0] = c_char( 249 )
   ucTxRxBuffer[1] = c_char(   0 )
   ucTxRxBuffer[2] = c_char(   0 )
   ucTxRxBuffer[3] = c_char(  96 )
   ucTxRxBuffer[4] = c_char(   1 )
   ucTxRxBuffer[5] = c_char(   0 )
   ucTxRxBuffer[6] = c_char( 129 )
   ucTxRxBuffer[7] = c_char(   0 )
   ucTxRxBuffer[8] = c_char(   0 )
   ucTxRxBuffer[9] = c_char( BLOCK_UNTIL_DONE )

   nRetVal = RP1210_SendCommand( c_short( RP1210_Protect_J1939_Address ), c_short( nClientID ), byref( ucTxRxBuffer ), 10 )

   if nRetVal == 0 :
      print("RP1210_Protect_J1939_Address - SUCCESS" )
   else :
      print("RP1210_Protect_J1939_Address returns %i" %nRetVal )
   #if

#if

#-----------------------------------------------------------------------------------------------------
# Set a main read/process loop.  Send message every 5 seconds.
#-----------------------------------------------------------------------------------------------------

tLastTimeRequestsSent = time()

while True:

   if msvcrt.kbhit():
      break
   #if

   nRetVal = RP1210_ReadMessage( c_short( nClientID ), byref( ucTxRxBuffer ), c_short( 2000 ), c_short( NON_BLOCKING_IO ) )
   
   if nRetVal > 0 :

      if ProtocolName.find( "J1708" ) != -1 :
         PrintRxJ1708Message( nRetVal, ucTxRxBuffer )

      elif ProtocolName.find( "J1939" ) != -1 :
         PrintRxJ1939Message( nRetVal, ucTxRxBuffer )

      elif ProtocolName.find( "CAN" ) != -1 :
         PrintRxCANMessage( nRetVal, ucTxRxBuffer )

      #if

   elif nRetVal < 0 :

      print( "RP1210_ReadMessage returns %i" %nRetVal )

   #if

   tDeltaTime = ( time() - tLastTimeRequestsSent )

   if tDeltaTime > 5 :

      if ProtocolName.find( "J1708" ) != -1 :
         SendJ1708RequestMessage( nClientID )

      elif ProtocolName.find( "J1939" ) != -1 :
         SendJ1939RequestMessage( nClientID )

      elif ProtocolName.find( "CAN" ) != -1 :
         SendCANRequestMessage( nClientID )
      #if

      tLastTimeRequestsSent = time() 

   #if

#while

#-----------------------------------------------------------------------------------------------------
# Disconnect from the data bus.  Python will handle the cleanup and will call FreeLibrary().
#-----------------------------------------------------------------------------------------------------

nRetVal = RP1210_ClientDisconnect( c_short( nClientID ) )

if nRetVal == 0 :
   print("RP1210_ClientDisconnect - SUCCESS" )
else :
   print("RP1210_ClientDisconnect returns %i" %nRetVal )
#if
