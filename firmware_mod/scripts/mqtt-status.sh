#!/bin/sh
source /system/sdcard/config/mqtt.conf
source /system/sdcard/scripts/common_functions.sh

## Uptime
uptime=$(/system/sdcard/bin/busybox uptime)

## Wifi
ssid=$(/system/bin/iwconfig 2>/dev/null | grep ESSID | sed -e "s/.*ESSID:\"//" | sed -e "s/\".*//")
bitrate=$(/system/bin/iwconfig 2>/dev/null | grep "Bit R" | sed -e "s/   S.*//" | sed -e "s/.*\\://")
quality=$(/system/bin/iwconfig 2>/dev/null | grep "Quali" | sed -e "s/  *//")
noise_level=$(echo "$quality" | awk '{ print $6}' | sed -e 's/.*=//' | sed -e 's/\/100/\%/')
link_quality=$(echo "$quality" | awk '{ print $2}' | sed -e 's/.*=//' | sed -e 's/\/100/\%/')
signal_level=$(echo "$quality" | awk '{ print $4}' | sed -e 's/.*=//' | sed -e 's/\/100/\%/')

echo "{\"uptime\":\"$uptime\", \"rtsp_server\":\"$(rtsp_server status)\", \"motion_detection\":\"$(motion_detection status)\", \"ssid\":\"$ssid\", \"bitrate\":\"$bitrate\", \"signal_level\":\"$signal_level\", \"link_quality\":\"$link_quality\", \"noise_level\":\"$noise_level\", \"blue_led\":\"$(blue_led status)\", \"yellow_led\":\"$(yellow_led status)\", \"ir_led\":\"$(ir_led status)\", \"ir_cut\":\"$(ir_cut status)\", \"ldr\":\"$(ldr status)\", \"night_mode\":\"$(night_mode status)\", \"auto_night_mode\":\"$(auto_night_mode status)\"}"
