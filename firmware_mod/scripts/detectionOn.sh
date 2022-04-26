#!/bin/sh
# Source your custom motion configurations
. /system/sdcard/config/motion.conf
. /system/sdcard/scripts/common_functions.sh
. /system/sdcard/config/rtspserver.conf

debug_msg () {
	if [ "$debug_msg_enable" = true ]; then
		echo "DEBUG: $*" 1>&2
	fi
}

send_snapshot() {

	# Publish a mqtt message
	if [ "$publish_mqtt_message" = true -o "$publish_mqtt_snapshot" = true ] ; then
		(
		. /system/sdcard/config/mqtt.conf

		if [ "$publish_mqtt_message" = true ] ; then
			debug_msg "Send MQTT message"
			/system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "$TOPIC"/motion $MOSQUITTOOPTS $MOSQUITTOPUBOPTS -m "ON"
		fi

		if [ "$publish_mqtt_snapshot" = true ] ; then
			debug_msg "Send MQTT snapshot"
			/system/sdcard/bin/jpegtran -scale 1/2 "$snapshot_tempfile" > "$snapshot_tempfile-s"
			/system/sdcard/bin/jpegoptim -m 70 "$snapshot_tempfile-s"
			/system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "$TOPIC"/motion/snapshot/image $MOSQUITTOOPTS $MOSQUITTOPUBOPTS -f "$snapshot_tempfile-s"
			rm "$snapshot_tempfile-s"
		fi
		) &
	fi

	# Send a telegram message
	if [ "$send_telegram" = true ]; then
		(
		include /system/sdcard/config/telegram.conf

		if [ "$telegram_alert_type" = "text" ] ; then
			debug_msg "Send telegram text"
			/system/sdcard/bin/telegram m "Motion detected"
		elif [ "$telegram_alert_type" = "image" -o "$telegram_alert_type" = "video+image" ] ; then
			debug_msg "Send telegram image"
			/system/sdcard/bin/telegram p "$snapshot_tempfile"
		fi
		) &
	fi

	# Send a matrix message or image
	if [ "$send_matrix" = true ]; then
		(
		include /system/sdcard/config/matrix.conf

		if [ "$matrix_alert_type" = "text" ] ; then
			debug_msg "Send matrix text"
			/system/sdcard/bin/matrix m "Motion detected"
		elif [ "$matrix_alert_type" = "image" -o "$matrix_alert_type" = "video+image" ] ; then
			debug_msg "Send matrix image"
			/system/sdcard/bin/matrix p "$filename" "$snapshot_tempfile"
		fi
		) &
	fi

	# Save FTP snapshot
	if [ "$ftp_snapshot" = true ]; then
		(
		ftpput_cmd="/system/sdcard/bin/busybox ftpput"
		if [ "$ftp_username" != "" ]; then
			ftpput_cmd="$ftpput_cmd -u $ftp_username"
		fi
		if [ "$ftp_password" != "" ]; then
			ftpput_cmd="$ftpput_cmd -p $ftp_password"
		fi
		if [ "$ftp_port" != "" ]; then
			ftpput_cmd="$ftpput_cmd -P $ftp_port"
		fi
		ftpput_cmd="$ftpput_cmd $ftp_host"

		debug_msg "Sending FTP snapshot to ftp://$ftp_host/$ftp_stills_dir/$filename.jpg"
		$ftpput_cmd "$ftp_stills_dir/$filename.jpg" "$snapshot_tempfile"

		) &
	fi

	# Save Dropbox snapshot
	if [ "$dropbox_snapshot" = true ]; then
		(
		debug_msg "Sending Dropbox snapshot to $dropbox_stills_dir/$filename.jpg"
		/system/sdcard/bin/curl -X POST "$dropbox_url" \
			--header "Authorization: Bearer $dropbox_token" \
			--header "Dropbox-API-Arg: {\"path\": \"$dropbox_stills_dir/$filename.jpg\"}" \
			--header "Content-Type: application/octet-stream" \
			--data-binary @"$snapshot_tempfile"
		) &
	fi

	# Save a snapshot
	if [ "$save_snapshot" = true ] ; then
		(
		debug_msg "Save snapshot to $save_snapshot_dir/$groupname/$filename.jpg"

		if [ ! -d "$save_snapshot_dir/$groupname" ]; then
			mkdir -p "$save_snapshot_dir/$groupname"
			chmod "$save_dirs_attr" "$save_snapshot_dir/$groupname"
		fi

		# Limit the number of snapshots
		if [ "$(ls "$save_snapshot_dir" | wc -l)" -ge "$max_snapshot_days" ]; then
			rm -rf "$save_snapshot_dir/$(ls -ltr "$save_snapshot_dir" | awk 'NR==2{print $9}')"
		fi

		chmod "$save_files_attr" "$snapshot_tempfile"
		cp "$snapshot_tempfile" "$save_snapshot_dir/$groupname/$filename.jpg"
		) &
	fi

	# Save SMB snapshot
	if [ "$smb_snapshot" = true ]; then
		(
		smbclient_cmd="/system/bin/smbclient $smb_share"
		if [ "$smb_password" != "" ]; then
			smbclient_cmd="$smbclient_cmd $smb_password"
		else
			smbclient_cmd="$smbclient_cmd -N"
		fi
		if [ "$smb_username" != "" ]; then
			smbclient_cmd="$smbclient_cmd -U $smb_username"
		fi

		debug_msg "Saving SMB snapshot to $smb_share/$smb_stills_path"
		snapshot_tempfilename=${snapshot_tempfile:5}
		$smbclient_cmd -D "$smb_stills_path" -c "lcd /tmp; mkdir $groupname; cd $groupname; put $snapshot_tempfilename; rename $snapshot_tempfilename $filename.jpg"
		) &
	fi

	# Wait for all background jobs to finish before existing
	debug_msg "Waiting for background jobs to end in send_snapshot function:"
	for jobpid in $(jobs -p); do
		wait "$jobpid"
		debug_msg "Job in send_snapshot function $jobpid ended"
	done

}

record_video () {
	# We only want one video stream at a time. Try to grab an exclusive
	# flock on file descriptor 5. Bail out if another process already has
	# it. Touch the flock to update its mod time as a signal to the
	# background process to keep recording when motion is repeatedly
	# observed.
	touch /run/recording_video.flock
	exec 5<> /run/recording_video.flock
	if /system/sdcard/bin/busybox flock -n -x 5; then
		# Got the lock
		debug_msg "Begin recording to $video_tempfile for $video_duration seconds"

		if [ "$video_use_rtsp" = true ]; then
			output_buffer_size="$((($BITRATE*100)+150000))"
			if [ -z "$USERNAME" ]; then
				/system/sdcard/bin/openRTSP -4 -w "$video_rtsp_w" -h "$video_rtsp_h" -f "$video_rtsp_f" -d "$video_duration" -b "$output_buffer_size" rtsp://127.0.0.1:$PORT/unicast > "$video_tempfile"
			else
				/system/sdcard/bin/openRTSP -4 -w "$video_rtsp_w" -h "$video_rtsp_h" -f "$video_rtsp_f" -d "$video_duration" -b "$output_buffer_size" rtsp://$USERNAME:$USERPASSWORD@127.0.0.1:$PORT/unicast > "$video_tempfile"
			fi
		else
			# Use avconv to stitch multiple JPEGs into 1fps video.
			# I couldn't get it working another way.
			# /dev/videoX inputs fail.
			# Localhost rtsp takes very long (10+ seconds) to start streaming and gets flaky when when memory or cpu are pegged.
			# This is a clungy method, but works well even at high res, fps, cpu, and memory load!
			( while [ "$(/system/sdcard/bin/busybox date "+%s")" -le "$(/system/sdcard/bin/busybox expr "$(/system/sdcard/bin/busybox stat -c "%X" /run/recording_video.flock)" + "$video_duration")" ]; do
					/system/sdcard/bin/getimage
					sleep 1
				done ) | /system/sdcard/bin/avconv -analyzeduration 0 -f image2pipe -r 1 -c:v mjpeg -c:a none -i - -c:v copy -c:a none -f mp4 -y "$video_tempfile"
		fi

		debug_msg "Finished recording"
	fi
}

if [ -f /tmp/last-night ]; then
        if [ -n "$night_mode_event_delay" ]; then
                if [ "$night_mode_event_delay" -gt 0 ]; then
                        now_ts="$(date +%s)"
                        night_ts="$(/system/sdcard/bin/busybox stat -c %Y /tmp/last-night)"
                        dt="$(($now_ts-$night_ts))"
                        if [ "$dt" -lt "$night_mode_event_delay" ]; then
                                exit 0
                        fi
                fi
        fi
fi

# Turn on the amber led
if [ "$motion_trigger_led" = true ] ; then
	debug_msg "Trigger LED"
	yellow_led on
fi

# Prepare temp files
snapshot_tempfile=$(mktemp /tmp/snapshot-XXXXXXX)
video_tempfile=$(mktemp /tmp/video-XXXXXXX)

# Prepare filename, save datetime ASAP
group_pattern="${group_date_pattern:-+%Y-%m-%d}"
groupname=$(date "$group_pattern")
filename_pattern="${file_date_pattern:-+%Y-%m-%d_%H-%M-%S}"
filename=$(date "$filename_pattern")

# First, take a snapshot (always)
/system/sdcard/bin/getimage > "$snapshot_tempfile"
debug_msg "Got snapshot_tempfile=$snapshot_tempfile"

# Next send picture alerts in the background

send_snapshot &

# Then, record video (if necessary)
if [ "$save_video" = true ] ||
   [ "$smb_video" = true ] ||
   [ "$dropbox_video" = true ] ||
  ([ "$send_telegram" = true ] && ([ "$telegram_alert_type" = video+image ] || [ "$telegram_alert_type" = video ])) ||
  ([ "$send_matrix" = true ] && ([ "$matrix_alert_type" = video+image ] || [ "$matrix_alert_type" = video ])) ||
   [ "$publish_mqtt_video" = true ]
then
	record_video
fi

# Next, start background tasks for all configured video notifications

# Save the video
if [ "$save_video" = true ] ; then
	(
	debug_msg "Save video to $save_video_dir/$groupname/$filename.mp4"

	if [ ! -d "$save_video_dir/$groupname" ]; then
		mkdir -p "$save_video_dir/$groupname"
		chmod "$save_dirs_attr" "$save_video_dir/$groupname"
	fi

	# Limit the number of videos
	if [ "$(ls "$save_video_dir" | wc -l)" -ge "$max_video_days" ]; then
		rm -rf "$save_video_dir/$(ls -ltr "$save_video_dir" | awk 'NR==2{print $9}')"
	fi

	chmod "$save_files_attr" "$video_tempfile"
	cp "$video_tempfile" "$save_video_dir/$groupname/$filename.mp4"
	) &
fi

# FTP video stream
if [ "$ftp_video" = true ]; then
	(
	ftpput_cmd="/system/sdcard/bin/busybox ftpput"
	if [ "$ftp_username" != "" ]; then
		ftpput_cmd="$ftpput_cmd -u $ftp_username"
	fi
	if [ "$ftp_password" != "" ]; then
		ftpput_cmd="$ftpput_cmd -p $ftp_password"
	fi
	if [ "$ftp_port" != "" ]; then
		ftpput_cmd="$ftpput_cmd -P $ftp_port"
	fi
	ftpput_cmd="$ftpput_cmd $ftp_host"

	# We only want one video stream at a time. Try to grab an exclusive
	# flock on file descriptor 5. Bail out if another process already has
	# it. Touch the flock to update it's mod time as a signal to the
	# background process to keep recording when motion is repeatedly
	# observed.
	touch /run/ftp_motion_video_stream.flock
	exec 5<> /run/ftp_motion_video_stream.flock
	if /system/sdcard/bin/busybox flock -n -x 5; then
		# Got the lock
		debug_msg "Begin FTP video stream to ftp://$ftp_host/$ftp_videos_dir/$filename.avi for $video_duration seconds"

		# XXX Uses avconv to stitch multiple JPEGs into 1fps video.
		#  I couldn't get it working another way. /dev/videoX inputs
		#  fail. Localhost rtsp takes very long (10+ seconds) to start
		#  streaming and gets flaky when when memory or cpu are pegged.
		#  This is a clugy method, but works well even at high res,
		#  fps, cpu, and memory load!
		( while [ "$(/system/sdcard/bin/busybox date "+%s")" -le "$(/system/sdcard/bin/busybox expr "$(/system/sdcard/bin/busybox stat -c "%X" /run/ftp_motion_video_stream.flock)" + "$video_duration")" ]; do
				/system/sdcard/bin/getimage
				sleep 1
			done ) \
		| /system/sdcard/bin/avconv -analyzeduration 0 -f image2pipe -r 1 -c:v mjpeg -c:a none -i - -c:v copy -c:a none -f avi - 2>/dev/null \
		| $ftpput_cmd "$ftp_videos_dir/$filename.avi" - &
	else
		debug_msg "FTP video stream already running, continued another $video_duration seconds"
	fi

	# File descriptor 5 is inherited across fork to preserve lock,
	# so we can close it here.
	exec 5>&-
	) &
fi

# Save Dropbox video
if [ "$dropbox_video" = true ]; then
	(
	debug_msg "Saving Dropbox snapshot to $dropbox_videos_dir/$filename.mp4"
	/system/sdcard/bin/curl -X POST "$dropbox_url" \
		--header "Authorization: Bearer $dropbox_token" \
		--header "Dropbox-API-Arg: {\"path\": \"$dropbox_videos_dir/$filename.mp4\"}" \
		--header "Content-Type: application/octet-stream" \
		--data-binary @"$video_tempfile"
	) &
fi

# SMB snapshot and video
if [ "$smb_video" = true ]; then
	(
	smbclient_cmd="/system/bin/smbclient $smb_share"
	if [ "$smb_password" != "" ]; then
		smbclient_cmd="$smbclient_cmd $smb_password"
	else
		smbclient_cmd="$smbclient_cmd -N"
	fi
	if [ "$smb_username" != "" ]; then
		smbclient_cmd="$smbclient_cmd -U $smb_username"
	fi

	debug_msg "Saving SMB video to $smb_share/$smb_videos_path"
	video_tempfilename=${video_tempfile:5}
	$smbclient_cmd -D "$smb_videos_path" -c "lcd /tmp; mkdir $groupname; cd $groupname; put $video_tempfilename; rename $video_tempfilename $filename.mp4"
	) &
fi

# Publish a mqtt message
if [ "$publish_mqtt_video" = true ] ; then
	(
	. /system/sdcard/config/mqtt.conf

	debug_msg "Send MQTT video"
	/system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "$TOPIC"/motion/video $MOSQUITTOOPTS $MOSQUITTOPUBOPTS -f "$video_tempfile"

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

	if [ "$telegram_alert_type" = "video" -o "$telegram_alert_type" = "video+image" ] ; then
		if [ "$video_use_rtsp" = true ]; then
			if [ "$AUDIOFORMAT" = "PCMU" ] || [ "$AUDIOFORMAT" = "OFF" ] ; then
				# Convert file to mp4 and remove audio stream so video plays in telegram app
				debug_msg "Send telegram video"
				/system/sdcard/bin/avconv -i "$video_tempfile" -c:v copy -an "$video_tempfile"-telegram.mp4
				/system/sdcard/bin/telegram v "$video_tempfile"-telegram.mp4
				rm "$video_tempfile"-telegram.mp4
			else
				# avconv can't strip audio it doesn't understand
				debug_msg "Send telegram video (only viable for external playback)"
				/system/sdcard/bin/telegram v "$video_tempfile"
			fi
		else
			/system/sdcard/bin/avconv -i "$video_tempfile" "$video_tempfile-lo.mp4"
			/system/sdcard/bin/telegram v "$video_tempfile-lo.mp4"
			rm "$video_tempfile-lo.mp4"
		fi
	fi
	) &
fi

# Send a matrix video
if [ "$send_matrix" = true ]; then
	(
	include /system/sdcard/config/matrix.conf

	if [ "$matrix_alert_type" = "video" -o "$matrix_alert_type" = "video+image" ] ; then
		debug_msg "Send matrix video"
		if [ "$video_use_rtsp" = true ]; then
			/system/sdcard/bin/matrix v "$filename" "$video_tempfile"
		else
			/system/sdcard/bin/avconv -i "$video_tempfile" "$video_tempfile-lo.mp4"
			/system/sdcard/bin/matrix v "$filename" "$video_tempfile-lo.mp4"
			rm -f "$video_tempfile-lo.mp4"
		fi
	fi
	) &
fi

# Run any user scripts.
for i in /system/sdcard/config/userscripts/motiondetection/*; do
	if [ -x "$i" ]; then
		debug_msg "Running: $i on $snapshot_tempfile"
		$i on "$snapshot_tempfile" "$video_tempfile" &
	fi
done

# Wait for all background jobs to finish before exiting and deleting tempfile
debug_msg "Waiting for background jobs to end:"
for jobpid in $(jobs -p); do
	wait "$jobpid"
	debug_msg " Job $jobpid ended"
done

debug_msg "Cleanup tempfiles"
rm "$snapshot_tempfile"
rm "$video_tempfile"

debug_msg "DONE"
