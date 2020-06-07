#! /bin/sh
export LD_LIBRARY_PATH='/system/sdcard/lib:/thirdlib:/system/lib'

DAEMON=onvif_srvd
DAEMON_PATH=/system/sdcard/bin
PID_FILE="/var/run/$DAEMON.pid"

DAEMON_ARGS="--pid_file $PID_FILE --ifs wlan0"

start()
{
	if [ -f $PID_FILE ] && kill -0 $(cat $PID_FILE); then
		echo "$DAEMON already running"
		return 1
	fi

	echo "Starting $DAEMON..."
	$DAEMON_PATH/$DAEMON $DAEMON_ARGS && echo "$DAEMON started"
}

stop()
{
	if [ ! -f "$PID_FILE" ] || ! kill -0 $(cat "$PID_FILE"); then
		echo "$DAEMON not running"
		return 1
	fi

	echo "Stopping $DAEMON..."
	kill -15 $(cat $PID_FILE) && rm -f $PID_FILE
	echo "$DAEMON stopped"
}

status()
{
	pid="$(cat "$PID_FILE" 2>/dev/null)"
	if [ "$pid" ]; then
	  kill -0 "$pid" >/dev/null && echo "PID: $pid" || return 1
	fi
}

restart()
{
	$0 stop
	sleep 1
	$0 start
}

if [ $# -eq 0 ]; then
  start
else
  case $1 in start|stop|restart|status)
	$1
	;;
  esac
fi
