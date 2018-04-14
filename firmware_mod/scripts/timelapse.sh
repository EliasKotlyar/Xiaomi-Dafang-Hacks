#!/bin/sh

# Takes a snapshot every N seconds interval configured
# in /system/sdcard/config/timelapse.conf

PIDFILE='/run/timelapse.pid'
TIMELAPSE_CONF='/system/sdcard/config/timelapse.conf'
SAVE_DIR='/system/sdcard/DCIM/timelapse'

if [ -f "$TIMELAPSE_CONF" ]; then
    . "$TIMELAPSE_CONF" 2>/dev/null
fi

if [ -z "$TIMELAPSE_INTERVAL" ]; then TIMELAPSE_INTERVAL=2.0; fi

if [ ! -d "$SAVE_DIR" ]; then
    mkdir -p $SAVE_DIR
fi

# because``date`` doesn't support milliseconds +%N
# we have to use a running counter to generate filenames
counter=0
last_prefix=''
ts_started=$(date +%s)

while true; do
    filename_prefix="$(date +%Y-%m-%d_%H%M%S)"
    if [ "$filename_prefix" = "$last_prefix" ]; then
        counter=$(($counter + 1))
    else
        counter=1
        last_prefix="$filename_prefix"
    fi
    counter_formatted=$(printf '%03d' $counter)
    filename="${filename_prefix}_${counter_formatted}.jpg"
    /system/sdcard/bin/getimage > "$SAVE_DIR/$filename" &
    sleep $TIMELAPSE_INTERVAL

    if [ $TIMELAPSE_DURATION -gt 0 ]; then
        ts_now=$(date +%s)
        elapsed=$(($ts_now - $ts_started))
        if [ $(($TIMELAPSE_DURATION * 60)) -le $elapsed ]; then
            break
        fi
    fi
done

# loop completed so let's purge pid file
rm "$PIDFILE"
