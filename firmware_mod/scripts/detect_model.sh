#!/bin/sh

# Try to detect hardware model
if [ -f /driver/8189es.ko ]; then
  # Its a DaFang
  echo "Xiaomi Dafang"
elif [ -f /driver/8189fs.ko ]; then
  # Its a XiaoFang T20
  echo "Xiaomi Xiaofang 1S"
else
  # Its a Wyzecam V2
  echo "Wyzecam V2"
fi
