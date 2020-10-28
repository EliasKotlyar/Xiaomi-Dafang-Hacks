#!/bin/sh

# Source your custom motion configurations
. /system/sdcard/config/motion.conf
. /system/sdcard/scripts/common_functions.sh

# Turn off the amber LED
if [ "$motion_trigger_led" = true ] ; then
	yellow_led off
fi

# Publish a mqtt message
if [ "$publish_mqtt_message" = true ] ; then
	. /system/sdcard/config/mqtt.conf
	/system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion ${MOSQUITTOOPTS} ${MOSQUITTOPUBOPTS} -m "OFF"
fi

# Run any user scripts.
for i in /system/sdcard/config/userscripts/motiondetection/*; do
	if [ -x $i ]; then
		echo "Running: $i off"
		$i off
	fi
done
