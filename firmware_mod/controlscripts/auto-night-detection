#!/bin/sh
PIDFILE="/run/auto-night-detection.pid"
CONF_FILE="/system/sdcard/config/autonight.conf"

status()
{
  pid="$(cat "$PIDFILE" 2>/dev/null)"
  if [ "$pid" ]; then
	kill -0 "$pid" >/dev/null && echo "PID: $pid" || return 1
  fi
}

start()
{
  . $CONF_FILE
  if [ -f /run/auto-night-detection.pid ]; then
	echo "Auto night detection already running";
  else
	if [ "$autonight_mode" == "sw" ]; then
		echo "Starting software auto night detection"
		/system/sdcard/bin/busybox nohup /system/sdcard/bin/autonight $sw_parameters &>/dev/null &
	else
		echo "Starting hardware auto night detection"
		/system/sdcard/bin/busybox nohup /system/sdcard/bin/autonight $hw_parameters &>/dev/null &
	fi
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

