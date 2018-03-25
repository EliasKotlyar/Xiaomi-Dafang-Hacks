#!/bin/sh

CONFIGPATH=/system/sdcard/config
echo "Starting up CFW"

## Update hostname:
hostname -F $CONFIGPATH/hostname.conf

## Get real Mac address from config file:
MAC=$(grep MAC < /params/config/.product_config | cut -c16-27 | sed 's/\(..\)/\1:/g;s/:$//')

## Start Wifi:
insmod /driver/8189es.ko rtw_initmac="$MAC"
wpa_supplicant -B -i wlan0 -c $CONFIGPATH/wpa_supplicant.conf -P /var/run/wpa_supplicant.pid
udhcpc -i wlan0 -p /var/run/udhcpc.pid -b -x hostname:"$(hostname)"

## Start Audio:
insmod /system/sdcard/driver/audio.ko

## Start GPIO:
setgpio () {
  GPIOPIN=$1
  echo "$GPIOPIN" > /sys/class/gpio/export
  echo out > "/sys/class/gpio/gpio$GPIOPIN/direction"
  echo 0 > "/sys/class/gpio/gpio$GPIOPIN/active_low"
  echo 1 > "/sys/class/gpio/gpio$GPIOPIN/value"
}

# IR-LED
setgpio 49
echo 1 > /sys/class/gpio/gpio49/active_low
echo 1 > /sys/class/gpio/gpio49/value
# Yellow-LED
setgpio 38
echo 0 > /sys/class/gpio/gpio38/value
# Blue-LED
setgpio 39
# IR-Cut:
setgpio 25
setgpio 26

# Startup Motor:
insmod /system/sdcard/driver/sample_motor.ko

## Start Sensor:
insmod /system/sdcard/driver/tx-isp.ko isp_clk=100000000
insmod /system/sdcard/driver/sensor_jxf22.ko data_interface=2 pwdn_gpio=-1 reset_gpio=18 sensor_gpio_func=0

## Update time
/system/sdcard/bin/busybox ntpd -q -n -p time.google.com

## Start FTP & SSH
/system/sdcard/bin/dropbearmulti dropbear -R
/system/sdcard/bin/bftpd -d

## Start Webserver:
/system/sdcard/bin/boa -c /system/sdcard/config/

## Configure OSD
if [ -f /system/sdcard/controlscripts/configureOsd ]; then
    source /system/sdcard/controlscripts/configureOsd  2>/dev/null
fi

## Configure Motion
if [ -f /system/sdcard/controlscripts/configureMotion ]; then
    source /system/sdcard/controlscripts/configureMotion  2>/dev/null
fi


## Autostart
for i in /system/sdcard/config/autostart/*; do
  $i
done

#Start
#/system/sdcard/bin/busybox nohup /system/sdcard/bin/v4l2rtspserver-master &>/dev/null &


echo "Startup finished!"
