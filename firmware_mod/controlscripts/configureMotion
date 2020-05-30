#!/bin/sh
# Motion detection (must be set before the server starting)

if [ ! -f /system/sdcard/config/motion.conf ]; then
  cp /system/sdcard/config/motion.conf.dist /system/sdcard/config/motion.conf
fi

if [ -f /system/sdcard/config/motion.conf ] ; then
	. /system/sdcard/config/motion.conf 2>/dev/null
	/system/sdcard/bin/setconf -k r -v ${region_of_interest} 2>/dev/null
	if [ "$motion_detection" = "off" ]; then
	  /system/sdcard/bin/setconf -k m -v -1 2>/dev/null
	else
	  /system/sdcard/bin/setconf -k m -v ${motion_sensitivity} 2>/dev/null
	fi
	/system/sdcard/bin/setconf -k z -v ${motion_indicator_color} 2>/dev/null
	/system/sdcard/bin/setconf -k t -v ${motion_tracking} 2>/dev/null
	/system/sdcard/bin/setconf -k u -v ${motion_timeout} 2>/dev/null
fi;
