# RP1210 Hello World
#                  Dr. Jeremy Daily
#                  Associate Professor of Mechanical Engineering
#                  University of Tulsa
#                  800 S. Tucker Dr.
#                  Tulsa, OK 74104

import struct
import sys
import os
import msvcrt
from   ctypes import *
from   ctypes.wintypes import HWND
from   array import *
from   time import *

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


# Connect to Device
print( "Attempting connect to DLL [%s], DeviceID [%d]" %( dllName, deviceID ) )

szProtocolName = bytes("J1939",'ascii')
nClientID = RP1210_ClientConnect( HWND(None), c_short( deviceID ), szProtocolName, 0, 0, 0  )

print('The Client ID is: %i' %nClientID )

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

# Disconnect from the VDA

input("Press Enter to Quit.")

nRetVal = RP1210_ClientDisconnect( c_short( nClientID ) )

if nRetVal == 0 :
   print("RP1210_ClientDisconnect - SUCCESS" )
else :
   print("RP1210_ClientDisconnect returns %i" %nRetVal )
