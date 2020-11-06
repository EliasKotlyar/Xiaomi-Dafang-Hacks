#!/bin/sh

PIDFILE="/var/run/ftp_server.pid"

status()
{
	pid="$(cat "$PIDFILE" 2>/dev/null)"
	if [ "$pid" ]; then
	  kill -0 "$pid" >/dev/null && echo "PID: $pid" || return 1
	fi
}
start()
{
	echo "Starting bftpd server"
	PID="$(pidof -o %PPID /system/sdcard/bin/bftpd)"
	if [ -z "$PID" ]; then
	  /system/sdcard/bin/bftpd -d
	  if [ $? -gt 0 ]; then
		echo "Failed to start bftpd Server"
	  else
		# wait until it forks
		sleep 2
		echo $(pidof -o %PPID bftpd) > $PIDFILE
		echo "bftpd server started"
	  fi
	else
	  echo "Failed to start bftpd Server"
	fi
}
stop()
{
	echo "Stopping bftpd Server"
	if [ -f $PIDFILE ] && kill -0 $(cat $PIDFILE); then
	  kill -15 $(cat $PIDFILE)
	  rm $PIDFILE
	  echo "bftpd server stopped"
	else
	  echo "Failed to stop bftpd Server"
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