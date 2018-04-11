#!/bin/sh

# Source your custom motion configurations
source /system/sdcard/config/motion.conf
source /system/sdcard/scripts/common_functions.sh

# Turn off the amber LED
if [ "$motion_trigger_led" = true ] ; then
	yellow_led off
fi

# Publish a mqtt message
if [ "$publish_mqtt_message" = true ] ; then
	source /system/sdcard/config/mqtt.conf
	/system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion ${MOSQUITTOOPTS} ${MOSQUITTOPUBOPTS} -m "OFF"
fi
