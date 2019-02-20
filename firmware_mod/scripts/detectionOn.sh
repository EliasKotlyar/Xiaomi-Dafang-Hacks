#!/bin/sh

# Source your custom motion configurations
. /system/sdcard/config/motion.conf
. /system/sdcard/scripts/common_functions.sh

debug_msg () {
	if [ "$debug_msg_enable" = true ]; then
		echo "DEBUG: $*" 1>&2
	fi
}

record_video () {
	# We only want one video stream at a time. Try to grab an
	# exclusive flock on file descriptor 5. Bail out if another
	# process already has it. Touch the flock to update it's mod
	# time as a signal to the background process to keep recording
	# when motion is repeatedly observed.
	touch /run/recording_video.flock
	exec 5<> /run/recording_video.flock
	if /system/sdcard/bin/busybox flock -n -x 5; then
		# Got the lock
		debug_msg "Begin recording to $video_tempfile for $video_duration seconds"

		# Use avconv to stitch multiple JPEGs into 1fps video.
		# I couldn't get it working another way.
		# /dev/videoX inputs fail.
		# Localhost rtsp takes very long (10+ seconds) to start streaming and gets flaky when when memory or cpu are pegged.
		# This is a clungy method, but works well even at high res, fps, cpu, and memory load!
		( while [ "$(/system/sdcard/bin/busybox date "+%s")" -le "$(/system/sdcard/bin/busybox expr "$(/system/sdcard/bin/busybox stat -c "%X" /run/recording_video.flock)" + "$video_duration")" ]; do
				/system/sdcard/bin/getimage
				sleep 1
			done ) | /system/sdcard/bin/avconv -analyzeduration 0 -f image2pipe -r 1 -c:v mjpeg -c:a none -i - -c:v copy -c:a none -f mp4 -y "$video_tempfile"
		debug_msg "Finished recording"
	fi
}

# First, take a snapshot and record date ASAP
snapshot_tempfile=$(mktemp /tmp/snapshot-XXXXXXX)
video_tempfile=$(mktemp /tmp/video-XXXXXXX)

snapshot_pattern="${save_file_date_pattern:-+%d-%m-%Y_%H.%M.%S}"
snapshot_filename=$(date "$snapshot_pattern")
/system/sdcard/bin/getimage > "$snapshot_tempfile"
debug_msg "Got snapshot_tempfile=$snapshot_tempfile"

if [ "$save_video" = true  ] || [ "$telegram_alert_type" = "video" ] ; then
	record_video
fi

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

# Save the video
if [ "$save_video" = true ] ; then
	(
	debug_msg "Save video to $save_video_dir/${snapshot_filename}.mp4"

	if [ ! -d "$save_video_dir" ]; then
		mkdir -p "$save_video_dir"
	fi

	# Limit the number of videos
	if [ "$(ls "$save_video_dir" | wc -l)" -ge "$max_videos" ]; then
		rm -f "$save_video_dir/$(ls -ltr "$save_video_dir" | awk 'NR==2{print $9}')"
	fi

	cp "$video_tempfile" "$save_video_dir/${snapshot_filename}.mp4"
	) &
fi

# FTP snapshot and video stream
if [ "$ftp_snapshot" = true -o "$ftp_video" = true ]; then
	(
	ftpput_cmd="/system/sdcard/bin/busybox ftpput"
	ftpput_url="ftp://"
	if [ "$ftp_username" != "" ]; then
		ftpput_cmd="$ftpput_cmd -u $ftp_username"
		ftpput_url="${ftpput_url}${ftp_username}@"
	fi
	if [ "$ftp_password" != "" ]; then
		ftpput_cmd="$ftpput_cmd -p $ftp_password"
	fi
	if [ "$ftp_port" != "" ]; then
		ftpput_cmd="$ftpput_cmd -P $ftp_port"
	fi
	ftpput_cmd="$ftpput_cmd $ftp_host"
	ftpput_url="${ftpput_url}${ftp_host}"
	if [ "$ftp_port" != "" ]; then
		ftpput_url="${ftpput_url}:$ftp_port"
	fi

	if [ "$ftp_snapshot" = true ]; then
		debug_msg "Send FTP snapshot to $ftpput_url/$ftp_stills_dir/${snapshot_filename}.jpg"
		$ftpput_cmd "$ftp_stills_dir/${snapshot_filename}.jpg" "$snapshot_tempfile"
	fi

	if [ "$ftp_video" = true ]; then
		# We only want one video stream at a time. Try to grab an
		# exclusive flock on file descriptor 5. Bail out if another
		# process already has it. Touch the flock to update it's mod
		# time as a signal to the background process to keep recording
		# when motion is repeatedly observed.
		touch /run/ftp_motion_video_stream.flock
		exec 5<> /run/ftp_motion_video_stream.flock
		if /system/sdcard/bin/busybox flock -n -x 5; then
			# Got the lock
			debug_msg "Begin FTP video stream to $ftpput_url/$ftp_videos_dir/${snapshot_filename}.avi for $ftp_video_duration seconds"

			# XXX Uses avconv to stitch multiple JPEGs into 1fps video.
			#  I couldn't get it working another way. /dev/videoX inputs
			#  fail. Localhost rtsp takes very long (10+ seconds) to
			#  start streaming and gets flaky when when memory or cpu
			#  are pegged. This is a clugy method, but works well even
			# at high res, fps, cpu, and memory load!
			( while [ "$(/system/sdcard/bin/busybox date "+%s")" -le "$(/system/sdcard/bin/busybox expr "$(/system/sdcard/bin/busybox stat -c "%X" /run/ftp_motion_video_stream.flock)" + "$ftp_video_duration")" ]; do
					/system/sdcard/bin/getimage
					sleep 1
				done ) \
			| /system/sdcard/bin/avconv -analyzeduration 0 -f image2pipe -r 1 -c:v mjpeg -c:a none -i - -c:v copy -c:a none -f avi - 2>/dev/null \
			| $ftpput_cmd "$ftp_videos_dir/${snapshot_filename}.avi" - &
		else
			debug_msg "FTP video stream already running, continued another $ftp_video_duration seconds"
		fi

		# File descriptor 5 is inherited across fork to preserve lock,
		# so we can close it here.
		exec 5>&-
	fi
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
	elif [ "$telegram_alert_type" = "image" ] ; then
		debug_msg "Send telegram image"
		/system/sdcard/bin/telegram p "$snapshot_tempfile"
	elif [ "$telegram_alert_type" = "video" ] ; then
		debug_msg "Send telegram video"
		/system/sdcard/bin/telegram v "$video_tempfile"
	fi
	) &
fi

# Send a matrix message
if [ "$send_matrix" = true ]; then
	(
	include /system/sdcard/config/matrix.conf
	debug_msg "Send matrix message"
	/system/sdcard/bin/matrix m "Motion detected"
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

debug_msg "Cleanup tempfiles"
rm "$snapshot_tempfile"
rm "$video_tempfile"

debug_msg "DONE"
