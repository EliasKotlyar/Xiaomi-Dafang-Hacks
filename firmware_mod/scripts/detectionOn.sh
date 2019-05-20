#!/bin/sh

# Source your custom motion configurations
. /system/sdcard/config/motion.conf
. /system/sdcard/scripts/common_functions.sh

# Turn on the amber led
if [ "$motion_trigger_led" = true ] ; then
	yellow_led on
fi

# Save a snapshot
if [[ "$save_snapshot" = true && "$opt" != 1 ]] ; then
	save_dir=/system/sdcard/motion/stills
	filename=$(date +%d-%m-%Y_%H.%M.%S).jpg
	if [ ! -d "$save_dir" ]; then
		mkdir -p $save_dir
	fi
	/system/sdcard/bin/getimage > $save_dir/$filename &
fi

#optimize image
if [ "$opt" -eq 1 ]; then o="-optimize"; else o=""; fi
if [ "$scl" -eq 1 ]; then s="-scale $sclv"; else s=""; fi
if [[ "$opt" -eq 1 || "$scl" -eq 1 ]]; then
/system/sdcard/bin/jpegtran ${s} ${o} -outfile $save_dir/$filename $save_dir/$filename
rm "$save_dir/$filename"
if [ "$cln" -eq 1 ]; then
/system/sdcard/bin/busybox find $save_dir/ -type f -mtime $clnd | xargs rm -f
fi
fi

# Publish a mqtt message
if [ "$publish_mqtt_message" = true ] ; then
	. /system/sdcard/config/mqtt.conf
	/system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion ${MOSQUITTOOPTS} ${MOSQUITTOPUBOPTS} -m "ON"
	if [ "$save_snapshot" = true ] ; then
		/system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/snapshot ${MOSQUITTOOPTS} ${MOSQUITTOPUBOPTS} -f $save_dir/$filename
	fi

fi

# Send emails ...
if [ "$sendemail" = true ] ; then
    /system/sdcard/scripts/sendPictureMail.sh&
fi
