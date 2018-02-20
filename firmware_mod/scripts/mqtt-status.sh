#!/bin/sh
source /system/sdcard/config/mqtt

getgpio(){
GPIOPIN=$1
cat /sys/class/gpio/gpio$GPIOPIN/value
}

## Uptime
UPTIME=`/system/sdcard/bin/busybox uptime`

## Wifi
SSID=`/system/bin/iwconfig 2>/dev/null | grep ESSID | sed -e "s/.*ESSID:\"//" | sed -e "s/\".*//"`
BITRATE=`/system/bin/iwconfig 2>/dev/null | grep "Bit R" | sed -e "s/   S.*//" | sed -e "s/.*\://"` 
QUALITY=`/system/bin/iwconfig 2>/dev/null | grep "Quali" | sed -e "s/  *//"`

## LED Status - (@pplucky &  @lolouk44)

# Blue Led
blue=$(getgpio 39)
if [ "$blue" == "0" ]; then blue="on"; fi
if [ "$blue" == "1" ]; then blue="off"; fi

# Yellow Led
yellow=$(getgpio 38)
if [ "$yellow" == "0" ]; then yellow="on"; fi
if [ "$yellow" == "1" ]; then yellow="off"; fi

# IR Cut
ir_cut=$(getgpio 26)
if [ "$ir_cut" == "0" ]; then ir_cut="on"; fi
if [ "$ir_cut" == "1" ]; then ir_cut="off"; fi


# IR Led
ir_led=$(getgpio 49)
if [ "$ir_led" == "0" ]; then ir_led="on"; fi
if [ "$ir_led" == "1" ]; then ir_led="off"; fi



## RTSP status
string=$(pidof v4l2rtspserver-master)
if [[ ${#string} == "0" ]]; then
	RTSPRUNNING="not running"
else
	RTSPRUNNING="running"
fi


if [ "$STATUSFORMAT" == "json" ]; then

NOISELEVEL=`echo $QUALITY |  awk '{ print $6}' | sed -e 's/.*=//' | sed -e 's/\/100/\%/'` 
LINKQUALITY=`echo $QUALITY |  awk '{ print $2}' | sed -e 's/.*=//' | sed -e 's/\/100/\%/'`
SIGNALLEVEL=`echo $QUALITY |  awk '{ print $4}' | sed -e 's/.*=//' | sed -e 's/\/100/\%/'`


echo "{\"Uptime\":\"$UPTIME\", \"RTSP-Server\":\"$RTSPRUNNING\", \"IR-Cut\":\"$ir_cut\", \"Wifi\":{\"SSID\":\"$SSID\", \"Bitrate\":\"$BITRATE\", \"SignalLevel\":\"$SIGNALLEVEL\", \"Linkquality\":\"$LINKQUALITY\", \"NoiseLevel\":\"$NOISELEVEL\"}, \"LEDs\":{\"Blue\":\"$blue\", \"Yellow\":\"$yellow\", \"Infrared\":\"$ir_led\"}}"


else
	echo "$UPTIME - "
	echo "SSID: $SSID, Bitrate: $BITRATE, $QUALITY - "
	echo "LEDs: blue=$blue, yellow=$yellow, IR=$ir_led - "
	echo "IR-Cut=$ir_cut - "
	echo "RTSP-Server: $RTSPRUNNING"
fi


## enable this for the format used befor
# echo $blue,$yellow,$ir_cut,$ir_led,$rstp
