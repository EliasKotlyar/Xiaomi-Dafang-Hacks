#!/bin/sh

getgpio(){
GPIOPIN=$1
cat /sys/class/gpio/gpio$GPIOPIN/value
}

## Uptime
/system/sdcard/bin/busybox uptime
echo " - "

## Wifi
SSID=`/system/bin/iwconfig 2>/dev/null | grep ESSID | sed -e "s/.*ESSID:\"//" | sed -e "s/\".*//"`
BITRATE=`/system/bin/iwconfig 2>/dev/null | grep "Bit R" | sed -e "s/   S.*//" | sed -e "s/.*\://"` 
QUALITY=`/system/bin/iwconfig 2>/dev/null | grep "Quali" | sed -e "s/  *//"`
echo "SSID: $SSID, Bitrate: $BITRATE, $QUALITY - "

## LED Status - (@pplucky &  @lolouk44)
# Blue Led
blue=$(getgpio 39)
# Yellow Led
yellow=$(getgpio 38)
# IR Cut
ir_cut=$(getgpio 26)
# IR Led
ir_led=$(getgpio 49)
echo "LEDs: blue=$blue, yellow=$yellow, IR=$ir_led - "
echo "IR-Cut=$ir_cut - "

## RTSP status
string=$(pidof v4l2rtspserver-master)
if [[ ${#string} == "0" ]]; then
  echo "RTSP-Server not running"
else
  echo "RTSP-Server running"
fi

## enable this for the format used befor
# echo $blue,$yellow,$ir_cut,$ir_led,$rstp
