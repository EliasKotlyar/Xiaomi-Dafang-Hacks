#!/bin/sh

# Source your custom motion configurations
. /system/sdcard/config/motion.conf
. /system/sdcard/scripts/common_functions.sh

function debug_msg () {
	if [ "$debug_msg_enable" == true ]; then
		echo "DEBUG: $*" 1>&2
	fi
}

# First, take a snapshot and record date ASAP
snapshot_tempfile=$(mktemp /tmp/snapshot-XXXXXXX)
snapshot_pattern="${save_file_date_pattern:-+%d-%m-%Y_%H.%M.%S}"
snapshot_filename=$(date "$snapshot_pattern")
/system/sdcard/bin/getimage > "$snapshot_tempfile"
debug_msg "Got snapshot_tempfile=$snapshot_tempfile"

# Turn on the amber led
if [ "$motion_trigger_led" = true ] ; then
	debug_msg "Trigger LED"
	yellow_led on
fi

# Next, start background tasks for all configured notifications

# Save a snapshot
if [ "$save_snapshot" = true ] ; then
	(
	debug_msg "Save snapshot to $save_dir/${snapshot_filename}.jpg"

	if [ ! -d "$save_dir" ]; then
		mkdir -p "$save_dir"
	fi

	# Limit the number of snapshots
	if [ "$(ls "$save_dir" | wc -l)" -ge "$max_snapshots" ]; then
		rm -f "$save_dir/$(ls -ltr "$save_dir" | awk 'NR==2{print $9}')"
	fi

	cp "$snapshot_tempfile" "$save_dir/${snapshot_filename}.jpg"
	) &
fi

# Publish a mqtt message
if [ "$publish_mqtt_message" = true -o "$publish_mqtt_snapshot" = true ] ; then
	(
	. /system/sdcard/config/mqtt.conf

	if [ "$publish_mqtt_message" = true ] ; then
		debug_msg "Send MQTT message"
		/system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion ${MOSQUITTOOPTS} ${MOSQUITTOPUBOPTS} -m "ON"
	fi

	if [ "$publish_mqtt_snapshot" = true ] ; then
		debug_msg "Send MQTT snapshot"
		/system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/snapshot ${MOSQUITTOOPTS} ${MOSQUITTOPUBOPTS} -f "$snapshot_tempfile"
	fi
	) &
fi

# Send emails
if [ "$send_email" = true ] ; then
	debug_msg "Send emails"
	/system/sdcard/scripts/sendPictureMail.sh &
fi

# Send a telegram message
if [ "$send_telegram" = true ]; then
	(
	include /system/sdcard/config/telegram.conf

	if [ "$telegram_alert_type" = "text" ] ; then
		debug_msg "Send telegram text"
		/system/sdcard/bin/telegram m "Motion detected"
	else
		debug_msg "Send telegram snapshot"
		/system/sdcard/bin/telegram p "$snapshot_tempfile"
	fi
	) &
fi

# Run any user scripts.
for i in /system/sdcard/config/userscripts/motiondetection/*; do
    if [ -x "$i" ]; then
        debug_msg "Running: $i on $snapshot_tempfile"
        $i on "$snapshot_tempfile" &
    fi
done

# Wait for all background jobs to finish before existing and deleting tempfile
debug_msg "Waiting for background jobs to end:"
for jobpid in $(jobs -p); do
	wait "$jobpid"
	debug_msg " Job $jobpid ended"
done

debug_msg "Cleanup snapshot_tempfile"
rm "$snapshot_tempfile"

debug_msg "DONE"
