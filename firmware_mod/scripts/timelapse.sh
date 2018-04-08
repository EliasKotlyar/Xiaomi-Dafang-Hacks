#!/bin/sh

TIMELAPSE_CONF='/system/sdcard/config/timelapse.conf'
SAVE_DIR='/system/sdcard/DCIM/timelapse'

if [ -f "$TIMELAPSE_CONF" ]; then
    source "$TIMELAPSE_CONF" 2>/dev/null
fi

if [ -z "$TIMELAPSE_INTERVAL" ]; then TIMELAPSE_INTERVAL=2.0; fi

if [ ! -d "$SAVE_DIR" ]; then
    mkdir -p $SAVE_DIR
fi

while true; do
    /system/sdcard/bin/getimage > "$SAVE_DIR/$(date +%Y-%m-%d_%H%M%S).jpg" &
    sleep $TIMELAPSE_INTERVAL
done

