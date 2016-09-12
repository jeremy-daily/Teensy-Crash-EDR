# Teensy-Crash-EDR
A Teensy 3.2 based through hole project that includes CAN, SD, an ADXL375 High G triaxial accelerometer, an AdaFruit Ultimate GPS breakout, An ESP

## Project Purpose
The goal of this project is to design and share an open source data acquisition device that can be used for vehicle crash testing. The crash tests
considered are typically done at crash reconstruction conferences or trainig events where law enforcement and private crash investigators
gather to witness a crash and solidify their understanding of the dynamics involved with such an event. 

Additionally, a light version (the one without the sensors) is designed to be used in training on Controller Area Networks and J1939.

## Hardware Features
 * Microprocessor: Teensy 3.2 32-bit ARM-Cortex M4 Arduino compatible microprocessor board
 * MicroSD Card for storage (Tested to log data at 4000Hz)
 * GPS: Adafruit Ultimate GPS capable of 10Hz update rates
 * High Speed CAN (1Mbps) capable of processing 100% bus load
 * Real Time Clock
 * High G Tri-axial accelerometer (+/- 200G)
 * Low G Tri-axial Accelerometer
 * Tri-axial Rate Gyro
 * Tri-axial Magnetometer
 * Battery Powered (Charges with USB)
 * Wi-Fi Capable (Internet of Things)
 * 7-36 VDC input with reverse polarity protection
 * Open source design and easily obtainable parts (See Hardware and Schematics directory)
 * Low cost
 * All through hole parts so it can be easily hand soldered.

## Learning to Write Software
The idea of this project is to enable students to start from the beginning and succeed with little or no previous experience with writing code for embedded processors.
There are a couple of prerequisites: 
 1. Arduino software (the code was developed and tested with version 1.6.11)
 2. Teensyduino software, which is an extension of Arduino (the code was developed and tested and developed with v1.30)
 3. The SdFat Arduino library
The idea of the code development is to take examples that are close to the functionality of what you are interested in and adapt them to the hardware we have. As such, some of the examples and projects have different
programming styles. This is because those programs extend the code base from different sources. 

The following sections describe the functional and learning objectives of each of the enumerated examples in this repository. They example programs (sometimes called sketches) are intended to be used in sequence. The assignment is to extend
the functionality of each of the code bases to demonstrate the learning objectives. 

### Lesson 1: Blink
This is a basic program that helps the student understand the process of writing a program and uploading it to the processor to run. The objective is to be able to change the blink rate and see the result.

Assignment: Change the Blink Rate by using an elapsedMillis timer.
### Lesson 2: Receive CAN messages
Introduce the FlexCAN library and print the CAN messages to the serial output.

Assignment: Change the output format to be comma separated values
### Lesson 3: Real Time Clock
Add the time keeping libraries so CAN messages can be timestamped with the real time
 
Assignment: Add the microseconds to each real time stamp. (Hint: You can use an IntervalTimer to reset an elapsedMicros counter every second.)

### Lesson 4: Send Request Messages for J1939
Add the ability to broadcast request messages for different J1939 parameters. Some data is only available upon request.

Assignment: Send requests to different Destination Addresses. Add another PGN to request to the list.
### Lesson 5: Interpret Simple J1939 Messages
Using the J1939-71 or J1939-DA interpret some interesting messages, like wheel speed.

Assignment: Add interpreters for a couple other signals of interest (e.g. Engine RPM or Front Axle Speed)
### Lesson 6: Write data to an SD Card
Log all CAN traffic to an SD Card.

Assignment: Send request messages so the responses get logged.

## Future Work
### Lesson 7: Add GPS data to the SD log files (to be written)
 
### Lesson 8: Read Sensor Data (to be written)

### Lesson 9: Implement an Extended Kalman Filter (to be written)