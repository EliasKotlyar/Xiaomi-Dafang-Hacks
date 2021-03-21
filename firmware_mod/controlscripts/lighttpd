#!/bin/sh
PIDFILE="/run/lighttpd.pid"

## Create a certificate for the webserver
if [ ! -f /system/sdcard/config/lighttpd.pem ]; then 
  export OPENSSL_CONF=/system/sdcard/config/openssl.cnf 
  /system/sdcard/bin/openssl req -new -x509 -keyout /system/sdcard/config/lighttpd.pem -out /system/sdcard/config/lighttpd.pem -days 365 -nodes -subj "/C=DE/ST=Bavaria/L=Munich/O=.../OU=.../CN=.../emailAddress=..."
  chmod 400 /system/sdcard/config/lighttpd.pem 
  echo "Created new certificate for webserver"
fi

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
	echo "A web server is already running, please stop it or reboot"
  else
	echo "Starting web server..."
	if [ ! -f /system/sdcard/config/lighttpd.conf ]; then 
	  cp /system/sdcard/config/lighttpd.conf.dist /system/sdcard/config/lighttpd.conf
	fi
	/system/sdcard/bin/lighttpd -f /system/sdcard/config/lighttpd.conf
  fi
}

stop()
{
  pid="$(cat "$PIDFILE" 2>/dev/null)"
  if [ "$pid" ]; then
        sleep 1
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
