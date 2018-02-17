#!/bin/sh
source /system/sdcard/config/mqtt
/bin/mknod $FIFO p 2>/dev/null
# next two lines are a little bit cruel
killall mosquitto_sub 2> /dev/null
killall mosquitto_sub.bin 2> /dev/null

export LD_LIBRARY_PATH='/thirdlib:/system/lib:/system/sdcard/lib'

/system/sdcard/bin/mosquitto_sub.bin -h $HOST -u $USER -P $PASS -t ${TOPIC}set ${MOSQUITTOOPTS} ${MOSQUITTOSUBOPTS} > $FIFO 2> /dev/null &


while read line < $FIFO
do
case $line in

help)
/system/sdcard/bin/mosquitto_pub.bin  -h $HOST -u $USER -P $PASS -t ${TOPIC}help -m "possible commands: status_text status_json `grep \)$ /system/sdcard/www/cgi-bin/action.cgi | grep -v \= | grep -v \* | sed -e "s/ //g" | grep -v osd | grep -v setldr | grep -v settz | grep -v showlog | sed -e "s/)//g"`"
;;

status_text)
/system/sdcard/bin/mosquitto_pub.bin  -h $HOST -u $USER -P $PASS -t ${TOPIC}help -m "`/system/sdcard/scripts/mqtt-plain-status.sh`"
;;

status_json)
/system/sdcard/bin/mosquitto_pub.bin  -h $HOST -u $USER -P $PASS -t ${TOPIC}help -m "JSON Status coming soon"
;;

*)
/system/sdcard/bin/curl -m 2 ${CURLOPTS} -s http://127.0.0.1/cgi-bin/action.cgi\?cmd\=${line} -o /dev/null 2>/dev/null
if [ $? -eq "0" ];
	then

		/system/sdcard/bin/mosquitto_pub.bin  -h $HOST -u $USER -P $PASS -t ${TOPIC}${line} -m "OK (this means: action.cgi invoke with parameter ${line}, nothing more, nothing less)"

	else
		/system/sdcard/bin/mosquitto_pub.bin  -h $HOST -u $USER -P $PASS -t ${TOPIC}error -m "An error occured when executing ${line}"

fi
;;
esac
done

