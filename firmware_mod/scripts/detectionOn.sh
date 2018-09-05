#!/bin/sh

# Source your custom motion configurations
. /system/sdcard/config/motion.conf
. /system/sdcard/scripts/common_functions.sh

# Turn on the amber led
if [ "$motion_trigger_led" = true ] ; then
	yellow_led on
fi

# Save a snapshot
if [ "$save_snapshot" = true ] ; then
	filename=$(date +%d-%m-%Y_%H.%M.%S).jpg
	if [ ! -d "$save_dir" ]; then
		mkdir -p "$save_dir"
	fi
	{
		# Limit the number of snapshots
		if [ "$(ls "$save_dir" | wc -l)" -ge "$max_snapshots" ]; then
			rm -f "$save_dir/$(ls -ltr "$save_dir" | awk 'NR==2{print $9}')"
		fi
	} &
	/system/sdcard/bin/getimage > "$save_dir/$filename" &
fi

# Publish a mqtt message
if [ "$publish_mqtt_message" = true ] ; then
	. /system/sdcard/config/mqtt.conf
	/system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion ${MOSQUITTOOPTS} ${MOSQUITTOPUBOPTS} -m "ON"
	if [ "$save_snapshot" = true ] ; then
		/system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/snapshot ${MOSQUITTOOPTS} ${MOSQUITTOPUBOPTS} -f "$save_dir/$filename"
	fi

fi

# Send emails ...
if [ "$sendemail" = true ] ; then
    /system/sdcard/scripts/sendPictureMail.sh&
fi

# Send a telegram message
if [ "$send_telegram" = true ]; then
	if [ "$save_snapshot" = true ] ; then
		/system/sdcard/bin/telegram p "$save_dir/$filename"
	else
		/system/sdcard/bin/getimage > "/tmp/telegram_image.jpg"
 		/system/sdcard/bin/telegram p "/tmp/telegram_image.jpg"
 		rm "/tmp/telegram_image.jpg"
	fi
fi

# Run any user scripts.
for i in /system/sdcard/config/userscripts/motiondetection/*; do
    if [ -x "$i" ]; then
        echo "Running: $i on"
        $i on &
    fi
done
