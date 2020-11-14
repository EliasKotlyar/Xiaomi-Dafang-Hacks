#!/bin/sh
. /system/sdcard/config/mqtt.conf
. /system/sdcard/scripts/common_functions.sh

if [ "$STATUSINTERVAL" -lt 30 ]; then
  STATUSINTERVAL=30
fi

while true
do
  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/leds/blue ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "$(blue_led status)"
  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/leds/yellow ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "$(yellow_led status)"
  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/leds/ir ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "$(ir_led status)"
  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/ir_cut ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "$(ir_cut status)"

  if [ $LIGHT_SENSOR == 'hw' ]
  then
	/system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/brightness ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "$(ldr status)"
  elif [ $LIGHT_SENSOR == 'virtual' ]
  then
	/system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/brightness ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "$(exposure status)"
  fi

  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/rtsp_server ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "$(rtsp_server status)"
  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/night_mode ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "$(night_mode status)"
  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/night_mode/auto ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "$(auto_night_mode status)"
  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/detection ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "$(motion_detection status)"
  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/led ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "$(motion_led status)"
  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/snapshot ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "$(motion_snapshot status)"
  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/video ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "$(motion_video status)"
  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/mqtt_publish ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "$(motion_mqtt_publish status)"
  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/mqtt_snapshot ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "$(motion_mqtt_snapshot status)"
  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/send_mail ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "$(motion_send_mail status)"
  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/send_telegram ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "$(motion_send_telegram status)"
  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/tracking ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "$(motion_tracking status)"
  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/recording ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "$(recording status)"
  MOTORSTATE=$(motor status vertical)
  if [ `/system/sdcard/bin/setconf -g f` -eq 1 ]; then
	TARGET=$(busybox expr $MAX_Y - $MOTORSTATE)
  else
	TARGET=$MOTORSTATE
  fi  
  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motors/vertical ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m  "$TARGET"
  MOTORSTATE=$(motor status horizontal)
  if [ `/system/sdcard/bin/setconf -g f` -eq 1 ]; then
	TARGET=$(busybox expr $MAX_X - $MOTORSTATE)
  else
	TARGET=$MOTORSTATE
  fi
  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motors/horizontal ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "$TARGET"
  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}" ${MOSQUITTOOPTS} ${MOSQUITTOPUBOPTS} -r -m "$(/system/sdcard/scripts/mqtt-status.sh)"
  sleep $STATUSINTERVAL
done
