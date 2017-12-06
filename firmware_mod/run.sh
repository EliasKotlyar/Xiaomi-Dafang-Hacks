#!/bin/sh
CONFIGPATH=/system/sdcard/config
echo "Starting up CFW"


## Start Wifi:
insmod /driver/8189es.ko
wpa_supplicant -B -i wlan0 -c $CONFIGPATH/wpa_supplicant.conf -P /var/run/wpa_supplicant.pid
udhcpc -i wlan0 -p /var/run/udhcpc.pid -b

## Start Audio:
insmod /driver/audio.ko

## Start GPIO:
setgpio () {
GPIOPIN=$1
echo $GPIOPIN > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio$GPIOPIN/direction
echo 0 > /sys/class/gpio/gpio$GPIOPIN/active_low
echo 1 > /sys/class/gpio/gpio$GPIOPIN/value
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

# Startup Motor:
insmod /system/sdcard/driver/sample_motor.ko



## Start Sensor:
insmod /system/sdcard/driver/tx-isp.ko isp_clk=100000000
insmod /system/sdcard/driver/sensor_jxf22.ko data_interface=2 pwdn_gpio=-1 reset_gpio=18 sensor_gpio_func=0

## Start FTP & SSH
/system/sdcard/bin/dropbearmulti dropbear -R
/system/sdcard/bin/bftpd -d

## Start Webserver:
/system/sdcard/bin/boa -c /system/sdcard/config/

echo "Startup finished!"

