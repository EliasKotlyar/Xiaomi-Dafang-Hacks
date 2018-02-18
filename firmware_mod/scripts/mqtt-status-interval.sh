#!/bin/sh
source /system/sdcard/config/mqtt
export LD_LIBRARY_PATH='/thirdlib:/system/lib:/system/sdcard/lib'

if [ $STATUSINTERVAL -lt 30 ]; then STATUSINTERVAL=30; fi

while true
do
	/system/sdcard/bin/mosquitto_pub.bin  -h $HOST -u $USER -P $PASS -t ${TOPIC}status -m "`/system/sdcard/scripts/mqtt-status.sh`"
	sleep $STATUSINTERVAL 
done

