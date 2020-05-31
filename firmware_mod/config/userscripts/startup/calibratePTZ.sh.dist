#!/bin/sh

# Performs PTZ calibration at boot and if
# /system/sdcard/config/cameraposition exists
# will adjust camera to that position.
# Disabled by default as calibration can cause issues
# on cameras that do not have mechanical endstops.
# To enable:
# cp /system/sdcard/config/userscripts/startup/calibratePTZ.sh.dist /system/sdcard/config/userscripts/startup/calibratePTZ.sh

/system/sdcard/bin/motor -d v

FILECAMERAPOS=/system/sdcard/config/cameraposition

if [ -f ${FILECAMERAPOS} ]; then
	# Get values in saved config file
	origin_x_axis=`grep "x:" ${FILECAMERAPOS} | sed "s/x: //"`
	origin_y_axis=`grep "y:" ${FILECAMERAPOS} | sed "s/y: //"`
else
	# No such file exists: create it with the current values
	/system/sdcard/bin/motor -d s > ${FILECAMERAPOS}
fi

# go to home for both axis
/system/sdcard/scripts/PTZpresets.sh $origin_x_axis $origin_y_axis
