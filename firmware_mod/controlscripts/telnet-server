#!/bin/sh

PIDFILE="/var/run/telnetd.pid"

status()
{
	pid="$(cat "$PIDFILE" 2>/dev/null)"
	if [ "$pid" ]; then
	  kill -0 "$pid" >/dev/null && echo "PID: $pid" || return 1
	fi
}
start()
{
	echo "Starting telnetd"
	PID="$(pidof -o %PPID /sbin/telnetd)"
	if [ -z "$PID" ]; then
	  /sbin/telnetd
	  if [ $? -gt 0 ]; then
		echo "Failed to start telnetd"
	  else
		# wait until it forks
		sleep 2
		echo $(pidof -o %PPID telnetd) > $PIDFILE
		echo "Telnetd started"
	  fi
	else
	  echo "Failed to start telnetd"
	fi
}
stop()
{
	echo "Stopping telnetd"
	if [ -f $PIDFILE ] && kill -0 $(cat $PIDFILE); then
	  kill -15 $(cat $PIDFILE)
	  rm $PIDFILE
	  echo "Telnetd stopped"
	else
	  echo "Failed to stop telnetd"
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
