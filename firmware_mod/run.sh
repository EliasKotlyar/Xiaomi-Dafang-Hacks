#!/bin/sh
CONFIGPATH=/system/sdcard/config
SAMPLE_CONFIGPATH=/system/sdcard/sample_config

echo "Starting up CFW"
## Copy Configs:
if [  ! -f $CONFIGPATH/wpa_supplicant.conf ]; then
	cp $SAMPLE_CONFIGPATH/wpa_supplicant.conf $CONFIGPATH/wpa_supplicant.conf
fi
if [  ! -f $CONFIGPATH/bftpd.conf ]; then
	cp $SAMPLE_CONFIGPATH/bftpd.conf $CONFIGPATH/bftpd.conf
fi
if [  ! -f $CONFIGPATH/boa.conf ]; then
	cp $SAMPLE_CONFIGPATH/boa.conf $CONFIGPATH/boa.conf
fi

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

