#Teensy 3.2 Based Crash EDR Hardware
This repository contains the information needed to understand how the device is built. The schematic provides the data needed to program 
the different input and output pins. The Bill of Materials is comprehsive in that it includes the parts for the circuit card assembly as well as the additional parts.
##Errata
 1. The 5V0 net and Vin need to be connected. This must be done by soldering an extra jumper wire between those pins. This modification is required for CAN to work.
 2. The Adafruit Ultimate GPS module has a 3.3V regulator and can provide power to the board if it is installed. However, the 3.3V line from the GPS headers is not connected, so it needs to have a jumper connected.
 3. The A14 voltage monitor is not connected, so R4 and R5 are not needed. Alternatively, they could be connected by hand. However, this feature is not that interesting.
 4. The silkscreen on the power and CAN entry cables have CANH and CANL backwards. In other words, the yellow CANH wire should be soldered to the bottom side into the CANH labeled hole. This only applied to the Rev2 boards.
## Minimum Assembly
For interfacing with CAN and creating a CAN logger to work with cars and trucks, you do not need the following:
 * 9-DOF IMU breakout board
 * 200G Triaxial Accelerometer
 * ESP8266 Wifi
 * Battery and Battery Charger
 
## Assembly Notes
 * Mount the voltage regulator on the bottom of the board.
 * Use long pinned female headers for the 7 holes hear the USB port on the Teensy 3.2. This enables a battery charger to be placed in line with the Teensy 3.2 under the board.
 * The 9-DOF board needs to be mounted on the bottom to ensure clearance for the USB cable.
 * The values of the electrolytic capacitors can be anywhere from 22uF to 400uF.
 * The four wires that go out of the box should be soldered to the bottom of the board. It is recommended that this be one of the last steps.
 * Be sure to tap the M3 holes in the Bud Box so the brass standoffs don't snap off when tightening. 
 
### Other Notes
 * The Wireless module is untested as of September 2016. Please let me know if this works.
 * The accelerometers (9DOF and High-G) are also untested. Please let me know if they work.
 