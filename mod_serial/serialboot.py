#!/usr/bin/env python
import serial
from time import sleep
ser = serial.Serial('/dev/ttyUSB0',115200, timeout=0)
import sys

while ser:
     ser.write(chr(27))
     ser.flush()
     sleep(0.00001)

     try:
         x = ser.read()
         sys.stdout.write(x)
         pass
     except serial.serialutil.SerialException:
         pass

