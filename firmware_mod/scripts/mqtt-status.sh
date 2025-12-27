#!/bin/sh
# shellcheck shell=busybox
# shellcheck source=config/mqtt.conf.dist
. /system/sdcard/config/mqtt.conf
# shellcheck source=scripts/common_functions.sh
. /system/sdcard/scripts/common_functions.sh

## Uptime
uptime=$(/system/sdcard/bin/busybox uptime)

## Wifi
ssid=$(/system/bin/iwconfig 2>/dev/null | grep ESSID | sed -e "s/.*ESSID:\"//" | sed -e "s/\".*//")
bitrate=$(/system/bin/iwconfig 2>/dev/null | grep "Bit R" | sed -e "s/   S.*//" | sed -e "s/.*\\://")
quality=$(/system/bin/iwconfig 2>/dev/null | grep "Quali" | sed -e "s/  *//")
noise_level=$(echo "$quality" | awk '{ print $6}' | sed -e 's/.*=//' | sed -e 's/\/100/\%/')
link_quality=$(echo "$quality" | awk '{ print $2}' | sed -e 's/.*=//' | sed -e 's/\/100/\%/')
signal_level=$(echo "$quality" | awk '{ print $4}' | sed -e 's/.*=//' | sed -e 's/\/100/\%/')

echo "{\"uptime\":\"$uptime\",  \"ssid\":\"$ssid\", \"bitrate\":\"$bitrate\", \"signal_level\":\"$signal_level\", \"link_quality\":\"$link_quality\", \"noise_level\":\"$noise_level\" }"
