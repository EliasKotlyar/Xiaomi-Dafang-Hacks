#!/bin/sh
## Start Wifi:
wpa_supplicant -B -i wlan0 -c /system/sdcard/wpa_supplicant.conf -P /var/run/wpa_supplicant.pid
udhcpc -i wlan0 -p /var/run/udhcpc.pid -b

## Start Sensor:
insmod /driver/sensor_jxf22.ko data_interface=2 pwdn_gpio=-1 reset_gpio=18 sensor_gpio_func=0

## Start FTP & SSH
/system/sdcard/bin/dropbearmulti dropbear -R
/system/dafang/bin/bftpd -d




