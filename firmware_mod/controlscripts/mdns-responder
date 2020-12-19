#!/bin/sh
PIDFILE="/run/mdns-responder.pid"

status()
{
  pid="$(cat "$PIDFILE" 2>/dev/null)"
  if [ "$pid" ]; then
  	kill -0 "$pid" >/dev/null && echo "PID: $pid" || return 1
  fi
}

start()
{
  if [ -f "$PIDFILE" ]; then
  	echo "mDNSResponder already running";
  else
    echo "Starting mDNSResponder";
		/system/sdcard/bin/mDNSResponder -b -P "$PIDFILE" -n "$(hostname)" -t _rtsp._tcp -p 8554
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
