#!/bin/sh

PIDFILE="/run/debugOnOsd.pid"

status()
{
  pid="$(cat "$PIDFILE" 2>/dev/null)"
  if [ "$pid" ]; then
	kill -0 "$pid" >/dev/null && echo "PID: $pid" || return 1
  fi
}

start()
{
  if [ -f ${PIDFILE} ]; then
	echo "Debug on OSD already running";
  else
	echo "Starting debug on OSD"
	/system/sdcard/scripts/debugInOsd.sh &>/dev/null &
#	/system/sdcard/bin/busybox nohup /system/sdcard/scripts/debugInOsd.sh &>/dev/null 
	echo "$!" > "$PIDFILE"
  fi
}

stop()
{
  pid="$(cat "$PIDFILE" 2>/dev/null)"
  if [ "${pid}" ]; then
	 kill "$pid" && rm "$PIDFILE"
	 if [ -f /system/sdcard/controlscripts/configureOsd ]; then
		source /system/sdcard/controlscripts/configureOsd
	 fi

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


