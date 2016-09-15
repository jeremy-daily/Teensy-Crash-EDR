# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 09:14:18 2016

@author: jeremy
"""

import serial

ser = serial.Serial("COM9")
while(1):
    print(ser.readline())
