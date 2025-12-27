#!/bin/sh
# shellcheck shell=busybox
# shellcheck source=config/mqtt.conf.dist
. /system/sdcard/config/mqtt.conf
# shellcheck source=scripts/common_functions.sh
. /system/sdcard/scripts/common_functions.sh

if [ "$STATUSINTERVAL" -lt 30 ]; then
  STATUSINTERVAL=30
fi

while true
do
  # shellcheck disable=2086
  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/leds/blue ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "$(blue_led status)"
  # shellcheck disable=2086
  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/leds/yellow ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "$(yellow_led status)"
  # shellcheck disable=2086
  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/leds/ir ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "$(ir_led status)"
  # shellcheck disable=2086
  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/ir_cut ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "$(ir_cut status)"

  if [ "$LIGHT_SENSOR" = 'hw' ]
  then
        # shellcheck disable=2086
	/system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/brightness ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "$(ldr status)"
  elif [ "$LIGHT_SENSOR" = 'virtual' ]
  then
        # shellcheck disable=2086
	/system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/brightness ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "$(exposure status)"
  fi

  # shellcheck disable=2086
  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/rtsp_server ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "$(rtsp_server status)"
  # shellcheck disable=2086
  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/night_mode ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "$(night_mode status)"
  # shellcheck disable=2086
  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/night_mode/auto ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "$(auto_night_mode status)"
  # shellcheck disable=2086
  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/detection ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "$(motion_detection status)"
  # shellcheck disable=2086
  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/led ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "$(motion_led status)"
  # shellcheck disable=2086
  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/snapshot ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "$(motion_snapshot status)"
  # shellcheck disable=2086
  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/video ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "$(motion_video status)"
  # shellcheck disable=2086
  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/mqtt_publish ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "$(motion_mqtt_publish status)"
  # shellcheck disable=2086
  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/mqtt_snapshot ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "$(motion_mqtt_snapshot status)"
  # shellcheck disable=2086
  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/send_mail ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "$(motion_send_mail status)"
  # shellcheck disable=2086
  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/send_telegram ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "$(motion_send_telegram status)"
  # shellcheck disable=2086
  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/tracking ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "$(motion_tracking status)"
  # shellcheck disable=2086
  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/recording ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "$(recording status)"
  # shellcheck disable=2086
  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/timelapse ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "$(timelapse status)"
  MOTORSTATE=$(motor status vertical)
  if [ "$(/system/sdcard/bin/setconf -g f)" -eq 1 ]; then
	TARGET=$(busybox expr "$MAX_Y" - "$MOTORSTATE")
  else
	TARGET=$MOTORSTATE
  fi
  # shellcheck disable=2086
  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motors/vertical ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m  "$TARGET"
  MOTORSTATE=$(motor status horizontal)
  if [ "$(/system/sdcard/bin/setconf -g f)" -eq 1 ]; then
	TARGET=$(busybox expr "$MAX_X" - "$MOTORSTATE")
  else
	TARGET=$MOTORSTATE
  fi
  # shellcheck disable=2086
  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motors/horizontal ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "$TARGET"
  # shellcheck disable=2086
  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}" ${MOSQUITTOOPTS} ${MOSQUITTOPUBOPTS} -r -m "$(/system/sdcard/scripts/mqtt-status.sh)"
  # shellcheck disable=2086
  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/hwvolume ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "$(hwvolume status)"
  # shellcheck disable=2086
  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/swvolume ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "$(swvolume status)"
  sleep "$STATUSINTERVAL"
done
