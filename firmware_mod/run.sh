#!/bin/sh

CONFIGPATH=/system/sdcard/config
echo "Starting up CFW"

## Load some common functions
. /system/sdcard/scripts/common_functions.sh

## Update the hostname:
hostname -F $CONFIGPATH/hostname.conf

## Get real Mac address from config file:
MAC=$(grep MAC < /params/config/.product_config | cut -c16-27 | sed 's/\(..\)/\1:/g;s/:$//')

## Start Wifi:
insmod /driver/8189es.ko rtw_initmac="$MAC"
wpa_supplicant -B -i wlan0 -c $CONFIGPATH/wpa_supplicant.conf -P /var/run/wpa_supplicant.pid
udhcpc -i wlan0 -p /var/run/udhcpc.pid -b -x hostname:"$(hostname)"

## Sync the via NTP
ntp_srv="$(cat "$CONFIGPATH/ntp_srv.conf")"
/system/sdcard/bin/busybox ntpd -q -n -p "$ntp_srv"

## Load audio driver module:
insmod /system/sdcard/driver/audio.ko

## Initialize the GPIOS
for pin in 25 26 38 39 49; do
  init_gpio $pin
done
# the ir_led pin is a special animal and needs active low
echo 1 > /sys/class/gpio/gpio49/active_low

## Set leds to default startup states
ir_led off
ir_cut on
yellow_led off
blue_led on

# Load motor driver module 
insmod /system/sdcard/driver/sample_motor.ko
# Don't calibrate the motors for now as for newer models the endstops don't work:
#motor hcalibrate
#motor vcalibrate

## Start Sensor:
insmod /system/sdcard/driver/tx-isp.ko isp_clk=100000000
insmod /system/sdcard/driver/sensor_jxf22.ko data_interface=2 pwdn_gpio=-1 reset_gpio=18 sensor_gpio_func=0

## Start FTP & SSH
/system/sdcard/bin/dropbearmulti dropbear -R
/system/sdcard/bin/bftpd -d

## Start Webserver:
/system/sdcard/bin/boa -c /system/sdcard/config/
#/system/sdcard/bin/lighttpd -f /system/sdcard/config/lighttpd.conf

## Configure OSD
if [ -f /system/sdcard/controlscripts/configureOsd ]; then
    . /system/sdcard/controlscripts/configureOsd  2>/dev/null
fi

## Configure Motion
if [ -f /system/sdcard/controlscripts/configureMotion ]; then
    . /system/sdcard/controlscripts/configureMotion  2>/dev/null
fi


## Autostart
for i in /system/sdcard/config/autostart/*; do
  $i
done

echo "Startup finished!"
