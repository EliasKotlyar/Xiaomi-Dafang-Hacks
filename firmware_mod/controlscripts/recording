#!/bin/sh
. /system/sdcard/config/rtspserver.conf

PIDFILE="/run/recording.pid"

## UserName and password
if [ "$USERNAME" != "" ]; then
	CREDENTIALS="$USERNAME:$USERPASSWORD@"
fi

if [ ! -d "$DCIM_PATH" ]; then
  mkdir -p $DCIM_PATH
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
	echo "Recording already running.";
  else
	echo "Started recording."

	if [ ! -d "$DCIM_PATH/$SUB_DIR" ]; then
	  mkdir -p "$DCIM_PATH/$SUB_DIR"
	fi
	# Create the recording with timestamp
	RECORDING_PATH="$DCIM_PATH/$SUB_DIR/$FILE_NAME"
	# wait for rtspserver to become available
	until pids=$(pidof v4l2rtspserver-master)
	do
	  sleep 1
	done
	/system/sdcard/bin/busybox nohup /system/sdcard/bin/avconv -flags low_delay -fflags nobuffer -probesize 32 -i rtsp://"$CREDENTIALS"0.0.0.0:$PORT/unicast -strict experimental -y -vcodec copy -an $RECORDING_PATH &>/dev/null &
	echo "$!" > "$PIDFILE"
  fi
}

stop()
{
  pid="$(cat "$PIDFILE" 2>/dev/null)"
  if [ "$pid" ]; then
	kill "$pid"
	rm "$PIDFILE" 1> /dev/null 2>&1
	echo "Stopped recording."
  else
	echo "Could not find a running recording to stop."
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
