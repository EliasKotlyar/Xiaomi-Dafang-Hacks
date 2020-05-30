#!/bin/sh

######### Bot commands #########
# /mem - show memory information
# /shot - take a shot
# /on - motion detect on
# /off - motion detect off

PIDFILE="/run/telegram-bot.pid"

if [ ! -f /system/sdcard/config/telegram.conf ]; then
  echo "You have to configure telegram first. Please see /system/sdcard/config/telegram.conf.dist for further instructions"
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
	echo "Bot already running";
  else
	echo "Starting bot"
	/system/sdcard/bin/busybox nohup /system/sdcard/scripts/telegram-bot-daemon.sh >/dev/null 2>&1 &
	echo "$!" > "$PIDFILE"
  fi
}

stop()
{
  pid="$(cat "$PIDFILE" 2>/dev/null)"
  if [ "$pid" ]; then
	kill -9 "$pid"
	rm "$PIDFILE"
	echo "Bot stopped"
  else
	echo "Could not find a bot to stop."
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
