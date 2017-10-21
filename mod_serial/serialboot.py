import serial
ser = serial.Serial('/dev/ttyUSB0',115200, timeout=1)
import sys

while ser:
     x = ser.read()
     sys.stdout.write(x)
# ser.write(b'h')