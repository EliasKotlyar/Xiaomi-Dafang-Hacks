#!/bin/sh
PIDFILE="/run/dropbear.pid"

if [ ! -d /system/sdcard/root/.ssh ]; then
  mkdir /system/sdcard/root/.ssh
fi

if [ ! -f /root/.ssh/authorized_keys ]; then 
  touch /root/.ssh/authorized_keys
fi

if [ ! -f /system/sdcard/config/ssh.conf ]; then 
  cp /system/sdcard/config/ssh.conf.dist /system/sdcard/config/ssh.conf
fi

if [ ! -f /system/bin/scp ]; then
  ln -s /system/sdcard/bin/dropbearmulti /system/bin/scp
fi

if [ ! -f /var/log/lastlog ]; then
  touch /var/log/lastlog 2>/dev/null
fi

source /system/sdcard/config/ssh.conf

status()
{
  pid="$(cat "$PIDFILE" 2>/dev/null)"
  if [ "$pid" ]; then
	# Prints PID: $pid if exists and returns 0(no error) else returns 1(error condition)
	kill -0 "$pid" >/dev/null && echo "PID: $pid" || return 1
  fi
}

start()
{
  if [ "$(status)" != "" ]; then
	echo "A Dropbear sever is already running, please stop it or reboot"
  else
	echo "Starting Dropbear Server"

  	if [ "$ssh_password" = "off" ]; then
  		/system/sdcard/bin/dropbearmulti dropbear -s -R -p $ssh_port
  	else
 		/system/sdcard/bin/dropbearmulti dropbear -R -p $ssh_port
  	fi
  fi
}

stop()
{
  pid="$(cat "$PIDFILE" 2>/dev/null)"
  if [ "$pid" ]; then
	kill "$pid"
	rm "$PIDFILE" 1> /dev/null 2>&1
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
