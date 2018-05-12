#!/bin/sh

CONFIGPATH="/system/sdcard/config"
LOGDIR="/system/sdcard/log"
LOGPATH="$LOGDIR/startup.log"
if [ ! -d $LOGDIR ]; then
  mkdir -p $LOGDIR
fi
echo "==================================================" >> $LOGPATH
echo "Starting the Dafang Hacks Custom Application Layer" >> $LOGPATH
echo "==================================================" >> $LOGPATH

## Stop telnet for security reasons
killall telnetd

## Load some common functions
. /system/sdcard/scripts/common_functions.sh
echo "loaded common functions" >> $LOGPATH

## Create root user home directory and etc directory on sdcard
if [ ! -d /system/sdcard/root ]; then
  mkdir /system/sdcard/root
  echo 'PATH=/system/sdcard/bin:$PATH' > /system/sdcard/root/.profile
  echo "Created root user home directory" >> $LOGPATH
fi
if [ ! -d /system/sdcard/etc ]; then
  mkdir /system/sdcard/etc
  cp -fRL /etc/TZ /etc/protocols /etc/fstab /etc/inittab /etc/hosts \
    /etc/passwd /etc/shadow /etc/group /etc/resolv.conf /etc/hostname \
    /etc/profile /etc/os-release /etc/sensor /system/sdcard/etc
  sed -i s#/:#/root:# /system/sdcard/etc/passwd
  echo "Created etc directory on sdcard" >> $LOGPATH
fi
mount -o bind /system/sdcard/root /root
echo "Bind mounted /system/sdcard/root to /root" >> $LOGPATH
mount -o bind /system/sdcard/etc /etc
echo "Bind mounted /system/sdcard/etc to /etc" >> $LOGPATH

## Start Wifi:
if [ ! -f $CONFIGPATH/wpa_supplicant.conf ]; then
  echo "Warning: You have to configure wpa_supplicant in order to use wifi. Please see /system/sdcard/config/wpa_supplicant.conf.dist for further instructions."
fi
MAC=$(grep MAC < /params/config/.product_config | cut -c16-27 | sed 's/\(..\)/\1:/g;s/:$//')
if [ -f /driver/8189es.ko ]; then
  insmod /driver/8189es.ko rtw_initmac="$MAC"
else
  insmod /driver/rtl8189ftv.ko rtw_initmac="$MAC"
fi
wpa_supplicant_status="$(wpa_supplicant -B -i wlan0 -c $CONFIGPATH/wpa_supplicant.conf -P /var/run/wpa_supplicant.pid)"
echo "wpa_supplicant: $wpa_supplicant_status" >> $LOGPATH

hostname -F $CONFIGPATH/hostname.conf
udhcpc_status=$(udhcpc -i wlan0 -p /var/run/udhcpc.pid -b -x hostname:"$(hostname)")
echo "udhcpc: $udhcpc_status" >> $LOGPATH

## Sync the via NTP
if [ ! -f $CONFIGPATH/ntp_srv.conf ]; then
  cp $CONFIGPATH/ntp_srv.conf.dist $CONFIGPATH/ntp_srv.conf
fi
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

echo "initialized gpios" >> $LOGPATH

## Set leds to default startup states
ir_led off
ir_cut on
yellow_led off
blue_led on

## Load motor driver module
insmod /system/sdcard/driver/sample_motor.ko
# Don't calibrate the motors for now as for newer models the endstops don't work:
# motor hcalibrate
# motor vcalibrate

## Start Sensor:
insmod /system/sdcard/driver/tx-isp.ko isp_clk=100000000
insmod /system/sdcard/driver/sensor_jxf22.ko data_interface=2 pwdn_gpio=-1 reset_gpio=18 sensor_gpio_func=0

## Start FTP & SSH Server:
dropbear_status=$(/system/sdcard/bin/dropbearmulti dropbear -R)
echo "dropbear: $dropbear_status" >> $LOGPATH

bftpd_status=$(/system/sdcard/bin/bftpd -d)
echo "bftpd: $bftpd_status" >> $LOGPATH

## Start Webserver:
lighttpd_status=$(/system/sdcard/bin/lighttpd -f /system/sdcard/config/lighttpd.conf)
echo "lighttpd: $lighttpd_status" >> $LOGPATH

## Configure OSD:
if [ -f /system/sdcard/controlscripts/configureOsd ]; then
    . /system/sdcard/controlscripts/configureOsd  2>/dev/null
fi

## Configure Motion:
if [ -f /system/sdcard/controlscripts/configureMotion ]; then
    . /system/sdcard/controlscripts/configureMotion  2>/dev/null
fi


## Autostart all enabled services:
for i in /system/sdcard/config/autostart/*; do
  $i
done

echo "Startup finished!" >> $LOGPATH
