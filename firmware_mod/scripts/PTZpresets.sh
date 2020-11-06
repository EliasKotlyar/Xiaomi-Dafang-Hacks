#!/bin/sh

#######################################################
# Accepts either presets or step coordinates		  #
# Created by slm4996								  #
# slm4996+github@gmail.com | 4-29-2020 | v0.0.1 Beta  #
#######################################################

set -e

LOG=false

logger() {
	echo "$1"
	if $LOG; then
		echo "$(date '+%Y-%m-%d-%H:%M:%S') $1" >> /system/sdcard/log/ptz.log
	fi
}

PIDFILE="/var/run/PTZpresets.pid"

# check pidfile
if [ -e "$PIDFILE" ] && [ -e "/proc/$(cat $PIDFILE)" ]
then
	# A process exists with our saved PID
	logger "PTZpresets.sh is already running with PID $PID_SAVED; exiting"
	exit 1
fi

# write pidfile
if ! echo $$ >"$PIDFILE"
then
	# If we couldn't save the PID to the lockfile...
	logger "Failed to create PID file for PID $$ in $PIDFILE; exiting"
	exit 1
fi

trap 'rm "$PIDFILE"' EXIT

# Include common_functions from Dafang-Hacks
# shellcheck disable=SC1091
. /system/sdcard/scripts/common_functions.sh

# Path to motor binary
MOTOR=/system/sdcard/bin/motor.bin

# Path to ptz_presets.conf
FILEPRESETS=/system/sdcard/config/ptz_presets.conf

# Check for custom presets file, load examples if not present
if [ ! -f ${FILEPRESETS} ]; then
	cp /system/sdcard/config/ptz_presets.conf.dist /system/sdcard/config/ptz_presets.conf
fi

# Print usage
print_usage() {
	logger "Usage:"
	logger "Presets: PTZpresets.sh preset [preset_name]"
	logger "Example: PTZpresets.sh preset home"
	logger "Presets are defined in /system/sdcard/config/ptz_presets.conf.dist."
	logger ""
	logger "Steps:   PTZpresets.sh [X axis steps] [Y axis steps]"
	logger "Example: PTZpresets.sh 1400 350"
}

# Calculate relative steps for axis
calculate_relative_steps() {
	case $1 in
		x|X)
			current_x_axis=$($MOTOR -d s | grep "$1" | awk '{print $2}')
			relative_x_steps=$(echo $(($2 - current_x_axis)) | sed 's/-//')
		;;
		y|Y)
			current_y_axis=$($MOTOR -d s | grep "$1" | awk '{print $2}')
			relative_y_steps=$(echo $(($2 - current_y_axis)) | sed 's/-//')
		;;
		*)
			exit 1
		;;
	esac
}

# Handle preset arguments
preset() {
	target_x_axis=$(/system/sdcard/bin/jq ".presets.$1.x" "$FILEPRESETS")
	target_y_axis=$(/system/sdcard/bin/jq ".presets.$1.y" "$FILEPRESETS")
	if [ "$target_y_axis" = 'null' ]; then
		logger "Error: Preset \"$1\" is not defined!"
		exit 1
	else
		logger "Loading preset $1: X=$target_x_axis, Y=$target_y_axis"
	fi
}

# Handle location arguments
location() {
	case $2 in
		[0-9]*)
			target_x_axis=$1
			target_y_axis=$2
			logger "Location defined: X=$target_x_axis, Y=$target_y_axis"
		;;
		*)
			print_usage
			exit 1
		;;
	esac
}

# Main
case "$1" in
	preset)
		preset "$2"
	;;
	[0-9]*)
		location "$1" "$2"
	;;
	*)
		print_usage
		exit 1
	;;
esac

calculate_relative_steps "x" "$target_x_axis"
calculate_relative_steps "y" "$target_y_axis"

if [ "$relative_x_steps" -ne 0 ]; then
	if [ "$target_x_axis" -lt "$current_x_axis" ]; then
		dir="l"
	else
		dir="r"
	fi

	CMD="$MOTOR -d $dir -s $relative_x_steps"
	logger "$CMD"
	$CMD > /dev/null 2>&1

	# Motor runs 1.3 time as long as the number of steps.
	SLEEP_NUM=$(awk -v a="$relative_x_steps" 'BEGIN{printf ("%f",a*1.3/1000)}')

	# Wait for motor to run
	sleep "$SLEEP_NUM"
else
	logger "X axis is already at position: $current_x_axis"
fi

if [ "$relative_y_steps" -ne 0 ]; then
	if [ "$target_y_axis" -lt "$current_y_axis" ]; then
		dir="d"
	else
		dir="u"
	fi

	CMD="$MOTOR -d $dir -s $relative_y_steps"
	logger "$CMD"
	$CMD > /dev/null 2>&1

	# Motor runs 1.3 time as long as the number of steps.
	SLEEP_NUM=$(awk -v a="$relative_y_steps" 'BEGIN{printf ("%f",a*1.3/1000)}')

	# Wait for motor to run
	sleep "$SLEEP_NUM"
else
	logger "Y axis is already at position: $current_y_axis"
fi

# Update OSD_AXIS
update_axis

exit 0
