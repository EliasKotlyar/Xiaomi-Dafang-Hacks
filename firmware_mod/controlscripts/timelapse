#!/bin/sh
PIDFILE='/run/timelapse.pid'

status()
{
  pid="$(cat "$PIDFILE" 2>/dev/null)"
  if [ "$pid" ]; then
	kill -0 "$pid" >/dev/null && echo "PID: $pid" || return 1
  fi
}

start()
{
  LOG=/dev/null
  echo "Starting timelapse"
  /system/sdcard/bin/busybox nohup /system/sdcard/scripts/timelapse.sh &> /dev/null &
  PID=$!
  echo $PID > $PIDFILE
  echo $PID
}

stop()
{ 
  PID=$(cat $PIDFILE)
  kill -9 $PID
  rm $PIDFILE
}

if [ $# -eq 0 ]; then
  start
else
  case $1 in start|stop|status)
	$1
	;;
  esac
fi
