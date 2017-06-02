#Teensy 3.6 Based Crash EDR Hardware
This repository contains the information needed to understand how the device is built. The schematic provides the data needed to program 
the different input and output pins. The Bill of Materials is comprehsive in that it includes the parts for the circuit card assembly as well as the additional parts.
##Errata for Revision 3
 1. The CAN tranceivers were not connected to the input pins. Therefore, some jumper wires are needed to connect the transievers to the circuit.
## Minimum Assembly
For interfacing with CAN and creating a CAN logger to work with cars and trucks, you do not need the following:
 * 9-DOF IMU breakout board
 * 200G Triaxial Accelerometer
 * ESP8266 Wifi
 * Battery and Battery Charger
 * GPS
 
## Assembly Notes
 * Mount the voltage regulator on the top of the board, but bend it backwards.
 * The USB cable is built into the board. jumper wires are needed to complete the connection to the D+ and D- pads of the Teensy.
 * The values of the electrolytic capacitors can be anywhere from 22uF to 400uF.
 
### Other Notes
 * The Wireless module is untested as of December 2016. Please let me know if this works.

 