#!/bin/sh

# Source your custom motion configurations
source /system/sdcard/config/motion.conf

# Define a gpio helper
setgpio(){
	GPIOPIN=$1
	echo "$2" > "/sys/class/gpio/gpio$GPIOPIN/value"
}

# Turn off the amber LED
if [ "$motion_trigger_led" = true ] ; then
	setgpio 38 1
fi

# Publish a mqtt message
if [ "$publish_mqtt_message" = true ] ; then
	source /system/sdcard/config/mqtt
	export LD_LIBRARY_PATH='/thirdlib:/system/lib:/system/sdcard/lib'
	/system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -u "$USER" -P "$PASS" -t "${TOPIC}"motion ${MOSQUITTOOPTS} ${MOSQUITTOPUBOPTS} -m "off"
fi
