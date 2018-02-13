#!/bin/sh

getgpio(){
GPIOPIN=$1
cat /sys/class/gpio/gpio$GPIOPIN/value
}

## Date and Time
date

## Uptime
SECONDS=`cat /proc/uptime | awk '{ print $1; }' | sed -e "s/\..*//"`

# Calculate hours, minutes, seconds idea taken from https://blog.jkip.de/in-bash-sekunden-umrechnen-in-stunden-minuten-und-sekunden/
    local seconds=$SECONDS
    local sign=""
    if [[ ${seconds:0:1} == "-" ]]; then
        seconds=${seconds:1}
        sign="-"
    fi
    local days=$(( seconds / 86400 ))
    local hours=$(( seconds / 3600 ))
    local minutes=$(( (seconds % 3600) / 60 ))
    seconds=$(( seconds % 60 ))

echo "Uptime: $days days $hours hours $minutes minutes $seconds seconds - "

## Load
LOAD=`cat /proc/loadavg | awk '{ print $1", " $2", " $3 }'`
echo "Load: $LOAD - "

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
