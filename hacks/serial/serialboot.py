#!/usr/bin/env python
# coding=utf-8
import sys
from time import sleep

import serial

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=0)

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
