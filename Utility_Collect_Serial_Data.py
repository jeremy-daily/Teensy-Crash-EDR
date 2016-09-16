# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 09:14:18 2016

@author: jeremy
"""

import serial


for i in range(1000):
    ser = serial.Serial("COM9")
    dataLine = ser.readline()
    ser.close()
    with open("C:\\Users\\jeremy\\Documents\\SpeedData.csv",'a') as dataFile:
        print(str(dataLine,'ascii').rstrip())
        dataFile.write(str(dataLine,'ascii').rstrip())
   