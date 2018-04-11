#!/bin/sh

source /system/sdcard/config/mqtt

# We're not using named pipes (FIFO), but rather pipe directly to while loop
#/bin/mknod "$FIFO" p 2>/dev/null

# next two lines are a little bit cruel
killall mosquitto_sub 2> /dev/null
killall mosquitto_sub.bin 2> /dev/null

export LD_LIBRARY_PATH='/thirdlib:/system/lib:/system/sdcard/lib'

/system/sdcard/bin/mosquitto_sub.bin -v -h "$HOST" -u "$USER" -P "$PASS" -t "${TOPIC}"# | while read -r line ; do
  case $line in
    "${TOPIC}set help")
      /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -u "$USER" -P "$PASS" -t "${TOPIC}"help ${MOSQUITTOOPTS} -m "possible commands: configured topic + Yellow_LED/set on/off, configured topic + Blue_LED/set on/off, configured topic + set with the following commands: status, $(grep \)$ /system/sdcard/www/cgi-bin/action.cgi | grep -v '[=*]' | sed -e "s/ //g" | grep -v -E '(osd|setldr|settz|showlog)' | sed -e "s/)//g")"
    ;;

    "${TOPIC}set status")
      # Publish updated states
      /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -u "$USER" -P "$PASS" -t "${TOPIC}"status ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(/system/sdcard/scripts/mqtt-status.sh)"
    ;;

    "${TOPIC}Blue_LED/set on")
      /system/sdcard/bin/curl -m 2 ${CURLOPTS} -s http://127.0.0.1/cgi-bin/action.cgi\?cmd=blue_led_on -o /dev/null 2>/dev/null
      # Publish updated states
      /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -u "$USER" -P "$PASS" -t "${TOPIC}"status ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(/system/sdcard/scripts/mqtt-status.sh)"
    ;;

    "${TOPIC}Blue_LED/set off")
      /system/sdcard/bin/curl -m 2 ${CURLOPTS} -s http://127.0.0.1/cgi-bin/action.cgi\?cmd=blue_led_off -o /dev/null 2>/dev/null
      # Publish updated states
      /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -u "$USER" -P "$PASS" -t "${TOPIC}"status ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS}  -m "$(/system/sdcard/scripts/mqtt-status.sh)"
    ;;

    "${TOPIC}Yellow_LED/set on")
      /system/sdcard/bin/curl -m 2 ${CURLOPTS} -s http://127.0.0.1/cgi-bin/action.cgi\?cmd=yellow_led_on -o /dev/null 2>/dev/null
      # Publish updated states
      /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -u "$USER" -P "$PASS" -t "${TOPIC}"status ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(/system/sdcard/scripts/mqtt-status.sh)"
    ;;

    "${TOPIC}Yellow_LED/set off")
      /system/sdcard/bin/curl -m 2 ${CURLOPTS} -s http://127.0.0.1/cgi-bin/action.cgi\?cmd=yellow_led_off -o /dev/null 2>/dev/null
      # Publish updated states
      /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -u "$USER" -P "$PASS" -t "${TOPIC}"status ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(/system/sdcard/scripts/mqtt-status.sh)"
    ;;

    "${TOPIC}motion_detection/set on")
      /system/sdcard/bin/curl -m 2 "${CURLOPTS}" -s http://127.0.0.1/cgi-bin/action.cgi\?cmd=motion_detection_on -o /dev/null 2>/dev/null
      /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -u "$USER" -P "$PASS" -t "${TOPIC}"motion_detection ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "on"
    ;;

    "${TOPIC}motion_detection/set off")
      /system/sdcard/bin/curl -m 2 "${CURLOPTS}" -s http://127.0.0.1/cgi-bin/action.cgi\?cmd=motion_detection_off -o /dev/null 2>/dev/null
      /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -u "$USER" -P "$PASS" -t "${TOPIC}"motion_detection ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "off"
    ;;

    "${TOPIC}set "*)
      COMMAND=$(echo "$line" | awk '{print $2}')
      #echo "$COMMAND"
      /system/sdcard/bin/curl -m 2 ${CURLOPTS} -s http://127.0.0.1/cgi-bin/action.cgi\?cmd="${COMMAND}" -o /dev/null 2>/dev/null
      if [ $? -eq 0 ]; then
        /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -u "$USER" -P "$PASS" -t "${TOPIC}${COMMAND}" ${MOSQUITTOOPTS} -m "OK (this means: action.cgi invoke with parameter ${COMMAND}, nothing more, nothing less)"
      else
        /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -u "$USER" -P "$PASS" -t "${TOPIC}error" ${MOSQUITTOOPTS} -m "An error occured when executing ${line}"
      fi
      # Publish updated states
      /system/sdcard/bin/mosquitto_pub.bin -h "$HOST" -u "$USER" -P "$PASS" -t "${TOPIC}"status ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(/system/sdcard/scripts/mqtt-status.sh)"
    ;;
  esac
done
