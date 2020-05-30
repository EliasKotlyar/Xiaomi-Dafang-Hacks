#!/bin/sh
PIDFILE="/run/mqtt-status.pid"

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
	echo "MQTT-Status already running";
  else
	echo "Starting MQTT-Status"
	/system/sdcard/bin/busybox nohup /system/sdcard/scripts/mqtt-status-interval.sh &>/dev/null &
	echo "$!" > "$PIDFILE"
  fi
}

stop()
{
  pid="$(cat "$PIDFILE" 2>/dev/null)"
  if [ "$pid" ]; then
	 kill "$pid" && rm "$PIDFILE"
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
