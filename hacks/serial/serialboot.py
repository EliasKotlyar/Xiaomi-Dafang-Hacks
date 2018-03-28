# coding=utf-8
# !/usr/bin/env python
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
