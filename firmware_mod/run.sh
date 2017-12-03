#!/bin/sh
CONFIGPATH=/system/sdcard/config
echo "Starting up CFW"


## Start Wifi:
insmod /driver/8189es.ko
wpa_supplicant -B -i wlan0 -c $CONFIGPATH/wpa_supplicant.conf -P /var/run/wpa_supplicant.pid
udhcpc -i wlan0 -p /var/run/udhcpc.pid -b

## Start Audio:
insmod /driver/audio.ko
## Start Sensor:
insmod /driver/tx-isp.ko isp_clk=100000000
insmod /driver/sensor_jxf22.ko data_interface=2 pwdn_gpio=-1 reset_gpio=18 sensor_gpio_func=0

## Start FTP & SSH
/system/sdcard/bin/dropbearmulti dropbear -R
/system/sdcard/bin/bftpd -d

## Start Webserver:
/system/sdcard/bin/boa -c /system/sdcard/config/

echo "Startup finished!"

