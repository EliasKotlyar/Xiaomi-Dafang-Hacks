#!/bin/sh
# shellcheck shell=busybox

# shellcheck source=config/mqtt.conf.dist
. /system/sdcard/config/mqtt.conf
# shellcheck source=scripts/common_functions.sh
. /system/sdcard/scripts/common_functions.sh

killall mosquitto_sub 2> /dev/null
killall mosquitto_sub.bin 2> /dev/null

while true; do
  # shellcheck disable=2086
  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/init ${MOSQUITTOOPTS} -n
  case $? in
	0)
		break 2
		;;
	5)
		# Not authorized
		logger "MQTT: credentials are not valid"
		break 2
		;;
	14)
		# Connection error, retry
		logger "MQTT: cannot connect to $HOST at $PORT, retry in 60s"
		sleep 60
		;;
  esac
done

# shellcheck disable=2086
/system/sdcard/bin/mosquitto_sub.bin -v -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/# -t "${LOCATION}/set" ${MOSQUITTOOPTS} | while read -r line ; do
  case $line in
	"${LOCATION}/set announce")
	  /system/sdcard/scripts/mqtt-autodiscovery.sh
	  ;;
	"${TOPIC}/set help")
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/help ${MOSQUITTOOPTS} -m "possible commands: configured topic + Yellow_LED/set on/off, configured topic + Blue_LED/set on/off, configured topic + set with the following commands: status, $(grep \)$ /system/sdcard/www/cgi-bin/action.cgi | grep -v '[=*]' | sed -e "s/ //g" | grep -v -E '(osd|setldr|settz|showlog)' | sed -e "s/)//g")"
	;;

	"${TOPIC}/set status")
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/ ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(/system/sdcard/scripts/mqtt-status.sh)"
	;;

	"${TOPIC}/play "*)
	  AUDIOFILE=$(echo "$line" | awk '{print $2}')
	  VOLUME=$(echo "$line" | awk '{print $3}')
	  VOLUME=${VOLUME:-50}
	  /system/sdcard/bin/audioplay "/system/sdcard/media/$AUDIOFILE" "$VOLUME" $
	;;

	"${TOPIC}/leds/blue")
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/leds/blue ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(blue_led status)"
	;;

	"${TOPIC}/leds/blue/set ON")
	  blue_led on
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/leds/blue ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(blue_led status)"
	;;

	"${TOPIC}/leds/blue/set OFF")
	  blue_led off
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/leds/blue ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS}  -m "$(blue_led status)"
	;;

	"${TOPIC}/leds/yellow")
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/leds/yellow ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(yellow_led status)"
	;;

	"${TOPIC}/leds/yellow/set ON")
	  yellow_led on
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/leds/yellow ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(yellow_led status)"
	;;

	"${TOPIC}/leds/yellow/set OFF")
	  yellow_led off
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/leds/yellow ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(yellow_led status)"
	;;

	"${TOPIC}/leds/ir")
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/leds/ir ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(ir_led status)"
	;;

	"${TOPIC}/leds/ir/set ON")
	  ir_led on
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/leds/ir ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(ir_led status)"
	;;

	"${TOPIC}/leds/ir/set OFF")
	  ir_led off
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/leds/ir ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(ir_led status)"
	;;

	"${TOPIC}/ir_cut")
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/ir_cut ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(ir_cut status)"
	;;

	"${TOPIC}/ir_cut/set ON")
	  ir_cut on
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/ir_cut ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(ir_cut status)"
	;;

	"${TOPIC}/ir_cut/set OFF")
	  ir_cut off
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/ir_cut ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(ir_cut status)"
	;;

	"${TOPIC}/brightness")
	  if [ "$LIGHT_SENSOR" == 'hw' ]
	  then
                # shellcheck disable=2086
		/system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/brightness ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(ldr status)"
	  elif [ "$LIGHT_SENSOR" == 'virtual' ]
	  then
                # shellcheck disable=2086
		/system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/brightness ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(exposure status)"
	  fi
	;;

	"${TOPIC}/rtsp_server")
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/rtsp_server ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(rtsp_server status)"
	;;

	"${TOPIC}/rtsp_server/set ON")
	  rtsp_server on
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/rtsp_server ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(rtsp_server status)"
	;;

	"${TOPIC}/rtsp_server/set OFF")
	  rtsp_server off
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/rtsp_server ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(rtsp_server status)"
	;;

	"${TOPIC}/night_mode")
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/night_mode ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(night_mode status)"
	;;

	"${TOPIC}/night_mode/set ON")
	  night_mode on
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/night_mode ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(night_mode status)"
	;;

	"${TOPIC}/night_mode/set OFF")
	  night_mode off
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/night_mode ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(night_mode status)"
	;;

	"${TOPIC}/night_mode/auto")
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/night_mode/auto ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(auto_night_mode status)"
	;;

	"${TOPIC}/night_mode/auto/set ON")
	  auto_night_mode on
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/night_mode/auto ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(auto_night_mode status)"
	;;

	"${TOPIC}/night_mode/auto/set OFF")
	  auto_night_mode off
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/night_mode/auto ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(auto_night_mode status)"
	;;

	"${TOPIC}/motion/detection")
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/detection ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(motion_detection status)"
	;;

	"${TOPIC}/motion/detection/set ON")
	  motion_detection on
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/detection ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(motion_detection status)"
	;;

	"${TOPIC}/motion/detection/set OFF")
	  motion_detection off
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/detection ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(motion_detection status)"
	;;

	"${TOPIC}/motion/led")
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/led ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(motion_led status)"
	;;

	"${TOPIC}/motion/led/set ON")
	  motion_led on
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/led ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(motion_led status)"
	;;

	"${TOPIC}/motion/led/set OFF")
	  motion_led off
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/led ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(motion_led status)"
	;;

	"${TOPIC}/motion/snapshot")
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/snapshot ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(motion_snapshot status)"
	;;

	"${TOPIC}/motion/snapshot/set ON")
	  motion_snapshot on
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/snapshot ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(motion_snapshot status)"
	;;

	"${TOPIC}/motion/snapshot/set OFF")
	  motion_snapshot off
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/snapshot ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(motion_snapshot status)"
	;;

	"${TOPIC}/motion/video")
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/video ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(motion_video status)"
	;;

	"${TOPIC}/motion/video/set ON")
	  motion_video on
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/video ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(motion_video status)"
	;;

	"${TOPIC}/motion/video/set OFF")
	  motion_video off
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/video ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(motion_video status)"
	;;

	"${TOPIC}/motion/mqtt_publish")
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/mqtt_publish ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(motion_mqtt_publish status)"
	;;

	"${TOPIC}/motion/mqtt_publish/set ON")
	  motion_mqtt_publish on
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/mqtt_publish ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(motion_mqtt_publish status)"
	;;

	"${TOPIC}/motion/mqtt_publish/set OFF")
	  motion_mqtt_publish off
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/mqtt_publish ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(motion_mqtt_publish status)"
	;;


	"${TOPIC}/motion/mqtt_snapshot")
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/mqtt_snapshot ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(motion_mqtt_snapshot status)"
	;;

	"${TOPIC}/snapshot/image GET")
	  /system/sdcard/bin/getimage > "/tmp/mqtt_snapshot"
	  /system/sdcard/bin/jpegoptim -m 50 "/tmp/mqtt_snapshot"
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/snapshot/image ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -f "/tmp/mqtt_snapshot"
	  rm "/tmp/mqtt_snapshot"
	;;

	"${TOPIC}/motion/mqtt_snapshot/set ON")
	  motion_mqtt_snapshot on
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/mqtt_snapshot ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(motion_mqtt_snapshot status)"
	;;

	"${TOPIC}/motion/mqtt_snapshot/set OFF")
	  motion_mqtt_snapshot off
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/mqtt_snapshot ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(motion_mqtt_snapshot status)"
	;;

   "${TOPIC}/motion/send_mail")
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/send_mail ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(motion_send_mail status)"
	;;

	"${TOPIC}/motion/send_mail/set ON")
	  motion_send_mail on
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/send_mail ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(motion_send_mail status)"
	;;

	"${TOPIC}/motion/send_mail/set OFF")
	  motion_send_mail off
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/send_mail ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(motion_send_mail status)"
	;;

   "${TOPIC}/motion/send_telegram")
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/send_telegram ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(motion_send_telegram status)"
	;;

	"${TOPIC}/motion/send_telegram/set ON")
	  motion_send_telegram on
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/send_telegram ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(motion_send_telegram status)"
	;;

	"${TOPIC}/motion/send_telegram/set OFF")
	  motion_send_telegram off
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/send_telegram ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(motion_send_telegram status)"
	;;

	"${TOPIC}/motion/tracking")
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/tracking ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(motion_tracking status)"
	;;

	"${TOPIC}/motion/tracking/set ON")
	  motion_tracking on
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/tracking ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(motion_tracking status)"
	;;

	"${TOPIC}/motion/tracking/set OFF")
	  motion_tracking off
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/tracking ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(motion_tracking status)"
	;;

	"${TOPIC}/motors/vertical/set up")
	  motor up
	  MOTORSTATE=$(motor status vertical)
	  if [ "$(/system/sdcard/bin/setconf -g f)" -eq 1 ]; then
		TARGET=$(busybox expr "$MAX_Y" - "$MOTORSTATE")
	  else
		TARGET=$MOTORSTATE
	  fi
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motors/vertical ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$TARGET"
	;;

	"${TOPIC}/motors/vertical/set down")
	  motor down
	  MOTORSTATE=$(motor status vertical)
	  if [ "$(/system/sdcard/bin/setconf -g f)" -eq 1 ]; then
		TARGET=$(busybox expr "$MAX_Y" - "$MOTORSTATE")
	  else
		TARGET=$MOTORSTATE
	  fi
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motors/vertical ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$TARGET"
	;;

	"${TOPIC}/motors/vertical/set "*)
	  COMMAND=$(echo "$line" | awk '{print $2}')
	  MOTORSTATE=$(motor status vertical)
	  if [ -n "$COMMAND" ] && [ "$COMMAND" -eq "$COMMAND" ] 2>/dev/null; then
		if [ "$(/system/sdcard/bin/setconf -g f)" -eq 1 ]; then
		  echo "Changing motor from $COMMAND to $MOTORSTATE"
		  TARGET=$(busybox expr "$MOTORSTATE" + "$COMMAND" - "$MAX_Y")
		else
		  echo "Changing motor from $MOTORSTATE to $COMMAND"
		  TARGET=$(busybox expr "$COMMAND" - "$MOTORSTATE")
		fi
		echo "Moving $TARGET"
		if [ "$TARGET" -lt 0 ]; then
		  motor down "$(busybox expr "$TARGET" \* -1)"
		else
		  motor up "$TARGET"
		fi
	  else
		echo "Requested $COMMAND is not a number"
	  fi
	;;

	"${TOPIC}/motors/horizontal/set left")
	  motor left
	  MOTORSTATE=$(motor status horizontal)
	  if [ "$(/system/sdcard/bin/setconf -g f)" -eq 1 ]; then
		TARGET=$(busybox expr "$MAX_X" - "$MOTORSTATE")
	  else
		TARGET=$MOTORSTATE
	  fi
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motors/horizontal ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$TARGET"
	;;

	"${TOPIC}/motors/horizontal/set right")
	  motor right
	  MOTORSTATE=$(motor status horizontal)
	  if [ "$(/system/sdcard/bin/setconf -g f)" -eq 1 ]; then
		TARGET=$(busybox expr "$MAX_X" - "$MOTORSTATE")
	  else
		TARGET=$MOTORSTATE
	  fi
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motors/horizontal ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$TARGET"
	;;

	"${TOPIC}/motors/horizontal/set "*)
	  COMMAND=$(echo "$line" | awk '{print $2}')
	  MOTORSTATE=$(motor status horizontal)
	  if [ -n "$COMMAND" ] && [ "$COMMAND" -eq "$COMMAND" ] 2>/dev/null; then
		if [ "$(/system/sdcard/bin/setconf -g f)" -eq 1 ]; then
		  echo "Changing motor from $COMMAND to $MOTORSTATE"
		  TARGET=$(busybox expr "$MOTORSTATE" + "$COMMAND" - "$MAX_X")
		else
		  echo "Changing motor from $MOTORSTATE to $COMMAND"
		  TARGET=$(busybox expr "$COMMAND" - "$MOTORSTATE")
		fi
		echo "Moving $TARGET"
		if [ "$TARGET" -lt 0 ]; then
		  motor left "$(busybox expr "$TARGET" \* -1)"
		else
		  motor right "$TARGET"
		fi
	  else
		echo "Requested $COMMAND is not a number"
	  fi
	;;

	"${TOPIC}/motors/set calibrate")
	  motor reset_pos_count
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motors ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(motor status horizontal)"
	;;

	"${TOPIC}/remount_sdcard/set ON")
	  remount_sdcard
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/remount_sdcard ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "Remounting the SD Card"
	;;

	"${TOPIC}/reboot/set ON")
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/reboot ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "Rebooting the System"
	  reboot_system
	;;

	"${TOPIC}/recording")
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/recording ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(recording status)"
	;;

	"${TOPIC}/recording/set ON")
	  recording on
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/recording ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(recording status)"
	;;

	"${TOPIC}/recording/set OFF")
	  recording off
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/recording ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(recording status)"
	;;

	"${TOPIC}/timelapse")
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/timelapse ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(timelapse status)"
	;;

	"${TOPIC}/timelapse/set ON")
	  timelapse on
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/timelapse ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(timelapse status)"
	;;

	"${TOPIC}/timelapse/set OFF")
	  timelapse off
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/timelapse ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(timelapse status)"
	;;

	"${TOPIC}/snapshot/set ON")
	  snapshot
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/snapshot ${MOSQUITTOOPTS} ${MOSQUITTOPUBOPTS} -f "$filename"
	;;

	"${TOPIC}/update/set update")
	  if [ -f "/system/sdcard/VERSION" ]; then
	  	branch=$(/system/sdcard/bin/jq -r .branch /system/sdcard/VERSION)
	  else
	    branch="master"
	  fi
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/update ${MOSQUITTOOPTS} ${MOSQUITTOPUBOPTS} -m "Upgrade started"
	  result=$(/bin/sh /system/sdcard/autoupdate.sh -s -v -f -r $branch)
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/update ${MOSQUITTOOPTS} ${MOSQUITTOPUBOPTS} -m "Upgrade finish: ${result}"
	;;

	"${TOPIC}/hwvolume")
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/hwvolume ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(hwvolume status)"
	;;

	"${TOPIC}/hwvolume/set"*)
		VOLUME=$(echo "$line" | awk '{print $2}')
		hwvolume "$VOLUME"
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/hwvolume ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(hwvolume status)"
	;;

	"${TOPIC}/swvolume")
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/swvolume ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(swvolume status)"
	;;

	"${TOPIC}/swvolume/set"*)
		VOLUME=$(echo "$line" | awk '{print $2}')
		swvolume "$VOLUME"
          # shellcheck disable=2086
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/swvolume ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(swvolume status)"
	;;

	"${TOPIC}/set "*)
	  COMMAND=$(echo "$line" | awk '{print $2}')
	  #echo "$COMMAND"
	  F_cmd="${COMMAND}" /system/sdcard/www/cgi-bin/action.cgi -o /dev/null 2>/dev/null
	  if [ $? -eq 0 ]; then
                # shellcheck disable=2086
		/system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}/${COMMAND}" ${MOSQUITTOOPTS} -m "OK (this means: action.cgi invoke with parameter ${COMMAND}, nothing more, nothing less)"
	  else
                # shellcheck disable=2086
		/system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}/error" ${MOSQUITTOOPTS} -m "An error occurred when executing ${line}"
	  fi
	  # Publish updated states
	  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}" ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(/system/sdcard/scripts/mqtt-status.sh)"
	;;
  esac
done
