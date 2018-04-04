#!/bin/sh
source /system/sdcard/config/mqtt.conf

if [ "$STATUSINTERVAL" -lt 30 ]; then
  STATUSINTERVAL=30
fi

while true
do
  /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -u "$USER" -P "$PASS" -t "${TOPIC}" ${MOSQUITTOOPTS} ${MOSQUITTOPUBOPTS} -m "$(/system/sdcard/scripts/mqtt-status.sh)"
  sleep $STATUSINTERVAL
done
