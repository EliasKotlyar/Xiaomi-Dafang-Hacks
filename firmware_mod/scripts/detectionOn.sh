#!/bin/sh

# Source your custom motion configurations
source /system/sdcard/config/motion.conf

# Define a gpio helper
setgpio(){
	GPIOPIN=$1
	echo "$2" > "/sys/class/gpio/gpio$GPIOPIN/value"
}

# Turn on the amber led
if [ "$motion_trigger_led" = true ] ; then
	setgpio 38 0
	setgpio 39 1
fi

# Save a snapshot
if [ "$save_snapshot" = true ] ; then
	save_dir=/system/sdcard/motion/stills
	filename=`date +%d-%m-%Y_%H.%M.%S`.jpg
	if [ ! -d "$save_dir" ]; then
		mkdir -p $save_dir
	fi
	/system/sdcard/bin/getimage > $save_dir/$filename &
fi

# Publish a mqtt message
if [ "$publish_mqtt_message" = true ] ; then
	source /system/sdcard/config/mqtt
	export LD_LIBRARY_PATH='/thirdlib:/system/lib:/system/sdcard/lib'
	/system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -u "$USER" -P "$PASS" -t "${TOPIC}"motion ${MOSQUITTOOPTS} ${MOSQUITTOPUBOPTS} -m "on"
fi
