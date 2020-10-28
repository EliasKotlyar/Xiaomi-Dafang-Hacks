#!/bin/sh

status()
{
  if [ -f /system/sdcard/config/autostart/sound-on-startup ]; then
	echo "enabled"
  fi
}

start()
{
  UPTIME=$( sed 's/\..*//g' < /proc/uptime )

  if [ ! -f /system/sdcard/config/autostart/sound-on-startup ] && [ "${UPTIME}" -gt 60 ] ; then
	echo "#!/bin/sh" > "/system/sdcard/config/autostart/sound-on-startup"
	echo "/system/sdcard/controlscripts/sound-on-startup" >> "/system/sdcard/config/autostart/sound-on-startup"
	echo "enabling sound on startup"
  fi

  # Don't play sound on activation
  if [ "${UPTIME}" -lt 60 ]; then
	/system/sdcard/bin/audioplay /usr/share/notify/CN/speaker.wav &
	echo "Please configure this option at least 1 minute after system startup"
  fi
}

stop()
{
  echo "disabling sound on startup"
  rm /system/sdcard/config/autostart/sound-on-startup
}

if [ $# -eq 0 ]; then
  start
else
  case $1 in start|stop|status)
	$1
	;;
  esac
fi

