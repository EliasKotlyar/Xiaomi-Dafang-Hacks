#!/bin/sh

# Check for orientation setting
if [ `/system/sdcard/bin/setconf -g f` -eq 1 ]; then
    # We are flipped, so check direction variable and reverse
    case $2 in
         u) flip=d ;;
         d) flip=u ;;
         r) flip=l ;;
         l) flip=r ;;
         *) flip=$2 ;;
    esac
else
    flip=$2
fi

# Send command to motor binary
/system/sdcard/bin/motor.bin $1 $flip $3 $4

