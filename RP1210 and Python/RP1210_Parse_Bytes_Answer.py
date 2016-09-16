# RP1210 Hello World
# Dr. Jeremy Daily
# Associate Professor of Mechanical Engineering
# The University of Tulsa
# 800 S. Tucker Dr.
# Tulsa, OK 74104
#
# This is a minimal program that tests to see if you can connect to an RP1210 device.
# It add the ability to print raw byte strings to the console.
#
# Assignment: Add a function that can interpret the RP1210 Byte Fields.

import struct
import sys
import os
import msvcrt
from   ctypes import *
from   ctypes.wintypes import HWND
from   array import *
from   time import *

def interpretRP1210Fields (bufferAsBytes,nRetVal,protocol):
	'''This function provides a way to separate out the bytes from a received RP1210 message.'''
	if "J1939" in protocol:
		timeStamp = int(struct.unpack('>L',(ucTxRxBuffer[0]+ucTxRxBuffer[1]+ucTxRxBuffer[2]+ucTxRxBuffer[3]))[0])
		PGN       = int(struct.unpack('<L',(ucTxRxBuffer[4]+ucTxRxBuffer[5]+ucTxRxBuffer[6]+b'\x00'))[0])
		HowSentAndPriority   =  int( struct.unpack( 'B', ucTxRxBuffer[7] )[0])
		priority = int( HowSentAndPriority & 0x07)
		HowSent  = int((HowSentAndPriority & 0x80) >> 7 )
		SourceAddress      = struct.unpack( 'B', ucTxRxBuffer[8]   )[0]
		DestinationAddress = struct.unpack( 'B', ucTxRxBuffer[9]   )[0]
		
		
		nDataBytes = nRetVal - 10
		print("J1939",end=",")
		print("%10i" %timeStamp, end="," )
		print(PGN, end="," )
		print(priority, end="," )
		print(HowSent, end="," )
		print(SourceAddress, end="," )
		print(DestinationAddress, end="" )
		for ucByte in ucTxRxBuffer[10:nRetVal] :
			print(",%02X" %ucByte, end="" )
		print()
	return 

	
	
#define the name of the RP1210 DLL
dllName =   "DPA4PMA.DLL" 

#define the protocol ID:
protocolID = 2

#define the device ID 
deviceID = 1

#Load the Windows Device Library
RP1210DLL = windll.LoadLibrary( dllName )
        
# Define windows prototype functions:
# typedef short (WINAPI *fxRP1210_ClientConnect)       ( HWND, short, char *, long, long, short );
prototype                   = WINFUNCTYPE( c_short, HWND, c_short, c_char_p, c_long, c_long, c_short)
RP1210_ClientConnect        = prototype( ( "RP1210_ClientConnect", RP1210DLL ) )

# typedef short (WINAPI *fxRP1210_ClientDisconnect)    ( short                                  );
prototype                   = WINFUNCTYPE( c_short, c_short )
RP1210_ClientDisconnect     = prototype( ( "RP1210_ClientDisconnect", RP1210DLL ) )

# typedef short (WINAPI *fxRP1210_SendMessage)         ( short, char*, short, short, short      );
prototype                   = WINFUNCTYPE( c_short, c_short,  POINTER( c_char*2000 ), c_short, c_short, c_short      )
RP1210_SendMessage          = prototype( ("RP1210_SendMessage", RP1210DLL ) )

# typedef short (WINAPI *fxRP1210_ReadMessage)         ( short, char*, short, short             );
prototype                   = WINFUNCTYPE( c_short, c_short, POINTER( c_char*2000 ), c_short, c_short             )
RP1210_ReadMessage          = prototype( ("RP1210_ReadMessage", RP1210DLL ) )

# typedef short (WINAPI *fxRP1210_SendCommand)         ( short, short, char*, short             );
prototype                   = WINFUNCTYPE( c_short, c_short, c_short, POINTER( c_char*2000 ), c_short             )
RP1210_SendCommand          = prototype( ("RP1210_SendCommand", RP1210DLL ) )

# typedef short (WINAPI *fxRP1210_ReadVersion)         ( char*, char*, char*, char*             );
prototype                   = WINFUNCTYPE( c_short, c_char_p, c_char_p, c_char_p, c_char_p             )
RP1210_ReadVersion          = prototype( ("RP1210_ReadVersion", RP1210DLL ) )

# typedef short (WINAPI *fxRP1210_ReadDetailedVersion) ( short, char*, char*, char*             );
prototype                   = WINFUNCTYPE( c_short, c_short, POINTER(c_char*17), POINTER(c_char*17), POINTER(c_char*17) )
RP1210_ReadDetailedVersion  = prototype( ("RP1210_ReadDetailedVersion", RP1210DLL ) )

# typedef short (WINAPI *fxRP1210_GetHardwareStatus)   ( short, char*, short, short             );
prototype                   = WINFUNCTYPE( c_short, c_short, c_char_p, c_short, c_short             )
RP1210_GetHardwareStatus    = prototype( ("RP1210_GetHardwareStatus", RP1210DLL ) )

# typedef short (WINAPI *fxRP1210_GetErrorMsg)         ( short, char*                           );
prototype                   = WINFUNCTYPE( c_short, c_short, c_char_p                           )
RP1210_GetErrorMsg          = prototype( ("RP1210_GetErrorMsg", RP1210DLL ) )

# typedef short (WINAPI *fxRP1210_GetLastErrorMsg)     ( short, int *, char*, short             );
prototype                   = WINFUNCTYPE( c_short, c_void_p, c_char_p, c_short             )
RP1210_GetLastErrorMsg      = prototype( ("RP1210_GetLastErrorMsg", RP1210DLL ) )

clientNames = {} # build a dictionary of client Connect sessions


# Connect to Device
print( "Attempting connect to DLL [%s], DeviceID [%d]" %( dllName, deviceID ) )
szProtocolName = bytes("J1939:Channel=1;Baud=Auto",'ascii') #This protocol name comes from the .ini file in the Windows directory.
nClientID = RP1210_ClientConnect( HWND(None), c_short( deviceID ), szProtocolName, 0, 0, 0  )
clientNames[nClientID] = str(szProtocolName,'ascii')
print('The Client ID is: %i for Protocol: %s' %(nClientID, str(szProtocolName,'ascii') ))

# szProtocolName = bytes("J1708",'ascii') #This protocol name comes from the .ini file in the Windows directory.
# nClientID = RP1210_ClientConnect( HWND(None), c_short( deviceID ), szProtocolName, 0, 0, 0  )
# clientNames[nClientID] = str(szProtocolName,'ascii')
# print('The Client ID is: %i for Protocol: %s' %(nClientID, str(szProtocolName,'ascii') ))



#-----------------------------------------------------------------------------------------------------
# Call RP1210_ReadDetailedVersion to get DLL, API, FW versions.
#-----------------------------------------------------------------------------------------------------


chAPIVersionInfo    = (c_char*17)()
chDLLVersionInfo    = (c_char*17)()
chFWVersionInfo     = (c_char*17)()
nRetVal = RP1210_ReadDetailedVersion( c_short( nClientID ), byref( chAPIVersionInfo ), byref( chDLLVersionInfo ), byref( chFWVersionInfo ) )

if nRetVal == 0 :
   print('Congratulations! You have connected to a VDA! No need to check your USB connection.')
   print('DLL = %s' % str( chDLLVersionInfo, 'ascii' ) )
   print('API = %s' % str( chAPIVersionInfo, 'ascii' ) )
   print('FW  = %s' % str( chFWVersionInfo , 'ascii' ) )
else :   
   print("ReadDetailedVersion fails with a return value of  %i" %nRetVal )

# Set all filters to pass.  This allows messages to be read.
RP1210_Set_All_Filters_States_to_Pass = 3 
nRetVal = RP1210_SendCommand( c_short( RP1210_Set_All_Filters_States_to_Pass ), c_short( nClientID ), None, 0 )

if nRetVal == 0 :
   print("RP1210_Set_All_Filters_States_to_Pass - SUCCESS" )
else :
   print('RP1210_Set_All_Filters_States_to_Pass returns %i' %nRetVal )

#Read some messages:
ucTxRxBuffer = (c_char*2000)()
NON_BLOCKING_IO = 0
while True:

	if msvcrt.kbhit():
		break
	
	nRetVal = RP1210_ReadMessage( c_short( nClientID ), byref( ucTxRxBuffer ), c_short( 2000 ), c_short( NON_BLOCKING_IO ) )
	if nRetVal > 0:
		print("RAW", end=",")
		print(ucTxRxBuffer[:nRetVal])
		interpretRP1210Fields (ucTxRxBuffer, nRetVal, clientNames[nClientID])
	
	
# Disconnect from the VDA

input("Press Enter to Quit.")

nRetVal = RP1210_ClientDisconnect( c_short( nClientID ) )

if nRetVal == 0 :
   print("RP1210_ClientDisconnect - SUCCESS" )
else :
   print("RP1210_ClientDisconnect returns %i" %nRetVal )
