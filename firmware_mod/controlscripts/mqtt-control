#!/bin/sh
PIDFILE="/run/mqtt-control.pid"

if [ ! -f /system/sdcard/config/mqtt.conf ]; then
  echo "You have to configure mqtt first. Please see /system/sdcard/config/mqtt.conf.dist for further instructions"
fi

status()
{
  pid="$(cat "$PIDFILE" 2>/dev/null)"
  if [ "$pid" ]; then
	kill -0 "$pid" >/dev/null && echo "PID: $pid" || return 1
  fi
}

start()
{
  if [ -f $PIDFILE ]; then
	echo "MQTT Control already running";
  else
	. /system/sdcard/config/mqtt.conf
	if [ -z ${AUTODISCOVERY_PREFIX+x} ];
	  then echo "MQTT autodiscovery is not enabled";
	else
	  echo "MQTT autodiscovery is enabled - now publishing initial configurations";
	  /system/sdcard/scripts/mqtt-autodiscovery.sh
	fi
	echo "Starting MQTT - Control"
	/system/sdcard/bin/busybox nohup /system/sdcard/scripts/mqtt-control.sh &>/dev/null &
	echo "$!" > "$PIDFILE"
  fi
}

stop()
{
  pid="$(cat "$PIDFILE" 2>/dev/null)"
  if [ "$pid" ]; then
	kill "$pid"
	rm "$PIDFILE" 1> /dev/null 2>&1
	killall mosquitto_sub 2>/dev/null
	killall mosquitto_sub.bin 2>/dev/null
  fi
}

if [ $# -eq 0 ]; then
  start
else
  case $1 in start|stop|status)
	$1
	;;
  esac
fi
